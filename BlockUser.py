from BlockUtils import BlockUtils as bu 
from BlockECC import BlockECC as Ecc
from Block import Block as blk 

class User:
	def __init__(self):
		ecc = Ecc()
		self.sk, self.pk = ecc.generate_sk_pk()
		self.balance = 0 #0 coins, someon will have to send you someone, do some Work

	def mine_block(self):
		pass

	def recieveCoins(self, amount):
		pass

	def sendCoins(self, amount, u_pk):
		pass
