from BlockUtils import BlockUtils as bu 

MAX_TXN = 5
CURR_VER = "0.0"
buObj = bu()

class Block:
	def __init__(self, bId, diff, prevHash):
		self.blockId = bId
		self.ver = CURR_VER
		self.timestamp = buObj.get_current_timestamp()
		self.merkleRoot = ""
		self.difficulty = diff
		self.prevHash = prevHash
		self.blockHash = ""
		self.txnList = []
		self.appNum = 0    #for mining purposes
		self.blockMinedBy = "will be added"

	def calculate_block_hash(self):
		msg = ""
		msg = msg + "%s+%s+%s+%s+%s+%s+%s" % (str(self.blockId), self.ver, self.timestamp, self.merkleRoot, self.difficulty, self.prevHash, self.blockMinedBy)
		self.blockHash = buObj.get_hash256(msg)

	def calculate_merkle_root(self):
		merkleRoot = ""
		l = len(txnList)
		if l == 1:
			self.merkleRoot = buObj.get_hash256(txnList[0].hash) #merkle root for just single entry
		else:
			tx_hash = []
			tx_hashcp = []
			for i in range(l):
				tx_hash.append(self.txnList[i].hash)

			while merkleRoot == "":
				i = 0
				while i < l:
					txhash1 = tx_hash[i]
					txhash2 = ""
					i = i + 1
					if i < l:
						txhash2 = tx_hash[i]
					else:
						txhash2 = txhash1
					tx = txhash1+txhash2
					txhash12 = buObj.get_hash256(tx)
					tx_hashcp.append(txhash12)
					i = i + 1
				tx_hash = tx_hashcp.copy()
				tx_hashcp = []
				l = len(tx_hash)
				if len(tx_hash) == 1:
					merkleRoot = tx_hash[0]

			self.merkleRoot = merkleRoot

	def check_mine_status(self):
		if len(self.txnList) == MAX_TXN:
			return True
		return False

	def add_txn(self, Txn):
		if len(TxnList) < MAX_TXN:
			self.TxnList.append(Txn)
