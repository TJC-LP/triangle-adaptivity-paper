from fractions import Fraction

def merge_count(left,right):
    i=j=count=0
    result=[]
    while i<len(left) and j<len(right):
        count+=1
        if left[i]<right[j]:
            i+=1
        elif left[i]>right[j]:
            j+=1
        else:
            result.append(left[i]); i+=1; j+=1
    return count,result

for i,j,u in [(1,1,2),(1,1,3),(2,1,2),(2,2,2)]:
    n=u**(4*i); a=u**(4*i-2*j); b=u**(4*i-j)
    c=u**(4*i+2*j); d=u**(4*i-3*j); H=u**(3*j)
    assert n==H*d and c==H*b and c*a==u**(8*i)
    Z1=[(H+1)*k for k in range(b)]
    Y0=[(c+1)*l for l in range(a)]
    z_counts=[]
    for h in range(H):
        row=[(H+1)*k+h+1 for k in range(b)]
        ct,out=merge_count(Z1,row)
        assert not out and ct==2*b-1
        z_counts.append(ct)
    y_counts=[]
    for z in range(c):
        row=[(c+1)*l+z+1 for l in range(a)]
        ct,out=merge_count(Y0,row)
        assert not out and ct==2*a-1
        y_counts.append(ct)
    Cx=n*min(a*(1+z_counts[0]),b*(1+y_counts[0]))
    Cy=a*min(b,n*(1+z_counts[0]))
    Cz=c*min(a,d*(1+y_counts[0]))
    assert (Cx,Cy,Cz)==(2*u**(12*i-3*j),u**(8*i-3*j),u**(8*i))
    N=3*(u**(8*i)+u**(8*i-j)+u**(8*i-2*j)+u**(8*i-3*j))
    fwd=3*u**(12*i-4*j)+u**(8*i)
    rev=3*u**(12*i-2*j)+u**(12*i-5*j)
    assert fwd<rev
    print('parameters', (i,j,u), 'checked row types',(len(z_counts),len(y_counts)), 'comparisons',(min(z_counts),min(y_counts)), 'root costs',(Cx,Cy,Cz), 'union',(N,fwd,Cx+Cy+Cz),'slope',Fraction(3,2)-Fraction(j,2*i),'exponent',Fraction(3,2)-Fraction(3*j,8*i))
