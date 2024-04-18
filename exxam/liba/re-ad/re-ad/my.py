def main(x):
    if x[3] == 'MIRAH':
        if x[0]==1997:
            return x2(x,x4(x,0,1),x1(x,2,3),4)
        elif x[0]== 2016:
            return x1(x,x4(x,5,6),x2(x,7,8,9))
    elif x[3] == 'LASSO':
        return 10

def x1(x,left, right):
    if x[1]=='TXL':
        return left
    if x[1]=='FISH':
        return right

def x2(x,left,middle,right):
    if x[2]=='HYPHY':
        return left
    elif x[2]=='FISH':
        return middle
    elif x[2]=='ZIMPL':
        return right

def x4(x,left,right):
    if x[4]=='ABAP':
        return left
    elif x[4]=='ECL':
        return right


print(main([2016, 'TXL', 'HYPHY', 'MIRAH', 'ECL']))