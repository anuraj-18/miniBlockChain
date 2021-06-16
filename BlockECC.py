import random

INF = None

N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
GPoint = (Gx,Gy) #will be using x coordinate as public key

class BlockECC:
	def __init__(self):
		self.p = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 -1 
		self.a = 0
		self.b = 7

		Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
		Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424

		self.G = [Gx, Gy]

		self.sk = 0x0
		self.pk = 0x0

	def generate_secret_key(self):
		sk = '0b'
		while self.sk == 0x0:
			for i in range(256):
				sk = sk + str(random.randint(0,1))
			if int(sk, 2) >= N:
				sk = '0b'
				continue
			self.sk = hex(int(sk, 2))
			print("Your private key is: %s"%(str(self.sk)))
			self.sk = int(sk, 2)
			break


	def check_equal(self, x, y):  
		return x%self.p == y%self.p

	def get_mod(self, x):
		return x%self.p

	def inverse_mod(self, x):
		#using Fermat's Little Theorem -- > Corollary
		if self.get_mod(x) == 0:
			return None
		return pow(x, self.p-2, self.p)

	def addEcc(self, P1, P2):
		if P1 == INF:
			return P2
		if P2 == INF:
			return P1

		x1 = P1[0]; y1 = P1[1];
		x2 = P2[0]; y2 = P2[1];

		u=0

		if self.check_equal(x1, x2) and self.check_equal(y1, -1 * y2):
			return INF

		if self.check_equal(x1, x2) and self.check_equal(y1, y2):
			u = self.get_mod((3*x1**2 + self.a) * self.inverse_mod(2*y1))
		else:
			u = self.get_mod((y1 - y2)*self.inverse_mod(x1-x2))

		v = self.get_mod(y1 - u*x1)
		x3 = self.get_mod(u**2 - x1 -x2)
		y3 = self.get_mod(-u*x3 - v)
		return (x3, y3)

	def multEcc(self, k):
		#running through bits of k
		Q = INF
		if k == 0:
			return Q

		while k != 0:
			if k&1 != 0:
				Q = self.addEcc(Q, self.G)
			P = self.addEcc(self.G, self.G)
			k >>= 1
		self.pk = Q[0]
		print("Your public key is:", hex(self.pk))

	def generate_sk_pk(self):
		self.generate_secret_key()
		self.multEcc(self.sk)
		return self.sk, self.pk
		