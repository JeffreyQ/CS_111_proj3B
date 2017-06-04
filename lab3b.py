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
		# SUPERBLOCK SUMMARY
		self.numBlocks = 0
		self.numInodes = 0
		self.blockSize = 0
		self.inodeSize = 0
		self.blocksPerGroup = 0
		self.inodesPerGroup = 0
		self.firstNonRsrvdInode = 0
		self.csvfile = csvfile

		# GROUP SUMMARY
		self.groupNum = 0
		self.numFreeBlocks = 0
		self.numFreeInodes = 0
		self.bbmapNum = 0
		self.ibmapNum = 0
		self.firstInodeBlockNum = 0

		self.reader = csv.reader(csvfile, delimiter=",")
		self.free_blocks = set()
		self.free_inodes = set()

		self.unrefBlocks = set()
		self.allocatedBlocks = set() # bad naming convention, intuitively refers to opposite of what the spec is trying to say
		
		self.reservedBlocks = set()


	def initData(self):
		for i in range(1, 8):
			self.reservedBlocks.add(i)
		for row in self.reader:
			if row[0] == "SUPERBLOCK":
				self.numBlocks = row[1]
				self.numInodes = row[2]
				self.blockSize = row[3]
				self.inodeSize = row[4]
				self.blocksPerGroup = row[5]
				self.inodesPerGroup = row[6]
				self.firstNonRsrvdInode = row[7]
			elif row[0] == "BFREE":
				self.free_blocks.add( int(row[1]) )	
			elif row[0] == "IFREE":
				self.free_inodes.add( int(row[1]) )		
			elif row[0] == "GROUP":
				self.groupNum = row[1]
				self.numFreeBlocks = row[4]
				self.numFreeInodes = row[5]
				self.bbmapNum = row[6]
				self.ibmapNum = row[7]
				self.firstInodeBlockNum = row[8]
			elif row[0] == "INODE":
				for item in row[12:]: # slicing
					if item == 0:
						break
					self.allocatedBlocks.add( int(item))
			elif row[0] == "INDIRECT":
				self.allocatedBlocks.add( int(row[5]) )

	def printAllocatedBlocks(self):
		for blockNum in self.allocatedBlocks:
			if blockNum in self.free_blocks:
				print "ALLOCATED BLOCK %s ON FREELIST" % (blockNum)

	def printUnrefBlocks(self):
		for i in range(0, int(self.numBlocks)):
			if i not in self.free_blocks and i not in self.allocatedBlocks and i not in self.reservedBlocks:
				print "UNREFERENCED BLOCK %s" % (i)

	def printContents(self):
		for item in self.allocatedBlocks:
			print item


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
	FSA.initData()
	FSA.printAllocatedBlocks()
	FSA.printUnrefBlocks()
#	FSA.printContents()
	
