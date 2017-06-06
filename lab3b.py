import sys
import csv

"""
 * superblock summary
 *
 * A single new-line terminated line, comprised of eight comma-separated fields (with no white-space), summarizing the key file system parameters:
 *
 * 1. SUPERBLOCK
 * 2. total number of blocks (decimal)
 * 3. total number of i-nodes (decimal)
 * 4. block size (in bytes, decimal)
 * 5. i-node size (in bytes, decimal)
 * 6. blocks per group (decimal)
 * 7. i-nodes per group (decimal)
 * 8.first non-reserved i-node (decimal)
 *
"""

"""
 * group summary
 *
 * Scan each of the groups in the file system. For each group, produce a new-line 
 * terminated line for each group, each comprised of nine comma-separated fields 
 * (with no white space), summarizing its contents.
 *
 * 1. GROUP
 * 2. group number (decimal, starting from zero)
 * 3. total number of blocks in this group (decimal)
 * 4. total number of i-nodes in this group (decimal)
 * 5. number of free blocks (decimal)
 * 6. number of free i-nodes (decimal)
 * 7. block number of free block bitmap for this group (decimal)
 * 8. block number of free i-node bitmap for this group (decimal)
 * 9. block number of first block of i-nodes in this group (decimal)
 * 
"""

"""
 * free block entries
 *
 * Scan the free block bitmap for each group. For each free block, produce a 
 * new-line terminated line, with two comma-separated fields (with no white space).
 * 
 * 1. BFREE
 * 2. number of the free block (decimal)
 * 
"""

"""
 * free I-node entries
 *
 * Scan the free I-node bitmap for each group. For each free I-node, produce a 
 * new-line terminated line, with two comma-separated fields (with no white space).
 * 
 * 1. IFREE
 * 2. number of the free I-node (decimal)
 *
"""

"""
 * I-node summary
 *
 * Scan the I-nodes for each group. For each valid (non-zero mode and non-zero link count) 
 * I-node, produce a new-line terminated line, with 27 comma-separated fields (with no 
 * white space). The first twelve fields are i-node attributes:
 * 
 * 1. INODE
 * 2. inode number (decimal)
 * 3. file type ('f' for file, 'd' for directory, 's' for symbolic link, '?" for anything else)
 * 4. mode (octal)
 * 5. owner (decimal)
 * 6. group (decimal)
 * 7. link count (decimal)
 * 8. creation time (mm/dd/yy hh:mm:ss, GMT)
 * 9. modification time (mm/dd/yy hh:mm:ss, GMT)
 * 10. time of last access (mm/dd/yy hh:mm:ss, GMT)
 * 11. file size (decimal)
 * 12. number of blocks (decimal)
 * 13. The next fifteen fields are block addresses (decimal, 12 direct, one indirect, one double indirect, one tripple indirect).
"""



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
		self.reservedInodes = set()
		self.allocatedInodes = set()

	def initData(self):
		# refer to the summaries above
		for row in self.reader:
			if row[0] == "SUPERBLOCK":
				self.numBlocks = row[1]
				self.numInodes = row[2]
				self.blockSize = row[3]
				self.inodeSize = row[4]
				self.blocksPerGroup = row[5]
				self.inodesPerGroup = row[6]
				self.firstNonRsrvdInode = row[7]
			if row[0] == "BFREE":
				self.free_blocks.add( int(row[1]) )	
			if row[0] == "IFREE":
				self.free_inodes.add( int(row[1]) )		
			if row[0] == "GROUP":
				self.groupNum = row[1]
				self.numFreeBlocks = row[4]
				self.numFreeInodes = row[5]
				self.bbmapNum = row[6]
				self.ibmapNum = row[7]
				self.firstInodeBlockNum = row[8]
			if row[0] == "INODE":
				# populate allocated inodes with inode
				self.allocatedInodes.add( int(row[1]) )
				# populate allocated blocks with inode direct pointers
				for item in row[12:24]: # slicing
					if int(item) != 0:
						if int(item) >= int(self.numBlocks) or int(item) < 0:
							print "INVALID BLOCK %d IN INODE %d AT OFFSET 0" % (int(item), int(row[1]))
						else:
							self.allocatedBlocks.add( int(item) )
				if int(row[24]) != 0:
					if int(row[24]) >= int(self.numBlocks) or int(item) < 0:
						print "INVALID INDIRECT BLOCK %d IN INODE %d AT OFFSET 12" % (int(row[24]), int(row[1]))
					else:
						self.allocatedBlocks.add( int(row[24]) )
				if int(row[25]) != 0:
					if int(row[25]) >= int(self.numBlocks) or int(item) < 0:
						print "INVALID DOUBLE INDIRECT BLOCK %d IN INODE %d AT OFFSET 268" % (int(row[25]), int(row[1]))
					else:
						self.allocatedBlocks.add( int(row[25]) )
				if int(row[26]) != 0:
					if int(row[26]) >= int(self.numBlocks) or int(item) < 0:
						print "INVALID TRIPPLE INDIRECT BLOCK %d IN INODE %d AT OFFSET 65804" % (int(row[26]), int(row[1]))
					else:
						self.allocatedBlocks.add( int(row[26]) )
						
				
			# populate allocated blocks set with referenced blockNum of INDIR block
			if row[0] == "INDIRECT":
				self.allocatedBlocks.add( int(row[5]) )
		# populate reservedBlocks set with blocks reserved by the system
		for i in range(0, 8):
			self.reservedBlocks.add(i)
		# populate reservedInodes set with inodes reserved by the system
		for i in range(0, int(self.firstNonRsrvdInode)):
			self.reservedInodes.add(i)

	def printReservedBlocks(self):
		print self.reader
		for row in self.reader:
			print row
			if row[0] == "INODE":
				for item in row[12:24]:
					if item in self.reservedBlocks:
						print "RESERVED BLOCK %d IN INODE %d AT OFFSET 0" % (int(item), int(row[1]))



	def printAllocatedBlocks(self):
		for block in self.allocatedBlocks:
			if block in self.free_blocks:
				print "ALLOCATED BLOCK %s ON FREELIST" % (block)




	def printUnrefBlocks(self):
		for i in range(0, int(self.numBlocks)):
			if i not in self.free_blocks and i not in self.allocatedBlocks and i not in self.reservedBlocks:
				print "UNREFERENCED BLOCK %s" % (i)

	# def printInvalBlocks(self):
	#	for blockNum in self.allocatedBlocks:
	#		if blockNum >= self


	def printAllocatedInodes(self):
		for i in range(0, int(self.numInodes)):
			if i not in self.allocatedInodes and i not in self.free_inodes and i not in self.reservedInodes:
				print "UNALLOCATED INODE %d NOT ON FREELIST" % (i)

	def printAllInodeInconsistency(self):
		for inode in self.free_inodes:
			if inode in self.reservedInodes:
				print "ALLOCATED INODE %d ON FREELIST" % (inode)

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
	FSA.printAllocatedInodes()
	FSA.printAllInodeInconsistency()
#	FSA.printReservedBlocks()
#	FSA.printContents()
	
