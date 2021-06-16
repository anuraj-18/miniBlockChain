from BlockUtils.py import BlockUtils as bu 
from Block import Block as blk 

class User:
	def __init__(self):
		self.sk, self.pk = self.generatePairKeys()
		

