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





def main(argv):
	try:
		f = open(argv, 'r')
	except IOError:
		print "Could not read file:", f
		sys.exit(1)
	


if __name__ == "__main__":
	main(sys.argv[1])	
