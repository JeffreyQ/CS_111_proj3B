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

class inodeSummary: 
	def __init__(self):
		self.inodeNumber = 0
		self.linkCount = 0
		self.blockPointers = list()




class direntSummary:
	def __init__(self):
		self.parentInode = 0
		self.offset = 0
		self.fileInode = 0
		self.entryLen = 0
		self.nameLen = 0
		self.name = ""


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
 * 13. The next fifteen fields are block appendresses (decimal, 12 direct, one indirect, one double indirect, one tripple indirect).
"""

class indirect:
	def __init__(self):
		self.inodeNumber = 0
		self.indirLevel = 0
		self.blockOffset = 0
		self.blockNumber = 0


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
		self.free_blocks = list()
		self.free_inodes = list()

		self.unrefBlocks = list()
		self.allocatedBlocks = list() # bad naming convention, intuitively refers to opposite of what the spec is trying to say
		
		self.reservedBlocks = list()
		self.reservedInodes = list()
		self.allocatedInodes = list()
		self.inodeList = list()
		self.indirectList = list()
		self.allInodes = list()
		self.allBlocks = list()
		self.direntList = list()
		


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
				self.free_blocks.append( int(row[1]) )	
			if row[0] == "IFREE":
				self.free_inodes.append( int(row[1]) )		
			if row[0] == "GROUP":
				self.groupNum = row[1]
				self.numFreeBlocks = row[4]
				self.numFreeInodes = row[5]
				self.bbmapNum = row[6]
				self.ibmapNum = row[7]
				self.firstInodeBlockNum = row[8]
			if row[0] == "DIRENT":
				dirent = direntSummary()
				dirent.parentInode = row[1]
				dirent.offset = row[2]
				dirent.fileInode = row[3]
				dirent.entryLen = row[4]
				dirent.nameLen = row[5]
				dirent.name = row[6]
				self.direntList.append(dirent)
			if row[0] == "INODE":
				inode = inodeSummary()
				inode.inodeNumber = int (row[1])
				inode.linkCount = int (row[6])
				self.allInodes.append(int (row[1]))

				# populate allocated inodes with inode
				self.allocatedInodes.append( int(row[1]) )
				# populate allocated blocks with inode direct pointers
				counter = 0 
				for item in row[12:24]: # slicing

					inode.blockPointers.append(int (item))
					if int(item) != 0:
						self.allBlocks.append(int(item))
						if int(item) <= 7 and int(item) > 0:
							print "RESERVED BLOCK %d IN INODE %d AT OFFSET %d" % (int(item),int(row[1]), int(counter))
						
						counter = int(counter) +1

						if int(item) >= int(self.numBlocks) or int(item) < 0:
							print "INVALID BLOCK %d IN INODE %d AT OFFSET 0" % (int(item), int(row[1]))
						else:
							self.allocatedBlocks.append( int(item))

				inode.blockPointers.append(int (row[24]))
				inode.blockPointers.append( int (row[25]))
				inode.blockPointers.append(int(row[26]))
				self.inodeList.append(inode)

				if int(row[24]) != 0:
					self.allBlocks.append( int(row[24]))
					if int(row[24]) <= 7 and int(row[24]) > 0: 
						print "RESERVED INDIRECT BLOCK %d IN INODE %d AT OFFSET 12" % (int(row[24]), int(row[1]))
					if int(row[24]) >= int(self.numBlocks) or int(item) < 0:
						print "INVALID INDIRECT BLOCK %d IN INODE %d AT OFFSET 12" % (int(row[24]), int(row[1]))
					else:
						self.allocatedBlocks.append( int(row[24]) )

				if int(row[25]) != 0:
					self.allBlocks.append( int(row[25]))
					if int(row[25]) <= 7 and int(row[25]) > 0: 
						print "RESERVED DOUBLE INDIRECT BLOCK %d IN INODE %d AT OFFSET 268" % (int(row[25]), int(row[1]))
					if int(row[25]) >= int(self.numBlocks) or int(item) < 0:
						print "INVALID DOUBLE INDIRECT BLOCK %d IN INODE %d AT OFFSET 268" % (int(row[25]), int(row[1]))
					else:
						self.allocatedBlocks.append( int(row[25]) )

				if int(row[26]) != 0:
					self.allBlocks.append( int(row[26]))
					if int(row[26]) <= 7 and int(row[26]) > 0: 
						print "RESERVED TRIPPLE INDIRECT BLOCK %d IN INODE %d AT OFFSET 65804" % (int(row[26]), int(row[1]))
					if int(row[26]) >= int(self.numBlocks) or int(item) < 0:
						print "INVALID TRIPPLE INDIRECT BLOCK %d IN INODE %d AT OFFSET 65804" % (int(row[26]), int(row[1]))
					else:
						self.allocatedBlocks.append( int(row[26]) )
						
				
			# populate allocated blocks list with referenced blockNum of INDIR block
			if row[0] == "INDIRECT":
				self.allInodes.append(int (row[1]))
				self.allBlocks.append( int (row[5]))
				indir = indirect()
				indir.inodeNumber =  int (row[1]) 
				indir.indirLevel = int (row[2])
				indir.blockOffset = int (row[3])
				indir.blockNumber = int (row[5])
				self.indirectList.append(indir)
				self.allocatedBlocks.append( int(row[5]))



		# populate reservedBlocks list with blocks reserved by the system
		for i in range(0, 8):
			self.reservedBlocks.append(i)
		# populate reservedInodes list with inodes reserved by the system
		for i in range(0, int(self.firstNonRsrvdInode)):
			self.reservedInodes.append(i)

	def printReservedBlocks(self):
		print self.reader
		for row in self.reader:
			print row
			if row[0] == "INODE":
				for item in row[12:24]:
					if item in self.reservedBlocks:
						print "RESERVED BLOCK %d IN INODE %d AT OFFSET 0" % (int(item), int(row[1]))

	def badRefCounts(self):
		for inode in self.inodeList:
			inodeExists = 0
			# print "inode number:%d\tlink count:%d" % ( int(inode.inodeNumber), int(inode.linkCount))
			direntReferences = 0
			for dirent in self.direntList:
				# print "dirent fileInode #:%d\tdirent parentInode #:%d" % ( int(dirent.fileInode), int(dirent.parentInode))
				if int(dirent.fileInode) == int(inode.inodeNumber):
					inodeExists = 1
					direntReferences += 1

			# print "hello inodeExists = %d\tand direntReferences = %d" % ( int(inodeExists), int(direntReferences))
			# if int(inodeExists) == 0:
			#	print "INODE %d HAS %d LINKS BUT LINKCOUNT IS %d" % (int(inode.inodeNumber), int(direntReferences), int(inode.linkCount))
			if (int(inodeExists) == 0) or (int(inode.linkCount) != int(direntReferences)):
				print "INODE %d HAS %d LINKS BUT LINKCOUNT IS %d" % ( int(inode.inodeNumber), int(direntReferences), int(inode.linkCount))

	def unallocInodes(self):
		for dirent in self.direntList:
			isAllocated = 0
			for inode in self.inodeList:
				if int(dirent.fileInode) == int(inode.inodeNumber):
					isAllocated = 1
			if int(dirent.fileInode) > int(self.numInodes):
				print "DIRECTORY INODE %d NAME %s INVALID INODE %d" % ( int(dirent.parentInode), dirent.name, int(dirent.fileInode) )
			elif int(isAllocated) == 0:
				print "DIRECTORY INODE %d NAME %s UNALLOCATED INODE %d" % ( int(dirent.parentInode), dirent.name, int(dirent.fileInode) )

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
	def testPrinter(self):
		# print self.inodeList[3].inodeNumber 
		# print "%d" % (len(self.indirectList))

		 for item in self.inodeList:
			print item

	def doubleDot(self):
		for item in self.direntList:
			childNode = 0
			FatherNode = 0   # From perspective of .. 
			if item.name == "'..'":
				#print "Name - %s, MyInode - %d ,Refer Inode - %d " % (item.name, int(item.parentInode) ,int(item.fileInode))
				childNode = item.parentInode
				FatherNode = item.fileInode
			else:
				continue

			for node in self.direntList: 
				if node.fileInode == childNode and node.parentInode != childNode: 
					# print "Name - %s, MyInode - %d ,Refer Inode - %d " % (node.name, int(node.parentInode) ,int(node.fileInode))
					if FatherNode != node.parentInode: 
					 	print "HIT"








				


	def singleDot(self): 
		for item in self.direntList:
			if item.name == "'.'":
				if(item.parentInode != item.fileInode):
					print "DIRECTORY INODE %d NAME '.' LINK TO INODE %d SHOULD BE %d" % (int (item.parentInode), int (item.fileInode),int (item.parentInode))
				

		#	SEXIEST FUNCTION IN THE HOUSE 
		#EVERYBODY GIVE IT UP FOR UDAYAN!!!!!!!!

	def printDuplicate(self):
			for item in self.inodeList: 
				count = 0
				for nBlock in item.blockPointers[0:12]: 
					if self.allBlocks.count(nBlock) > 1:
						print "DUPLICATE BLOCK %d IN INODE %d AT OFFSET %d" %  ( int(nBlock), int(item.inodeNumber), int(count))
						count = count + 1

			for item in self.inodeList: 
				nBlock = item.blockPointers[12]
				if self.allBlocks.count(nBlock) > 1:
					print "DUPLICATE INDIRECT BLOCK %d IN INODE %d AT OFFSET 12" %  (int(nBlock), int(item.inodeNumber))
						
			for item in self.inodeList: 
				nBlock = item.blockPointers[13]
				if self.allBlocks.count(nBlock) > 1:
					print "DUPLICATE DOUBLE INDIRECT BLOCK %d IN INODE %d AT OFFSET 268" %  (int(nBlock), int(item.inodeNumber))

			for item in self.inodeList: 
				nBlock = item.blockPointers[14]
				if self.allBlocks.count(nBlock) > 1:
					print "DUPLICATE TRIPPLE INDIRECT BLOCK %d IN INODE %d AT OFFSET 65804" %  (int(nBlock), int(item.inodeNumber))


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
	#FSA.testPrinter()
	FSA.printDuplicate()
	FSA.badRefCounts()
	FSA.unallocInodes()
	FSA.singleDot()
	FSA.doubleDot()

#	FSA.printReservedBlocks()
#	FSA.printContents()
	
