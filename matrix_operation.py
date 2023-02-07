#{
#"created":"2021-02-22",
#"type":"Python module",
#"part of":"math package",
#"desc":"This module contains matrix operations as external procedures"
#}
import math
# Create matrix from iterable object.
def from_iter(source,shape_,int_=False,float_=False):
    ''
    if len(source)!=shape_[0]*shape_[1]:
        raise ValueError('matrix_op.from_iter: the length of source and target shape are mismatch')
    m=[[] for i in range(shape_[0])]
    count=0
    it=iter(source)
    while True:
        try:
            val=next(it)
            t=divmod(count,shape_[1])
            try:
            # change data format (if required)
                if int_==True:
                    val=int(val)
                elif float_==True:
                    val=float(val)
                else:
                    # format is unchanged
                    pass
            except ValueError as e:
                # value can't be casted to specified type
                pass
            m[t[0]].append(val)
            count+=1
        except StopIteration as e:
            return m
        
# Return shape of specified matrix
def shape(m):
    ''
    num_rows=len(m)
    if num_rows==0:
        return (0,0)
    num_cols=len(m[0])
    # all rows MUST have the same length
    for i in range(1,num_rows):
        if len(m[i])!=num_cols:
            raise ValueError('matrix_op.shape: Invalid shape')
    return (num_rows,num_cols)

# Return matrix with new specified shape. Returned matrix has 'list-of-list' type
def reshape(m,shape_new):
    ''
    shape_old=shape(m)
    if (shape_old[0]*shape_old[1])!=(shape_new[0]*shape_new[1]):
        raise ValueError('matrix_op::reshape: new shape MUST have the same volume')
    res=[[] for i in range(shape_new[0])]
    volume=shape_new[0]*shape_new[1]
    for count in range(volume):
        coord_old=divmod(count,shape_old[0])
        coord_new=divmod(count,shape_new[0])
        assert len(res[coord_new[0]])<(shape_new[1]-1)
        res[coord_new[0]].append(m[coord_old[0]][coord_old[1]])
    return res
        

# Remove specified columns from the matrix. Each deleted column is returned as
# matrix (list-of-list) with the single raw. Also, new matrix without deleted
# columns is returned. This matrix has 'list-of-list' type.
# @param src - input matrix
# @param cols_set (set-of-int) - indices of columns to delete
def remove_cols(src,cols_set):
    ''
    s=shape(src)
    cols_list=[]
    # convert column indices to 'list-of-int'
    for val in cols_set:
        if val<0 or s[1]<=val:
            raise ValueError('matrix_op.remove_cols: invalid column index')
        cols_list.append(val)
    # order list of indices
    cols_list.sort()
    num_cols_to_del=len(cols_list)
    cols=[[] for i in range(num_cols_to_del)]
    dst=[[] for i in range(s[0])]
    for i in range(s[0]):
        for j in range(s[1]):
            try:
                # current column should be deleted from the source
                idx=cols_list.index(j)
                cols[idx].append(src[i][j])
            except ValueError as e:
                # current column should not be deleted from the source
                dst[i].append(src[i][j])
    return dst,cols

# Return dict. where keys are columns indices and values are columns (list).
# @param m - source matrix
# cols_set (set-of-int) - indices of required columns
def cols(m,cols_set):
    ''
    result={idx:[] for idx in cols_set}
    s=shape(m)
    i=0
    while i<s[0]:
        for idx in result:
            if idx<0 or s[1]<=idx:
                # ignore invalid column index
                continue
            result[idx].append(m[i][idx])
        # next
        i+=1
    return result

# math operations
def add(m1,m2):
    'Addition'
    s=shape(m1)
    if s!=shape(m2):
        raise ValueError('matrix_op.add: Shapes are different')
    return [[m1[i][j]+m2[i][j] for j in range(s[1])] for i in range(s[0])]

def mul(m1,m2):
    'Multiplication'
    s1=shape(m1)
    s2=shape(m2)
    if s1[1]!=s2[0]:
        raise ValueError('matrix_op.mul: Number of columns and number of rows are different')
    result=[]
    for i in range(s1[0]):
        result.append([0 for k in range(s2[0])])
        for j in range(s2[1]):
            for k in range(s1[1]):
                result[i][j]+=m1[i][k]*m2[k][j]
    return result

def mul_const(m,c):
    'Multiplication on constant'
    s=shape(m)
    return [[c*m[i][j] for j in range(s[1])] for i in range(s[0])]
        
def sub(m1,m2):
    'Subtraction'
    return add(m1,mul_const(m2,-1))
