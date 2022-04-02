
from types import FunctionType, MethodType
import copy

class Meta(type):

	def __new__(meta, classname, bases, classDict):
		for name, entry in classDict.items():
			if isinstance(entry, (FunctionType, MethodType)):
				classDict[name] = staticmethod(entry)
		return type.__new__(meta, classname, bases, classDict)

	def __get__(self, instance, owner):
		return self.get(instance)

	def __set__(self, instance, value):
		return self.set(instance, value)

class Property(object):
	__metaclass__ = Meta

class Sudoku(object):
	def __init__(self,mat):
		self._mat = mat
		
	class mat(Property):
		def get(owner):
			return owner._mat
			
	class row(Property):
		def get(owner):
			row = [i for i in owner._mat]
			return row
			
	class col(Property):
		def get(owner):
			col = [[r[c] for r in owner._mat] for c in range(9)]
			return col
			
	class block(Property):
		def get(owner):
			blocks = []
			for r in range(3):
				for c in range(3):
					b = [[vj for kj,vj in enumerate(vi) if kj in range(3*c,3*(c+1))] for ki,vi in enumerate(owner._mat) if ki in range(3*r,3*(r+1))]
					bo = []
					for bi in b:
						bo += bi
					blocks.append(bo)
			return blocks
			
	def setItem(self,row,col,val):
		self._mat[row][col] = val
	
	def solve(self):
		defset = set(range(1,10))
		minpos = 9
		finished = True
		for r in range(9):
			for c in range(9):
				if self._mat[r][c]:
					continue
				else:
					finished = False
					b = 3 * (r//3) + (c//3)
					posval = defset.difference(self.row[r]).difference(self.col[c]).difference(self.block[b])

					if len(posval)==0:
						raise ValueError("Not Solvable")
					elif len(posval)<=minpos:
						minpos = len(posval)
						bestval = posval
						min_r = r
						min_c = c
		if finished:
			return self
		else:
			for n in bestval:
				s = Sudoku(copy.deepcopy(self._mat))
				s.setItem(min_r, min_c, n)
				try:
					soln = s.solve()
					break
				except ValueError:
					soln = None
			if soln is None:
				raise ValueError('Not Solvable')
			return soln
			
	def __repr__(self):
		out = ''
		for i in range(9):
			if i % 3 == 0:
				out += '+-------+-------+-------+\n'
			for j in range(9):
				if j % 3 == 0:
					out += '| '
				v = self._mat[i][j]
				if v is not None:
					out += '%1d ' % v
				else:
					out +=  '  '
			out += '|\n'
		out += '+-------+-------+-------+\n'
		return out
	

def main(m):
	s = Sudoku(m)
	print(s)
	print("")
	print("result")
	try:
		print(s.solve())
	except ValueError as e:
		print(e)



	
N = None
easy = [
    [7, N, N,   1, 5, N,   N, N, 8],
    [N, N, 4,   N, N, 2,   N, N, N],
    [N, N, N,   N, N, 4,   5, 6, N],

    [6, N, N,   N, N, N,   N, 2, 9],
    [5, N, 2,   N, N, N,   8, N, 4],
    [3, 4, N,   N, N, N,   N, N, 1],

    [N, 3, 8,   6, N, N,   N, N, N],
    [N, N, N,   2, N, N,   9, N, N],
    [1, N, N,   N, 8, N,   N, N, 3]
    ]
	
hard = [
    [N, 4, N,   N, N, 7,   9, N, N],
    [N, N, 8,   5, 3, 9,   N, N, N],
    [N, 6, N,   N, N, N,   2, N, 3],

    [N, N, N,   N, N, 2,   5, N, N],
    [N, 8, 6,   N, N, N,   1, 4, N],
    [N, N, 9,   8, N, N,   N, N, N],

    [6, N, 3,   N, N, N,   N, 9, N],
    [N, N, N,   9, 8, 6,   3, N, N],
    [N, N, 1,   4, N, N,   N, 6, N]
    ]


evil = [
    [4, 2, N,   N, N, N,   N, 1, N],
    [N, N, N,   5, 4, N,   N, 3, N],
    [N, N, 6,   N, N, 7,   N, N, N],

    [N, N, N,   N, N, N,   2, 7, 9],
    [N, 1, N,   N, N, N,   N, 6, N],
    [3, 4, 2,   N, N, N,   N, N, N],

    [N, N, N,   9, N, N,   3, N, N],
    [N, 6, N,   N, 3, 8,   N, N, N],
    [N, 8, N,   N, N, N,   N, 5, 7]
    ]
	
empt = [
    [N, N, N,   N, N, N,   N, N, N],
    [N, N, N,   N, N, N,   N, N, N],
    [N, N, N,   N, N, N,   N, N, N],

    [N, N, N,   N, N, N,   N, N, N],
    [N, N, N,   N, N, N,   N, N, N],
    [N, N, N,   N, N, N,   N, N, N],

    [N, N, N,   N, N, N,   N, N, N],
    [N, N, N,   N, N, N,   N, N, N],
    [N, N, N,   N, N, N,   N, N, N]
    ]

rp20100821a = [
    [6, 7, 1,   N, N, 2,   N, N, 3],
    [9, N, N,   5, N, N,   4, N, N],
    [2, N, 5,   9, N, N,   N, 1, N],

    [N, 9, 6,   N, 2, N,   N, N, 1],
    [4, N, N,   6, N, 7,   N, N, 2],
    [3, N, N,   N, 4, N,   9, 7, N],

    [N, 3, N,   N, N, 8,   7, N, 4],
    [N, N, 4,   N, N, 9,   N, N, 5],
    [5, N, N,   1, N, N,   2, 8, 9]
    ]

rp20100821b = [
    [N, N, N,   8, 2, 1,   N, 3, N],
    [N, N, N,   9, N, N,   N, 2, 7],
    [N, N, N,   N, N, 4,   6, N, N],

    [1, 4, N,   N, N, N,   3, N, 8],
    [5, N, N,   N, N, N,   N, N, 9],
    [2, N, 8,   N, N, N,   N, 7, 6],

    [N, N, 7,   5, N, N,   N, N, N],
    [4, 5, N,   N, N, 2,   N, N, N],
    [N, 9, N,   3, 4, 8,   N, N, N]
    ]

rp20100821c = [
    [N, N, 9,   1, N, 4,   6, N, N],
    [N, N, 2,   N, 7, N,   9, N, N],
    [3, N, N,   N, N, N,   N, N, 2],

    [N, 2, N,   N, 3, N,   N, 4, N],
    [N, N, N,   5, N, 8,   N, N, N],
    [N, 6, N,   N, 1, N,   N, 7, N],

    [7, N, N,   N, N, N,   N, N, 5],
    [N, N, 4,   N, 5, N,   8, N, N],
    [N, N, 6,   8, N, 3,   1, N, N]
    ]
rp20101009c = [
    [N, N, 3,   N, N, N,   1, N, N],
    [2, N, N,   N, N, N,   N, N, 4],
    [N, 8, N,   N, 9, N,   N, 2, N],

    [N, 1, N,   9, N, 5,   N, 4, N],
    [7, N, N,   2, N, 8,   N, N, 1],
    [N, 4, N,   6, N, 7,   N, 8, N],

    [N, 2, N,   N, 5, N,   N, 3, N],
    [4, N, N,   N, N, N,   N, N, 8],
    [N, N, 9,   N, N, N,   7, N, N]
    ]
	
rp20120310c = [
    [N, 2, 6,   4, N, N,   N, 3, N],
    [7, N, N,   N, N, N,   4, N, N],
    [N, 9, N,   5, 3, N,   2, N, N],

    [N, N, N,   N, N, N,   N, 4, 8],
    [N, N, N,   7, N, 1,   N, N, N],
    [1, 3, N,   N, N, N,   N, N, N],

    [N, N, 8,   N, 4, 2,   N, 7, N],
    [N, N, 9,   N, N, N,   N, N, 4],
    [N, 7, N,   N, N, 6,   9, 2, N]
    ]
	
rp20120317c = [
    [N, 1, 7,   N, 8, N,   9, N, N],
    [N, N, N,   N, N, 3,   N, N, 5],
    [N, N, N,   N, N, N,   2, 7, N],

    [N, N, N,   N, N, 7,   3, 8, N],
    [N, 4, N,   N, N, N,   N, 2, N],
    [N, 5, 6,   2, N, N,   N, N, N],

    [N, 2, 9,   N, N, N,   N, N, N],
    [4, N, N,   6, N, N,   N, N, N],
    [N, N, 8,   N, 7, N,   1, 4, N]
    ]
	
rp20120331c = [
    [N, 6, 8,   N, 5, N,   N, N, N],
    [N, 2, 4,   N, N, N,   N, N, N],
    [3, N, N,   N, N, 7,   N, 9, N],

    [6, N, N,   N, N, N,   N, N, N],
    [N, N, 1,   2, 4, 3,   7, N, N],
    [N, N, N,   N, N, N,   N, N, 8],

    [N, 5, N,   6, N, N,   N, N, 9],
    [N, N, N,   N, N, N,   3, 8, N],
    [N, N, N,   N, 2, N,   6, 1, N]
    ]
	
nov20120629x = [
    [8, N, N,   N, N, N,   N, N, N],
    [N, N, 3,   6, N, N,   N, N, N],
    [N, 7, N,   N, 9, N,   2, N, N],

    [N, 5, N,   N, N, 7,   N, N, N],
    [N, N, N,   N, 4, 5,   7, N, N],
    [N, N, N,   1, N, N,   N, 3, N],

    [N, N, 1,   N, N, N,   N, 6, 8],
    [N, N, 8,   5, N, N,   N, 1, N],
    [N, 9, N,   N, N, N,   4, N, N]
    ]
	
rp20120722 = [
    [N, 3, N,   N, 1, N,   N, N, 7],
    [N, N, N,   8, N, 5,   1, N, N],
    [N, N, N,   N, N, N,   N, 4, N],

    [N, 5, N,   7, N, N,   4, 1, 8],
    [N, N, N,   N, N, N,   N, N, N],
    [1, 7, 3,   N, N, 9,   N, 6, N],

    [N, 8, N,   N, N, N,   N, N, N],
    [N, N, 9,   5, N, 8,   N, N, N],
    [4, N, N,   N, 7, N,   N, 3, N]
    ]
	
rp20120804 = [
    [N, N, 9,   4, N, N,   N, N, N],
    [N, N, 4,   N, N, N,   N, N, 3],
    [N, 5, N,   N, 2, 3,   4, 6, N],

    [N, 1, N,   5, N, N,   8, 4, N],
    [N, N, N,   N, N, N,   3, N, N],
    [N, 8, 3,   N, N, 2,   6, 1, N],

    [N, 2, 1,   7, 6, N,   N, 3, N],
    [3, N, N,   2, N, N,   1, N, N],
    [N, N, N,   3, 1, 4,   7, N, N]
    ]
	
rp20121013 = [
    [9, N, N,   N, N, N,   N, N, N],
    [N, N, N,   7, N, N,   5, N, 2],
    [N, N, N,   6, 9, N,   3, 7, N],

    [N, 3, 8,   N, N, 4,   N, N, N],
    [N, 4, N,   N, N, N,   N, 5, N],
    [N, N, N,   2, N, N,   4, 1, N],

    [N, 6, 5,   N, 7, 3,   N, N, N],
    [2, N, 1,   N, N, 9,   N, N, N],
    [N, N, N,   N, N, N,   N, N, 1]
    ]
    
rp20121124 = [
    [N, N, N,   1, N, 8,   N, N, 5],
    [N, N, N,   2, N, N,   7, N, 1],
    [N, N, 3,   N, N, N,   N, N, 9],

    [3, N, N,   N, N, 6,   N, 1, N],
    [N, N, 5,   N, 7, N,   4, N, N],
    [N, 4, N,   8, N, N,   N, N, 6],

    [4, N, N,   N, N, N,   1, N, N],
    [9, N, 8,   N, N, 2,   N, N, N],
    [7, N, N,   9, N, 5,   N, N, N]
    ]
	
rp20130420 = [
    [5, 9, N,   3, N, N,   8, N, N],
    [N, N, N,   N, 7, N,   N, 6, N],
    [N, N, N,   4, N, N,   N, 3, N],

    [4, N, N,   N, 3, N,   6, N, N],
    [2, N, N,   N, N, N,   5, 4, N],
    [N, N, 1,   N, N, N,   N, N, 2],

    [N, N, N,   2, N, N,   N, N, 7],
    [N, N, 5,   N, N, 4,   N, N, N],
    [9, N, N,   8, N, 5,   N, N, N]
    ]
    
rp20140301 = [
    [N, N, N,   N, N, 9,   N, 6, 3],
    [N, N, N,   N, 1, N,   N, N, N],
    [N, 2, N,   3, N, 7,   N, 8, N],

    [N, N, 6,   5, 3, N,   N, N, N],
    [N, N, N,   N, N, N,   N, 7, N],
    [N, 4, N,   2, N, N,   N, N, 6],

    [N, N, 8,   N, N, N,   N, N, 5],
    [9, N, N,   N, 5, N,   4, N, N],
    [N, 7, 2,   N, N, N,   N, 9, N]
    ]
    
rp20140524 = [
    [7, N, N,   N, 4, N,   N, 3, N],
    [N, 6, N,   N, N, N,   N, N, N],
    [N, N, N,   N, N, 2,   5, N, N],

    [N, N, 8,   N, 2, N,   N, 5, N],
    [N, 1, N,   N, 7, N,   6, N, 3],
    [4, N, N,   8, N, N,   N, N, N],

    [N, N, N,   N, 3, 5,   1, N, 4],
    [N, N, N,   N, N, N,   N, N, 9],
    [N, N, 9,   N, N, 1,   N, N, N]
    ]
    
rp20140727 = [
    [N, N, 9,   7, N, N,   N, 8, 2],
    [N, 7, 4,   N, N, N,   9, N, N],
    [N, N, N,   N, N, N,   N, N, 1],

    [4, N, N,   N, 3, N,   N, N, N],
    [N, 3, N,   N, N, N,   N, 6, 9],
    [N, 1, N,   6, 2, N,   N, N, N],

    [N, N, N,   N, N, N,   N, N, N],
    [7, N, N,   N, N, 1,   8, N, N],
    [8, 5, N,   N, N, N,   3, 1, N]
    ]

rp20140830 = [
    [N, N, N,   N, 4, N,   2, N, 1],
    [N, N, 5,   N, 6, N,   3, N, N],
    [4, N, N,   N, N, N,   N, N, N],

    [N, 8, 9,   7, N, 1,   N, 6, N],
    [6, 2, N,   N, N, N,   N, N, N],
    [N, N, N,   8, N, N,   N, N, 3],

    [9, N, N,   N, 8, N,   N, N, N],
    [N, N, 1,   9, N, 7,   N, N, N],
    [N, N, N,   N, N, N,   N, 8, 5]
    ]
    
rp20150125 = [
    [9, N, N,   2, N, N,   6, N, N],
    [N, N, N,   4, N, N,   5, 2, N],
    [N, N, 4,   1, 5, N,   N, N, N],

    [N, 2, N,   N, N, N,   N, 6, 7],
    [8, N, N,   N, N, N,   N, N, N],
    [N, N, N,   N, N, 7,   9, N, N],

    [N, N, 5,   9, N, 4,   3, N, N],
    [3, N, N,   N, N, N,   N, 1, N],
    [N, 6, N,   N, N, N,   N, N, 8]
    ]

tv20170108 = [
    [N, 6, N,   N, N, 5,   8, N, 4],
    [2, 7, N,   6, 9, N,   N, N, N],
    [N, 4, N,   8, N, N,   N, N, N],

    [N, N, N,   N, N, N,   5, N, 8],
    [N, 5, 6,   N, 4, N,   3, 1, N],
    [8, N, 9,   N, N, N,   N, N, N],

    [N, N, N,   N, N, 6,   N, 5, N],
    [N, N, N,   N, 3, 9,   N, 8, 7],
    [6, N, 1,   5, N, N,   N, 2, N]
    ]
    
test1 = [
    [1, 2, 3,   N, N, N,   N, N, N],
    [4, 5, 6,   N, N, N,   N, N, N],
    [7, 8, 9,   N, N, N,   N, N, N],

    [N, N, N,   1, 2, 3,   N, N, N],
    [N, N, N,   4, 5, 6,   N, N, N],
    [N, N, N,   7, 8, 9,   N, N, N],

    [N, N, N,   N, N, N,   N, N, N],
    [N, N, N,   N, N, N,   N, N, N],
    [N, N, N,   N, N, N,   N, N, N]
    ]

if __name__=="__main__":
    main(test1)


