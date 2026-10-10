import csv, math, sys
rows=list(csv.DictReader(open(sys.argv[1])))
out=sys.argv[2]
ser=[("AGM / U","agm_over_U","#2a78d6","",2),('<tspan font-family="New Computer Modern Math">ℓ</tspan><tspan dy="3" font-size="8">2</tspan><tspan dy="-3"> / U</tspan>',"l2_over_U","#eb6834","6 3",2),
     ("degree / U","deg_over_U","#1baf7a","2 3",2),("best prior / U","bestprior_over_U","#0b0b0b","10 3 2 3",3.2)]
W,H=640,330; L,R,T,B=60,170,20,50
lo,hi=-4,3
X=lambda v:L+(math.log10(v)-lo)/(hi-lo)*(W-L-R)
Y=lambda p:T+(1-p)*(H-T-B)
s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="New Computer Modern, STIX Two Text, Times, serif" font-size="11">',
   f'<rect width="{W}" height="{H}" fill="#ffffff"/>']
for e in range(lo,hi+1):
    x=X(10**e); s.append(f'<line x1="{x:.1f}" y1="{T}" x2="{x:.1f}" y2="{H-B}" stroke="#e6e5e0" stroke-width="1"/>')
    s.append(f'<text x="{x:.1f}" y="{H-B+16}" text-anchor="middle" fill="#52514e">10<tspan dy="-5" font-size="8">{e}</tspan></text>')
for p in (0,.25,.5,.75,1):
    y=Y(p); s.append(f'<line x1="{L}" y1="{y:.1f}" x2="{W-R}" y2="{y:.1f}" stroke="#e6e5e0" stroke-width="1"/>')
    s.append(f'<text x="{L-6}" y="{y+4:.1f}" text-anchor="end" fill="#52514e">{p:.2f}</text>')
x1=X(1); s.append(f'<line x1="{x1:.1f}" y1="{T}" x2="{x1:.1f}" y2="{H-B}" stroke="#0b0b0b" stroke-width="1.2"/>')
s.append(f'<text x="{x1-5:.1f}" y="{H-B-8}" text-anchor="end" fill="#0b0b0b">ratio = 1</text>')
s.append(f'<text x="{(L+W-R)/2:.1f}" y="{H-12}" text-anchor="middle" fill="#0b0b0b">bound / U (log scale)</text>')
s.append(f'<text transform="translate(16,{(T+H-B)/2:.1f}) rotate(-90)" text-anchor="middle" fill="#0b0b0b">fraction of queries ≤ x</text>')
n=len(rows)
for i,(name,col,color,dash,wd) in enumerate(ser):
    v=sorted(max(10**lo,min(10**hi,float(r[col]))) for r in rows)
    pts=[]; 
    for k,val in enumerate(v):
        pts.append(f'{X(val):.1f},{Y(k/n):.1f}'); pts.append(f'{X(val):.1f},{Y((k+1)/n):.1f}')
    d=f' stroke-dasharray="{dash}"' if dash else ''
    s.append(f'<polyline fill="none" stroke="{color}" stroke-width="{wd}"{d} points="{" ".join(pts)}"/>')
    ly=T+14+i*20; lx=W-R+12
    s.append(f'<line x1="{lx}" y1="{ly}" x2="{lx+24}" y2="{ly}" stroke="{color}" stroke-width="{wd}"{d}/>')
    s.append(f'<text x="{lx+30}" y="{ly+4}" fill="#0b0b0b">{name}</text>')
s.append('</svg>'); open(out,'w').write("\n".join(s))
