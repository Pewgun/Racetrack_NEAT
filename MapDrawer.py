from tkinter import *
from line import Line
import json
WIDTH = 900
HEIGHT = 600
class Screen(Frame):
	def __init__(self, master):
		Frame.__init__(self, master, highlightthickness = 0)
		self.pack()
		self.master = master
		
		self.canvas = Canvas(self, bg='white', width=WIDTH, height = HEIGHT, borderwidth=0,highlightthickness = 0)
		self.canvas.pack()

		self.start = ()
		self.veryFirst = ()
		self.end = ()
		self.activeLine = None

		master.bind("<Button-1>", self.onClickLeft)
		master.bind("<Button-3>", self.onClickRight)
		master.bind("<Motion>", self.onDrag)
		master.bind("d", self.cancel)
		master.bind("s", self.save)
		master.bind("c", self.change)

		#add option to mark starting point
		self.lines = []
		self.checkpoints = []
		self.lineType = "Border"

		#For spawn
		self.spawn_point = None

	def cancel(self, evt):
		if self.lineType == "Border":
			if self.lines and self.start != ():#If there is at least one border
				if self.start != ():#If currently there is no active line 
					#if there is an active line then first we remove it
					self.activeLine.remove()
				self.lines[-1].remove()
				self.start = self.lines[-1].start
				del self.lines[-1]
				#Active line is updated
				self.activeLine = Line(self.canvas, self.start, self.end)
			elif self.start != ():
				self.activeLine.remove()
				self.start = ()
		elif self.lineType == "Checkpoint":
			if self.start != ():
				self.activeLine.remove()
				self.start = ()
			elif self.checkpoints:
				self.checkpoints[-1].remove()
				del self.checkpoints[-1]

	def save(self, evt):
		out = {}
		out["borders"] = []
		for line in self.lines:
			out["borders"].append({"startx": line.start[0], "starty": line.start[1], "endx": line.end[0], "endy": line.end[1]})
		out["checkpoints"] = []
		for line in self.checkpoints:
			out["checkpoints"].append({"startx": line.start[0], "starty": line.start[1], "endx": line.end[0], "endy": line.end[1]})
		out["spawn_point"] = {"startx":self.spawn_point.start[0], "starty":self.spawn_point.start[1],"endx":self.spawn_point.end[0], "endy":self.spawn_point.end[1]}
		with open("race_track_2.json",'w') as f:
			json.dump(out, f)
		print('saved')

	def change(self, evt):
		if self.lineType == "Border" and self.start == ():
			self.lineType = "Checkpoint"
		elif self.lineType == "Checkpoint" and self.start == ():
			self.lineType = "Spawn"
		elif self.lineType == "Spawn" and self.start == ():
			self.lineType = "Border"""
		print(self.lineType)

	def onClickLeft(self, evt):
		x = evt.x
		y = evt.y
		if self.lineType == "Border":
			if self.start == ():#If it is first border
				self.veryFirst = (x, y)
				self.activeLine = Line(self.canvas, (x, y), (x, y))
			else:#If this is a following border in a sequence
				self.lines.append(self.activeLine)
				self.activeLine = Line(self.canvas, self.start, (x, y))
			self.start = (x, y)#Storing the starting point
		elif self.lineType == "Checkpoint" and self.start == ():
			self.activeLine = Line(self.canvas, (x, y), (x, y))
			self.start = (x, y)
		elif self.lineType == "Spawn" and self.start == ():
			if self.spawn_point:
				self.spawn_point.remove()
			self.activeLine = Line(self.canvas, (x, y), (x, y))
			self.start = (x, y)

	def onClickRight(self, evt):
		if self.lineType == "Border":
			self.activeLine.remove()
			self.lines.append(Line(self.canvas, self.start, self.veryFirst))
			self.start = ()
			self.veryFirst = ()
		elif self.lineType == "Checkpoint" and self.start != ():
			self.activeLine.remove()
			self.checkpoints.append(Line(self.canvas, self.start, self.end, clr="red"))
			self.start = ()
		elif self.lineType == "Spawn" and self.start != ():
			self.spawn_point = self.activeLine
			self.start = ()

	def onDrag(self, evt):
		if self.start == (): 
			self.end = (evt.x, evt.y)
			return

		if self.lineType == "Border":
			self.activeLine.remove()
			self.activeLine = Line(self.canvas, self.start, (evt.x, evt.y))
		elif self.lineType == "Checkpoint":
			self.activeLine.remove()
			self.activeLine = Line(self.canvas, self.start, (evt.x, evt.y), clr="red")
		elif self.lineType == "Spawn":
			self.activeLine.remove()
			self.activeLine = Line(self.canvas, self.start, self.end, clr="green")
		self.end = (evt.x, evt.y)

def main():
	root = Tk()
	root.resizable(False, False)
	root.geometry(str(WIDTH)+"x"+str(HEIGHT))

	screen = Screen(root)
	while True:
		root.update()
		root.update_idletasks()

if __name__ == '__main__':
	main()