import math
from local import simplex
from local import matrix
from local import matrix_operation as operation
from local.matrix import matrix_t
# number of products type
NUM_PRODUCTS=4
# number of cutting ways
NUM_CUTTING_WAYS=6
# matrix that defines five variants of cutting
a_=[3,0,0,0,1,1,0,0,1,0,1,0,0,2,0,0,0,1,1,0,0,0,0,1]
# vector of not used material for each variant of cutting
c_1=[0.9,1.6,1.0,0.6,0,0.6]
# vector of target function coef. for optimization of number of used 
c_2=[1,1,1,1,1,1]
# vector of demand on four type of products
n_=[]
# vector of solutions
x_=[]
# length of four type of products
l_=[1.7,2.7,3.3,5.4]
if __name__=='__main__':
        import sys
        simplex.clear()
        # default coef. of target function
        c_=c_2
        # the first argument of demand in cmd-line
        demand_start=-1
        argc=len(sys.argv)
        # parse command line
        if argc<5:
                # minimum number of arguments
                print('usage: cutting [-o1|-d] n_0 n_1 n_2 n_3, where')
                print('\t-o1 is optimization by number of used ... (optional)')
                print('\t-d set debug mode (optional)')
                print('\tn_i is demand on product of type i (mandatory)')
                sys.exit()
        i=1
        while i<argc:
                if sys.argv[i]=='-o1':
                        c_=c_1
                        # next
                        i+=1
                        continue
                elif sys.argv[i]=='-d':
                        simplex.debug_level=1
                        # next
                        i+=1
                        continue
                else:
                        # it's assumed that vector of demand start from this position
                        demand_start=i
                        break
        if demand_start<0:
                print('demand vector is not specified')
                sys.exit()
        # initialize demand vector
        n_.clear()
        for i in range(demand_start,demand_start+4):
                n_.append(int(sys.argv[i]))
        simplex.INITIALIZE_SIMPLEX(a_,c_,n_)
        simplex.SIMPLEX()
        # dimension of task
        I=NUM_CUTTING_WAYS
        J=NUM_PRODUCTS
        if len(simplex.c)!=(I+J):
                print('invalid length {}'.format(len(simplex.c)))
                sys.exit()
        for i in range(I):
                if J+i in simplex.N:
                        x_.append(math.ceil(-simplex.c.get(0,J+i)))
                else:
                        x_.append(0)
                        
        # show result
        A=operation.from_iter(a_,(I,J),int_=True)
        x=operation.from_iter(x_,(1,I),int_=True)
        N=operation.mul(x,A)
        total=sum(x_)
        total_in_metres=total*6

        print('total used logs: {}'.format(total))
        print('total used logs (m): {}'.format(total*6))
        print('used cutting methods: {} {} {} {} {} {}'.format(x_[0],x_[1],x_[2],x_[3],x_[4],x_[5]))
        print('output (by type): {} {} {} {}'.format(N[0][0],N[0][1],N[0][2],N[0][3]))
        
        unused_products=[N[0][i]-n_[i] for i in range(NUM_PRODUCTS)]
        print('unused output (by type): {} {} {} {}'.format(
                unused_products[0],
                unused_products[1],
                unused_products[2],
                unused_products[3]))
        unused_products_in_metres=0
        for i in range(NUM_PRODUCTS):
                unused_products_in_metres+=unused_products[i]*l_[i]
        # in metres
        unused_remains=0
        for i in range(NUM_CUTTING_WAYS):
                unused_remains+=x_[i]*c_1[i]
        print('unused output (m): {}'.format(unused_products_in_metres))
        print('unused output (%): {}'.format(unused_products_in_metres/(total_in_metres)*100))
        print('unused remains (m): {}'.format(unused_remains))
        print('unused remains (%): {}'.format(unused_remains/total_in_metres*100))
        print('unused total (m): {}'.format(unused_remains+unused_products_in_metres))
        print('unused total (%): {}'.format((unused_remains+unused_products_in_metres)/total_in_metres*100))
	
