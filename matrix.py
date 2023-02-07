class matrix_t:
        def __init__(self,rows,cols,val=None,store_by_rows=True,row_del='\n',col_del='\t'):
                ''
                self._shape=(rows,cols)
                self._data=[]
                # modified params are stored in the following format
                #       storage-type;row-delimiter;col-delimiter
                self._params=[store_by_rows,row_del,col_del]
                for i in range(0,rows*cols):
                        self._data.append(val)

        def __len__(self):
                'Return number of elements, i.e. product of rows number and columns number'
                return self._shape[0]*self._shape[1]

        def __le__(self,m):
                ''
                if self._shape!=m._shape:
                        raise ValueError('Matrices are not compareable')
                return self._data<=m._data

        def __lt__(self,m):
                ''
                if self._shape!=m._shape:
                        raise ValueError('Matrices are not compareable')
                return self._data<m._data

        def __rmul__(self,c):
                'Multiplication on constant'
                size=len(self._data)
                self._data*=c

        def __isub__(self,m):
                ''
                if self._shape!=m._shape:
                        raise ValueError('Matrix has different shape')
                self._data-=m._data

        def __str__(self):
                ''
                result=str()
                row_del=self._params[1]
                col_del=self._params[2]
                rows=self._shape[0]
                cols=self._shape[1]
                for x in range(0,rows):
                        for y in range(0,cols):
                                buf='{}{}'.format(str(self.get(x,y)),col_del)
                                result+=buf
                        result+=row_del
                return result

        def from_array(self,data):
                'Initialization of matrix with the help of array like object'
                rows=self._shape[0]
                cols=self._shape[1]
                N=len(data)
                if N!=rows*cols:
                        raise ValueError('data is too small')
                # don't check data types
                self._data=data
                
        def set(self,x,y,val):
                ''
                idx=self.index(x,y)
                if idx==None:
                        return
                self._data[idx]=val

        def get(self,x,y):
                ''
                idx=self.index(x,y)
                if idx==None:
                        raise ValueError('Invalid indices')
                return self._data[idx]

        def rows(self):
                'Return number of rows'
                return self._shape[0]

        def cols(self):
                'Return number of columns'
                return self._shape[1]

        def row(self,index):
                'Return row with specified index as matrix'
                if self._shape[0]<=index:
                        return None
                num_cols=self._shape[1]
                result=matrix_t(1,num_cols)
                for y in range(0,num_cols):
                        result.set(0,y,self.get(index,y))
                return result

        def col(self,index):
                'Return column with specified index as matrix'
                if self._shape[1]<=index:
                        return None
                num_rows=self._shape[0]
                result=matrix_t(num_rows,1)
                for x in range(0,num_rows):
                        result.set(x,0,self.get(x,index))
                return result

        def index(self,x,y):
                'Return index of element for specified row and column'
                rows=self._shape[0]
                cols=self._shape[1]
                if rows<=x or cols<=y:
                        return None
                elif self._params[0]==True:
                        return x*cols+y
                else:
                        return y*rows+x

def add(m1,m2):
        'Addition of two matrices'
        if m1._shape!=m2._shape:
                raise ValueError('Matrices have different shapes')
        rows=m1.rows()
        cols=m1.cols()
        result=matrix_t(rows,cols)
        for x in range(0,rows):
                for y in range(0,cols):
                        result.set(x,y,m1.get(x,y)+m2.get(x,y))
        return result

def sub(m1,m2):
        'Subtraction of two matrices'
        if m1._shape!=m2._shape:
                raise ValueError('Matrices have different shapes')
        rows=m1.rows()
        cols=m1.cols()
        result=matrix_t(rows,cols)
        for x in range(0,rows):
                for y in range(0,cols):
                        result.set(x,y,m1.get(x,y)-m2.get(x,y))
        return result













