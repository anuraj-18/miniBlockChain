import random
from BlockUtils import BlockUtils as bu

INF = None
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
RandNum = 28695618543805844332113829720373285210420739438570883203839696518176414791234
buObj = bu()

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
		self.pkFull = (0x0, 0x0)

		self.randomP = self.multiply_ecc(RandNum, self.G)

	def convert_to_strhex(self, num):
		str_hex = "0x{:X}".format(num)
		str_hex = str_hex.zfill(64)
		return str_hex

	def generate_secret_key(self):
		sk = '0b'
		while self.sk == 0x0:
			for i in range(256):
				sk = sk + str(random.randint(0,1))
			if int(sk, 2) >= N:
				sk = '0b'
				continue

			self.sk = int(sk, 2)
			str_sk = self.convert_to_strhex(self.sk)

			print("Your private key is: "+str_sk)
			break

	def check_equal(self, x, y):  
		return (x-y)%self.p == 0

	def get_mod(self, x):
		return x%self.p

	def inverse_mod(self, a):
		#using Fermat's Little Theorem -- > Corollary
		lm, hm = 1, 0
		low, high = a%self.p,self.p
		while low > 1:
			ratio = high//low
			nm, new = hm-lm*ratio, high-low*ratio
			lm, low, hm, high = nm, new, lm, low
		return lm % self.p

	def inverse_mod_n(self, a, n):
		lm, hm = 1, 0
		low, high = a%n, n
		while low > 1:
			ratio = high//low
			nm, new = hm-lm*ratio, high-low*ratio
			lm, low, hm, high = nm, new, lm, low
		return lm % n

	def add_ecc(self, P1, P2):
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
				Q = self.add_ecc(Q, P)
			P = self.add_ecc(P, P)
			k >>= 1
		self.pk = Q[0]
		self.pkFull = Q
		str_pk = self.convert_to_strhex(self.pk)
		if self.pk%2 == 1:
			print("Your public key is:"+" 03 "+str_pk)
		else:
			print("Your public key is:"+" 02 "+str_pk)

	def multiply_ecc(self, k, P):
		Q = INF
		if k == 0:
			return Q
		while k != 0:
			if k&1 != 0:
				Q = self.add_ecc(Q, P)
			P = self.add_ecc(P, P)
			k >>= 1
		return Q

	def is_point_on_curve(self, P):
		(x1, y1) = P
		return self.check_equal(y1*y1, x1*x1*x1 + self.a*x1 + self.b)

	def generate_sk_pk(self):
		self.generate_secret_key()
		self.generate_public_key(self.sk)
		return self.sk, self.pk

	def sign_msg(self, msg):
		self.randomP = self.multiply_ecc(RandNum, self.G)
		r = self.randomP[0]%N
		msgHash = buObj.get_hash256_int(msg)
		signature = ((msgHash + (r*self.sk))*(self.inverse_mod_n(RandNum, N)))%N
		print("Signature of the message: %s"%(self.convert_to_strhex(signature)))
		return signature, msgHash

	def sign_verification(self, signature, msgHash):
		w = self.inverse_mod_n(signature, N)
		r = self.randomP[0]%N
		p1 = self.multiply_ecc((msgHash * w)%N, self.G)
		p2 = self.multiply_ecc((r * w)%N, self.pkFull)  
		(x,y) = self.add_ecc(p1, p2)
		if r==x:
			print("Signature verification completed.")
		else:
			print("Signature verification failed.")
		return r == x 
