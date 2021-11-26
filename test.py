import numpy as np

SBox =[
		# S1
		[0, 3, 
         1, 1,  
         0, 2,
         1, 2],

		# S2
		[1, 3, 
         1, 2,  
         0, 0,
         0, 3],

		# S3
		[0, 2, 
         3, 0,  
         0, 1],

		# S4
		[3, 3, 
         1, 0,  
         1, 2,
         0, 2],
	]

sinput = np.array([0,1,0])
tableno = 1 - 1
row = int((np.array2string(sinput[0]) + np.array2string(sinput[2])),2)

column = sinput[1:2]
column = np.array2string(column)
column = column[1:2].replace(" ", "")
column = int(column,2)

elementno = (2 * row) + column
soutput = SBox[tableno][elementno]
soutput = list(np.binary_repr(soutput, width=2))

print(soutput)