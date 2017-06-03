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
		self.firstNonRsvpInode = 0
		self.csvfile = csvfile

	def initSuperblock(self):
		reader = csv.reader(self.csvfile, delimiter=",")
		for row in reader:
			print row



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
	
