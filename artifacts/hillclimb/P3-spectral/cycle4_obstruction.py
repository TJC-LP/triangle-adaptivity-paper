from fractions import Fraction
for n in [1,2,3,7,16,64,1000]:
    R={(0,0)}
    S={(0,i) for i in range(n)}
    T={(i,i) for i in range(n)}
    Q={(i,0) for i in range(n)}
    out=sum((y,z) in S and (w,x) in Q for x,y in R for z,w in T)
    sizes=tuple(map(len,[R,S,T,Q]))
    # Exact Gram forms: AA^t=[1], BB^t=[n], CC^t=I_n,
    # and D^tD=[n]. Thus largest eigenvalues are 1,n,1,n.
    squared_norms=(1,n,1,n)
    assert out==n and sizes==(1,n,n,n)
    block_best=1
    upper=sizes[0]*sizes[2]
    assert out==upper
    print('n=%d sizes=%s norm_squared=%s Out=%d W=%d complete_block_best=%d ratio=%s' % (n,sizes,squared_norms,out,upper,block_best,Fraction(out,block_best)))
