import math
from line import Line

class Car:

	def __init__(self, canvas, center, brain,dirr=[], show=True):
		self.brain = brain
		self.brain.prepareNetwork()
		self.alive = True
		self.numOfDecisions = 0
		self.chPassed = 0
		self.show = show

		self.chInOrder = []

		self.canvas = canvas
		if dirr == []:
			self.dirX = 0
			self.dirY = -1
		else:
			self.dirX = dirr[0]
			self.dirY = dirr[1]
		self.speed = 5
		self.center = center#[x, y]
		self.width = 10
		self.height = 20
		self.angle = math.pi*10/180#Turn angle
		self.sides = []
		self.detectors = []
		self.detectorLength = 150
		self.update()

	def addCheckpoints(self, chs):
		self.chs = chs

	def passedCheckpoint(self):
		if self.intersects(self.chs[0]):
			ch = self.chs.pop(0)
			self.chs.append(ch)
			return True
		return False

	def update(self):
		if self.sides and self.show:
			for side in self.sides:
				side.remove()
		self.sides[:] = []

		x1 = self.center[0] + (self.height/2)*self.dirX + (self.width/2)*self.dirY
		y1 = self.center[1] + (self.height/2)*self.dirY + (self.width/2)*-self.dirX
		x2 = self.center[0] + (self.height/2)*self.dirX - (self.width/2)*self.dirY
		y2 = self.center[1] + (self.height/2)*self.dirY - (self.width/2)*-self.dirX
		x3 = self.center[0] - (self.height/2)*self.dirX - (self.width/2)*self.dirY
		y3 = self.center[1] - (self.height/2)*self.dirY - (self.width/2)*-self.dirX
		x4 = self.center[0] - (self.height/2)*self.dirX + (self.width/2)*self.dirY
		y4 = self.center[1] - (self.height/2)*self.dirY + (self.width/2)*-self.dirX
		self.sides.append(Line(self.canvas, (x1, y1), (x2, y2), show= self.show))
		self.sides.append(Line(self.canvas, (x2, y2), (x3, y3), show= self.show))
		self.sides.append(Line(self.canvas, (x3, y3), (x4, y4), show= self.show))
		self.sides.append(Line(self.canvas, (x4, y4), (x1, y1), show= self.show))
		########################################################
		if self.detectors and self.show:
			for detector in self.detectors:
				detector.remove()
		self.detectors[:] = []
			
		numberOfDetectors = 8
		start = (self.center[0] + (self.height/2)*self.dirX, self.center[1] + (self.height/2)*self.dirY)
		detectorAngle = -math.pi*1/2
		detectorDirX = self.dirX*math.cos(detectorAngle) - self.dirY*math.sin(detectorAngle)
		detectorDirY = self.dirX*math.sin(detectorAngle) + self.dirY*math.cos(detectorAngle)
		detectorAngle = math.pi*1/(numberOfDetectors+1)
		
		for i in range(numberOfDetectors):
			detectorDirX, detectorDirY = detectorDirX*math.cos(detectorAngle) - detectorDirY*math.sin(detectorAngle),detectorDirX*math.sin(detectorAngle) + detectorDirY*math.cos(detectorAngle)
			end = (start[0] + detectorDirX*self.detectorLength, start[1] + detectorDirY*self.detectorLength)
			self.detectors.append(Line(self.canvas, start, end, clr="red", show= self.show))

	def returnDetections(self, borders):
		import math
		outs = []
		for detector in self.detectors:
			distance = float('inf')
			for border in borders:
				res = detector.find_intersection(border)
				if res:
					distance = min(distance, math.sqrt((res[0]-detector.start[0])**2 + (res[1]-detector.start[1])**2))
			if distance != float('inf'):
				outs.append(distance/self.detectorLength)
			else:
				outs.append(0.0)
		return outs

	def decide(self, borders):
		out = self.brain.feedForward(self.returnDetections(borders))

		#Move forward or backwards or None
		"""if out[0] < 1.0/3.0:
			#Move forward
			self.moveForward()
		elif out[0] > 2.0/3.0:
			self.moveBackwards()"""
		self.moveForward()

		if out[0] < 0.5:#1.0/3.0:
			#Move forward
			self.rotateRight()
		else:#elif out[0] > 2.0/3.0:
			self.rotateLeft()


	def rotateRight(self):
		newDirX = self.dirX*math.cos(self.angle) - self.dirY*math.sin(self.angle)
		newDirY = self.dirX*math.sin(self.angle) + self.dirY*math.cos(self.angle)
		self.dirX = newDirX
		self.dirY = newDirY
		self.update()

	def rotateLeft(self):
		newDirX = self.dirX*math.cos(-self.angle) - self.dirY*math.sin(-self.angle)
		newDirY = self.dirX*math.sin(-self.angle) + self.dirY*math.cos(-self.angle)
		self.dirX = newDirX
		self.dirY = newDirY
		self.update()

	def moveForward(self):
		self.center[:] = [self.center[0] + self.dirX*self.speed, self.center[1] + self.dirY*self.speed]
		self.update()

	def moveBackwards(self):
		self.center[:] = [self.center[0] - self.dirX*self.speed, self.center[1] - self.dirY*self.speed]
		self.update()

	def intersects(self, line):
		for side in self.sides:
			if side.intersects(line):
				return True
		return False

	def remove(self):
		for side in self.sides:
			side.remove()
		for detector in self.detectors:
			detector.remove()
		