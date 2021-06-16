import hashlib
from datetime import datetime

class BlockUtils:
	def __init__(self):
		pass

	def get_hash(self, msg):
		return hashlib.sha256(msg.encode()).hexdigest()

	def get_current_timestamp(self):
		return datetime.now().strftime("%I:%M %p, %d %b, %Y")

	def sign_msg(self, data):
		pass