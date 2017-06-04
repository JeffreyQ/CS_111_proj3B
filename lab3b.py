import sys
import csv



class Inode:
	def __init__(self, inum, numLinks):
		self.inum = inum # inode number
		self.numLinks = numLinks # number of hard links to this inode
		self.pointers = set() # the set of directory entries that point to this inode
		self.blockptrs = set() # block pointers, EXT2: 12 direct, 3 indrect


class Block:
	def __init__(self, blockNum):
		self.blockNum = blockNum # block number
		self.pointers = set() # the set of inodes that point to this block



class analyzer:
	def __init__(self, csvfile):
		# SUPERBLOCK INFO
		self.numBlocks = 0
		self.numInodes = 0
		self.blockSize = 0
		self.inodeSize = 0
		self.blocksPerGroup = 0
		self.inodesPerGroup = 0
		self.firstNonRsrvdInode = 0
		self.csvfile = csvfile

		self.free_blocks = set()

	def initSuperblock(self):
		reader = csv.reader(self.csvfile, delimiter=",")
		rows = list(reader)
		self.numBlocks = rows[0][1]
		self.numInodes = rows[0][2]
		self.blockSize = rows[0][3]
		self.inodeSize = rows[0][4]
		self.blocksPerGroup = rows[0][5]
		self.inodesPerGroup = rows[0][6]
		self.firstNonRsrvdInode = rows[0][7]
"""	
		print self.numBlocks
		print self.numInodes
		print self.blockSize
		print self.inodeSize
		print self.blocksPerGroup
		print self.inodesPerGroup
		print self.firstNonRsrvdInode
"""

	# def initFreeList(self):
		


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print >> sys.stderr, "Usage:\tpython lab3b.py *.csv"
		sys.exit(1)
	try:
		f = open(sys.argv[1], 'r')
	except IOError:
		print >> sys.stderr, "Could not read file"
		sys.exit(1)
	
	FSA = analyzer(f)
	FSA.initSuperblock()
	
