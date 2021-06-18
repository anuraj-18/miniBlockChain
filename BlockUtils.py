import hashlib
from datetime import datetime

class BlockUtils:
	def __init__(self):
		pass

	def get_hash256(self, msg):
		return hashlib.sha256(msg.encode()).hexdigest()

	def get_hash256_int(self, msg):
		return int(self.get_hash256(msg), 16)

	def get_current_timestamp(self):
		return datetime.now().strftime("%I:%M %p, %d %b, %Y")

	def sign_msg(self, data):
		pass