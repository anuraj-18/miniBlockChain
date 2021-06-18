import random

INF = None
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

class BlockECC:
	def __init__(self):
		self.p = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 -1 
		self.a = 0
		self.b = 7

		Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
		Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424

		self.G = (Gx, Gy)

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
			self.sk = int(sk, 2)
			str_sk = "0x{:X}".format(self.sk)
			str_sk = str_sk.zfill(64)
			while len(str_sk) < 66:
				str_sk = str_sk[0:2] + "0" + str_sk[2:]
			print("Your private key is: "+str_sk)
			break

	def check_equal(self, x, y):  
		return (x-y)%self.p == 0

	def get_mod(self, x):
		return x%self.p

	def inverse_mod(self, a):
		#using Fermat's Little Theorem -- > Corollary
		lm, hm = 1,0
		low, high = a%self.p,self.p
		while low > 1:
			ratio = high//low
			nm, new = hm-lm*ratio, high-low*ratio
			lm, low, hm, high = nm, new, lm, low
		return lm % self.p

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
			u = self.get_mod((3*x1*x1 + self.a) * self.inverse_mod(2*y1))
		else:
			u = self.get_mod((y1 - y2)*self.inverse_mod(x1-x2))

		x3 = self.get_mod(u*u - x1 - x2)
		y3 = self.get_mod(u*(x1-x3) - y1)
		return (x3, y3)

	def generate_public_key(self, k):
		#running through bits of k
		Q = INF
		if k == 0:
			return Q
		P = self.G
		while k != 0:
			
			if k&1 != 0:
				Q = self.addEcc(Q, P)
			P = self.addEcc(P, P)
			k >>= 1
		self.pk = Q[0]
		str_pk = "0x{:X}".format(self.pk)
		str_pk = "0x"+str_pk[2:].zfill(64)
		if self.pk%2 == 1:
			print("Your public key is:"+" 03 "+"0x{:X}".format(self.pk))
		else:
			print("Your public key is:"+" 02 "+"0x{:X}".format(self.pk))

	def is_point_on_curve(self, P):
		(x1, y1) = P
		return self.check_equal(y1*y1, x1*x1*x1 + self.a*x1 + self.b)

	def generate_sk_pk(self):
		self.generate_secret_key()
		self.generate_public_key(self.sk)
		return self.sk, self.pk

ecc=BlockECC()
ecc.generate_sk_pk()
