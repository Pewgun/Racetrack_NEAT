
class Line:

	def __init__(self, canvas, start, end, clr='black', show=True):
		self.canvas = canvas
		self.start = start
		self.end = end
		self.show = show
		if show:
			self.lineId = self.canvas.create_line(self.start[0], self.start[1], self.end[0], self.end[1], fill=clr)

	def remove(self):
		if self.show:
			self.canvas.delete(self.lineId)

	# Return true if line segments AB and CD intersect
	def intersects(self, otherLine):
		def ccw(A,B,C):
			return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])
		A = self.start
		B = self.end
		C = otherLine.start
		D = otherLine.end
		return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

	def find_intersection(self, otherLine) :
		p0 = self.start
		p1 = self.end
		p2 = otherLine.start
		p3 = otherLine.end

		s10_x = p1[0] - p0[0]
		s10_y = p1[1] - p0[1]
		s32_x = p3[0] - p2[0]
		s32_y = p3[1] - p2[1]

		denom = s10_x * s32_y - s32_x * s10_y

		if denom == 0 : return None # collinear

		denom_is_positive = denom > 0

		s02_x = p0[0] - p2[0]
		s02_y = p0[1] - p2[1]

		s_numer = s10_x * s02_y - s10_y * s02_x

		if (s_numer < 0) == denom_is_positive : return None # no collision

		t_numer = s32_x * s02_y - s32_y * s02_x

		if (t_numer < 0) == denom_is_positive : return None # no collision

		if (s_numer > denom) == denom_is_positive or (t_numer > denom) == denom_is_positive : return None # no collision


		# collision detected

		t = t_numer / denom

		intersection_point = [ p0[0] + (t * s10_x), p0[1] + (t * s10_y) ]


		return intersection_point