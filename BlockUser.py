from BlockUtils import BlockUtils as bu 
from BlockECC import BlockECC as Ecc
from Block import Block as blk 

class User:
	def __init__(self):
		ecc = Ecc()
		self.sk, self.pk = ec.generate_sk_pk()

	def mine_block(self):
		pass
