from time import sleep
class Move:
	__move=None
	def __init__(self,w1,w2):
		self.w1=w1
		self.w2=w2
		self.ready=False
		self.paused=False

	def getInstance(w1,w2):
		if Move.__move is None:
			Move.__move=Move(w1,w2)
		return Move.__move
	
	def mstart(self):
		self.w1.setupp()
		self.w2.setupp()
		self.w1.begin()
		self.w2.begin()
		self.ready=True
		
	def forward(self):
		if self.paused:
			self.paused=False
			self.w1.mresume()
			self.w2.mresume()
		self.w1.clkwise()
		self.w2.clkwise()
	
	def reverse(self):
		if self.paused:
			self.paused=False
			self.w1.mresume()
			self.w2.mresume()
		self.w1.aclkwise()
		self.w2.aclkwise()

	def right(self):
		if self.paused:
			self.paused=False
			self.w1.mresume()
			self.w2.mresume()
		self.w1.aclkwise()
		self.w2.clkwise()
	
	def left(self):
		if self.paused:
			self.paused=False
			self.w1.mresume()
			self.w2.mresume()
		self.w1.clkwise()
		self.w2.aclkwise()

	def mhalt(self):
		self.w1.mstop()
		self.w2.mstop()
		self.paused=True

	def finish(self):
		self.w1.terminate()
		self.w2.terminate()
		self.ready=False
