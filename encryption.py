import numpy as np
import time

IP = [3, 13, 4, 9,
      8, 5, 0, 1,
      7, 10, 12, 15, 
      14, 6, 11, 2]

FP = [15, 13, 14, 9,
      11, 5, 10, 1,
      13, 14, 12,10, 
      9, 1, 8, 0]

EBox = [8, 2, 4, 1,
        3, 2, 6, 1,
        7, 5, 3, 8]

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

F_PBox = [1, 7, 4, 3,
          0, 5, 2, 6]


def xor(left,xorstream):
    
    xorresult = np.logical_xor(left,xorstream)
    xorresult  = xorresult.astype(int)

    return xorresult

def E_box(right):
    expanded = np.empty(12)
    j = 0

    for i in EBox:
        expanded[j] = right[i - 1]
        j += 1

    expanded = list(map(int,expanded))
    expanded = np.array(expanded)
    
    return expanded

def sboxloopup(sinput,x):
    tableno = x - 1
    row = int((np.array2string(sinput[0]) + np.array2string(sinput[2])),2)

    column = sinput[1:2]
    column = np.array2string(column)
    column = column[1:2].replace(" ", "")
    column = int(column,2)

    elementno = (2 * row) + column
    soutput = SBox[tableno][elementno]
    soutput = list(np.binary_repr(soutput, width=2))
    return soutput

def sbox(sboxin):
    sboxin1 = sboxin[0:3]
    sboxout1 = sboxloopup(sboxin1, 1)
    sboxin2 = sboxin[3:6]
    sboxout2 = sboxloopup(sboxin2, 2)
    sboxin3 = sboxin[6:9]
    sboxout3 = sboxloopup(sboxin3, 3)
    sboxin4 = sboxin[9:12]
    sboxout4 = sboxloopup(sboxin4, 4)
    
    sboxout = np.concatenate([sboxout1,sboxout2,sboxout3,sboxout4])
    return sboxout

def f_permute(topermute):
    permuted= np.empty(8)
    j = 0
    for i in F_PBox:
        permuted[j] = topermute[i - 1]
        j += 1

    return permuted

def f_function(right,rkey):
    expanded = E_box(right)
    xored = xor(expanded,rkey)
    sboxed = sbox(xored)
    xorstream = f_permute(sboxed)

    return xorstream

def round(data,rkey):
    l0 = data[0:8]
    r0 = data[8:16]

    xorstream = f_function(r0,rkey)

    r1 = xor(l0,xorstream)
    l1 = r0

    returndata = np.empty_like(data)
    returndata[0:8] = l1
    returndata[8:16] = r1
    return(returndata)

def permutation(data,x):
    permute1 = np.empty_like(IP)
    if x == 0:
        j = 0
        for i in IP:
            permute1[j] = data[i-1]
            j += 1
        return(permute1)
    else:
        permute2 = np.empty_like(FP)
        k = 0
        for l in FP:
            permute2[k] = data[l-1]
            k += 1
        return(permute2)

def main():
    key = ['1', '0', '1', '1', '0', '1', '1', '0', '0', '0', '1', '0']
    #data = ['1', '1', '1', '1', '1', '1', '1', '0', '0', '1', '1', '1', '0', '0', '0', '1']
    data = ['1', '0', '1', '1', '1', '1', '1', '1', '0', '1', '0', '1', '1', '1', '1', '1']

    rkey = list(map(int, key))
    print(data,rkey)

    operate = int(input("Choose 0 for encryption or Choose 1 for decryption "))
    starttime = time.time()

    if operate == 0:
        data = permutation(data,0)
        data = round(data,rkey)
                
        data = np.roll(data,8)
        data = (permutation(data, 1))
        print("Time taken to encrypt the data with DES is", time.time() - starttime)
        print("Encrypted data is", data)

    if operate == 1:
        data = permutation(data, 0)
        data = round(data, rkey)

        data = np.roll(data, 8)
        data = (permutation(data, 1))
        print("Time taken to decrypt the data with DES is", time.time() - starttime)
        print("Decrypted data is", data)

main()