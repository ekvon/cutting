import local.matrix
from local.matrix import matrix_t
import local.matrix_operation as op
# global variables
# nonbasic variables indices
N=[]
# basic variables indices
B=[]
# base matrix
A=None
# free variables
b=None
# target function constants
c=None
# optional constant in target function
v=0
#
debug_level=0
# initialization
# @param A_ - list of coeff. of base matrix.
# @param b_ - list of free variables
# @param c_ - list of coeff. of target function
# The shape of the matrix is defined with the help of number of free variables
# (number of rows) and number of coeff. of target function (number of columns).
# If
#   m=len(b_) and n=len(c_)
# then the number of rows in matrix is n+m and number of columns is n+m.
# This is the result of 'm' additional variables are introduced. At the start time
# all introduced variables (their indices) are basic variables and initial variables
# are non-basic variables. At that
#   len(A_)=m*n
# and it's assumed that coeff. are stored in list by rows.
def INITIALIZE_SIMPLEX(A_,b_,c_):
    ''
    global N,B,A,b,c,v
    n=len(c_)
    m=len(b_)
    assert len(A_)==(n*m)
    b=matrix_t(n+m,1,0)
    # number of equations in extended system is n+m
    for i in range(0,n+m):
        if i<n:
            b.set(i,0,0)
        else:
            # check free variable
            # print('i={};m={}'.format(i,m))
            assert b_[i-n]>=0
            b.set(i,0,b_[i-n])
            # index of basic variable
            B.append(i)
    if debug_level!=0:
        print('B={}\n'.format(B))
    # number of variables in extended system is n+m
    c=matrix_t(1,n+m,0)
    for i in range(0,n+m):
        if i<n:
            # check coeff.
            c.set(0,i,c_[i])
            # index of non-basic variable
            N.append(i)
        else:
            # coeff. for introduced variables
            c.set(0,i,0)
    if debug_level!=0:
        print('N={}\n'.format(N))
    # extended matrix has the following shape: (n+m) x (n+m)
    A=matrix_t(n+m,n+m,0)
    for i in range(0,n+m):
        for j in range(0,n+m):
            if i<n:
                # At the start time initial variables are not defined
                # with the help of introduced variables.
                A.set(i,j,0)
            elif j<n:
                # Introduced variables are expressed through initial variables.
                idx=(i-n)*n+j
                # print('i={};j={};idx={}'.format(i,j,idx))
                A.set(i,j,A_[idx])
            elif (j-n)==(i-n):
                # If 'i' in range(m,m+m) then the following equation has taken a place:
                #   a[i][0]*x[0]+...+a[i][n-1]*x[n-1]+0*x[n]+...+(-1)*x[i]+...+0*x[n+m-1]=b[i]
                A.set(i,j,1)
            else:
                A.set(i,j,0)
    if debug_level!=0:
        print('A={}\nb={}\nc={}\n'.format(A,b,c))

# @param l - Index of leaving variable. It must be presented in 'B'
# @param e - Index of entering variable. It must be presented in 'N'
def PIVOT(l,e):
    'Calculation parameters for new basis variable'
    global N,B,A,b,c,v
    if l not in B or e not in N:
        if debug_level!=0:
            print('B={}\nN={}\nl={}\ne={}'.format(B,N,l,e))
        raise ValueError('Invalid variable indices')
    d_=A.get(l,e)
    if d_==0:
        raise ValueError('Zero division')
    m=len(B)
    n=len(N)
    assert (m+n)==c.cols()
    assert (m+n)==b.rows()
    # new canonical form
    b_=matrix_t(n+m,1,0)
    c_=matrix_t(1,m+n,0)
    A_=matrix_t(n+m,m+n,0)
    # free variable for entering variable
    b_.set(e,0,b.get(l,0)/d_)
    # coeff. for entering variable
    for j in N:
        if j==e:
            continue
        A_.set(e,j,A.get(l,j)/d_)
    A_.set(e,l,1/d_)
    # coeff. for other variables, i.e. for variables which indices belong
    # to the set 'B\{l}'.
    for i in B:
        if i==l:
            continue
        # At the present time b_[e][0]=b[l][0]/A[l][e] (see above)
        b_.set(i,0,b.get(i,0)-A.get(i,e)*b_.get(e,0))
        for j in N:
            if j==e:
                continue
            # at the present time A_[e][j]=A[l][j]/A[l][e] (see above)
            A_.set(i,j,A.get(i,j)-A.get(i,e)*A_.get(e,j))
        A_.set(i,l,-A.get(i,e)/A.get(l,e))
    # target function
    v_=v+c.get(0,e)*b_.get(e,0)
    for j in N:
        if j==e:
            continue
        c_.set(0,j,c.get(0,j)-c.get(0,e)*A.get(l,j)/A.get(l,e))
    c_.set(0,l,-c.get(0,e)*1/A.get(l,e))
    # new sets of basic and non-basic variables
    N.pop(N.index(e))
    N.append(l)
    B.pop(B.index(l))
    B.append(e)
    A=A_
    b=b_
    c=c_
    v=v_
    if debug_level!=0:
        print('A={}\nb={}\nc={}\nv={}\n'.format(A,b,c,v))
    return

def SIMPLEX():
    ''
    global N,B,A,b,c,v,debug_level
    m=len(B)
    n=len(N)
    result=[]
    while True:
        e=None
        for i in N:
            # select index 'e' from N for which 0<c[e]
            if 0<c.get(0,i):
                e=i
                break
        if e==None:
            break
        # select leaving variable
        min_val=-1
        l=None
        for i in B:
            if 0<A.get(i,e):
                val=b.get(i,0)/A.get(i,e)
                if l==None or val<min_val:
                    l=i
                    min_val=val
                else:pass
            else:pass
        if l==None:
            # pivot element is not detected
            return ('Task is unbounded',result)
        else:
            if debug_level!=0:
                print('SIMPLEX: entering variable-{};leaving variable-{}'.format(e,l))
            PIVOT(l,e)

def SOLUTION():
    ''
    global N,B,A,b,c,v,debug_level
    # dimension of initial task
    dim=len(N)
    # dimension of inverse task
    dim_inv=len(B)
    # solution of initial task
    x=matrix_t(dim,1,0)
    # solution of inverse task
    y=matrix_t(1,dim_inv,0)
    for idx in B:
        if idx<dim:
            x.set(idx,0,b.get(idx,0))
    for idx in N:
        if dim<=idx:
            y.set(0,idx-dim,-c.get(0,idx-dim))
    return x,y
        
def clear():
    ''
    global N,B,A,b,c,v,debug_level
    N.clear()
    B.clear()
    A=None
    b=None
    c=None
    v=0
    debug_level=0
    
