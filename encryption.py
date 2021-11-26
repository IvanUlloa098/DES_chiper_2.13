import numpy as np

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
		[0, 3, 
         1, 1,  
         0, 2,
         1, 2],

		[1, 3, 
         1, 2,  
         0, 0,
         0, 3],

		[0, 2, 
         3, 0,  
         0, 1],

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

def substitution(sinput,x):
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

def sbox(sbox_in_):
    sbox_in_1 = sbox_in_[0:3]
    sbox_out_1 = substitution(sbox_in_1, 1)
    sbox_in_2 = sbox_in_[3:6]
    sbox_out_2 = substitution(sbox_in_2, 1)
    sbox_in_3 = sbox_in_[6:9]
    sbox_out_3 = substitution(sbox_in_3, 1)
    sbox_in_4 = sbox_in_[9:12]
    sbox_out_4 = substitution(sbox_in_4, 1)
    
    sbox_result = np.concatenate([sbox_out_1,sbox_out_2,sbox_out_3,sbox_out_4])
    return sbox_result

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

def des_encryption(data,rkey):
    l0 = data[0:8]
    r0 = data[8:16]

    xorstream = f_function(r0,rkey)

    r1 = xor(l0,xorstream)
    l1 = r0

    result = np.empty_like(data)
    result[0:8] = l1
    result[8:16] = r1
    return(result)

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
    data = ['1', '1', '1', '1', '1', '1', '1', '0', '0', '1', '1', '1', '0', '0', '0', '1']
    #data = ['1', '0', '1', '1', '1', '1', '1', '1', '0', '1', '0', '1', '1', '1', '0', '1']

    rkey = list(map(int, key))
    print(data,rkey)

    option = int(input("0 encriptar, 1 desencriptar >>"))

    data = permutation(data,0)
    data = des_encryption(data,rkey)
            
    data = np.roll(data,8)
    data = (permutation(data, 1))

    if option == 0:
        print("Los datos encriptados son ", data)

    if option == 1:
        print("Los datos desencriptados son ", data)

main()