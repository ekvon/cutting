import re
def read_txt(path):
        'Read input data from text file with the help of regular expression'
        # output arrays
        x1=[]
        x2=[]
        y1=[]
        y2=[]
        # line pattern
        p=re.compile(r'(\d\d\d\d)-(\d\d)-(\d\d) (\d\d):(\d\d):(\d\d).(\d\d) \((\d+) (\d+)\) \((\d+) (\d+)\)')
        f=open(path)
        line=f.readline().strip(' \n')
        # lines count
        count=0
        while 0<len(line):
                m=p.match(line)
                if m==None or len(m.groups())!=11:
                        raise ValueError('invalid format at line {}'.format(count))
                x1.append(m.group(8))
                x2.append(m.group(9))
                y1.append(m.group(10))
                y2.append(m.group(11))
                # next (line)
                line=f.readline().strip(' \n')
                # next (count)
                count+=1
        return x1,x2,y1,y2

# Params:
# @x1 (iter-of-int) - the begining of mesurements along x-axis
# @x2 (iter-of-int) - the end of mesurements along x-axis
# @y1 (iter-of-int) - the begining of mesurements along y-axis
# @y2 (iter-of-int) - the end of mesurements along y-axis
# Remarks:
# All arrays MUST have the same length. If measurements along z-axis are not
# presented (z==None) then parameter 'delta_z' is used. It specified distance
# along z-axis between two adjacent measurements in pixels.
def curvature(x1,x2,y1,y2,z=None,delta_z=1):
        'Calculation of timber curvature'
        assert len(x1)==len(x2)==len(y1)==len(y2)
        data_len=len(x1)
        if z==None:
                z=[i*delta_z for i in range(data_len)]
        else:
                # all measurements MUST have the same length
                assert len(z)==data_len
        
