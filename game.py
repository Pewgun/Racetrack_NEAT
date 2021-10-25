from tkinter import *
from car import Car
from line import Line
import json
from population import Population
import math

WIDTH = 900
HEIGHT = 600
class Screen(Frame):
#class Screen(Canvas):
#class Screen:
	#def __init__(self, master, genomes):
	def __init__(self, genomes, master=None, show=True):
		self.show = show	
		if show:
			Frame.__init__(self, master, width=WIDTH, height=HEIGHT, highlightthickness = 0)
			self.pack(fill="both", expand=True)
			self.my_canvas = Canvas(self, width=WIDTH, height=HEIGHT)
			self.my_canvas.pack(fill="both", expand=True)
		else:
			self.my_canvas = None
		
		self.borders = []
		self.checkpoints = []
		self.startx = 0
		self.starty = 0
		self.endx = 0
		self.endy = 0
		self.loadFromFile()

		def lengthh(x1, y1, x2, y2):
			return math.sqrt((x1-x2)**2 + (y1-y2)**2)

		self.cars = []
		length = lengthh(self.startx, self.starty, self.endx, self.endy)
		for g in genomes:
			self.cars.append(Car(self.my_canvas, [self.startx, self.starty], g, dirr=[(self.endx-self.startx)/length, (self.endy-self.starty)/length], show=self.show))
		c = self.cars[0]
		for c in self.cars:
			c.addCheckpoints([ch for ch in self.checkpoints])

	def loadFromFile(self):
		with open("race_track_2.json") as f:
			data = json.load(f)

		for line in data["borders"]:
			border = Line(self.my_canvas, (line["startx"], line["starty"]), (line["endx"], line["endy"]), show=self.show)
			self.borders.append(border)

		for line in data["checkpoints"]:
			ch = Line(self.my_canvas, (line["startx"], line["starty"]), (line["endx"], line["endy"]), clr='red', show=self.show)
			self.checkpoints.append(ch)

		spawn_point = data["spawn_point"]
		self.startx = spawn_point["startx"]
		self.starty = spawn_point["starty"]
		self.endx = spawn_point["endx"]
		self.endy = spawn_point["endy"]

	def doActions(self):
		#Cars do actions
		for c in self.cars:
			c.decide(self.borders)
			c.numOfDecisions += 1
			c.brain.fitness += 0.1

		#Check if any has died
		for c in self.cars:
			for border in self.borders:
				if c.intersects(border):
					c.alive = False
					continue
		#Can add check that if a car made for exaple 20 decision and still has not reached next chekpoint!!!!
		#We can assume it's dead
		for c in self.cars:
			if c.numOfDecisions > 60:
				c.alive = False
				continue
		#Update cars
		newCars = []
		for c in self.cars:
			if c.alive:
				newCars.append(c)
			elif self.show:
				c.remove()
		self.cars = newCars

		#Check if any has passed checkpoints
		for c in self.cars:
			if c.passedCheckpoint():
				c.brain.fitness += 10.0
				c.numOfDecisions = 0
				c.chPassed += 1

		return self.cars != []
		
def main():
	import time
	pop = Population()	
	flag = False
	i = 0
	while True:
		i += 1
		print(f"Generation: {i}")
		screen = Screen(pop.genomes, show=False)
		while screen.doActions():
			for c in screen.cars:
				if c.chPassed == 100*27:#16 circles
					flag = True
			if flag:
				break
		pop.naturalSelection()
		if flag or i == 300:
			break
	pop.bestGenome.saveToFile("Genome100")

	"""from genome import Genome
	root = Tk()
	root.geometry(str(WIDTH)+"x"+str(HEIGHT))
	g = Genome.loadFromFile("Genome100.json")
	screen = Screen([g], master=root)"""
	root = Tk()
	root.geometry(str(WIDTH)+"x"+str(HEIGHT))
	screen = Screen([pop.bestGenome], master=root, show=True)
	flag = False
	i = 0
	score = 0
	while screen.doActions():
		root.update()
		root.update_idletasks()
		time.sleep(0.1)
		for c in screen.cars:
			"""if c.chPassed == 64*27:# 32 circles
				print("cool")
				flag = True"""
			score = c.chPassed//27
			print(score)
		if flag:
			break
	screen.destroy()
	print("Done")
	"""pop.showSpeciesMemNum()
	pop.showFitnessGrowth()
	pop.showBestGenomeNeuralNet()"""

if __name__ == '__main__':
	main()