from pathlib import Path
from fractions import Fraction as F
from collections import Counter,defaultdict
import csv
import sys
# The verifier's working copy of the run-B data (raw-new/, raw-old2/, ctl/, logs/); pass its path.
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '.')
def load(file):
    groups=defaultdict(dict)
    for row in csv.DictReader(file.open()):
        assert row['policy'] not in groups[row['query_id']]
        groups[row['query_id']][row['policy']]=row
    return groups

def quantile(xs,p):
    xx=sorted(xs);i=F(len(xx)-1)*p;j=i.numerator//i.denominator
    return xx[j] if i==j else xx[j]+(xx[j+1]-xx[j])*(i-j)
def time(r):return int(r['median_ns'])
def printnum(label,x):print(label,str(x),'decimal',format(float(x),'.12g'))

print('KG RESULTS recomputed independently from raw CSV using integer/Fraction arithmetic')
for name in ['codex-l','sci50','w5m']:
    groups=load(ROOT/'raw-new'/f'{name}.csv')
    good=[p for p in groups.values() if p['sampled']['outcome']!='timeout' and p['greedy']['outcome']!='timeout']
    factor=quantile([F(time(p['sampled']),time(p['greedy'])) for p in good if p['sampled']['outcome']=='gate'],F(1,2))
    new=[];old=[];raw=[]
    for p in good:
        nn=time(p['sampled']);rescued=p['sampled']['outcome']=='rescued'
        new.append(nn);old.append(time(p['greedy'])*factor if rescued else F(nn));raw.append(F(time(p['greedy']) if rescued else nn))
    ratios=[a/b for a,b in zip(old,new)];ratiosraw=[a/b for a,b in zip(raw,new)]
    outcomes=Counter(p['sampled']['outcome'] for p in good)
    oks=sum(r['answer_ok']=='1' for p in groups.values() for r in p.values());total=sum(map(len,groups.values()))
    print('\nDATASET',name,'queries',len(groups),'timed',len(good),'outcomes',dict(outcomes),'answer_flags',oks,total)
    print('timeouts',[qid for qid,p in groups.items() if p['sampled']['outcome']=='timeout' or p['greedy']['outcome']=='timeout'])
    printnum('overhead',factor);printnum('old_total_ms',sum(old)/1000000);printnum('new_total_ms',F(sum(new),1000000))
    for what,rs in [('adjusted',ratios),('raw',ratiosraw)]:
        printnum(what+'_median',quantile(rs,F(1,2)));printnum(what+'_p90',quantile(rs,F(9,10)));printnum(what+'_max',max(rs))
        print(what,'regressions_gt_1.2',sum(x<F(5,6) for x in rs))
    olddecl=outcomes['gate']+outcomes['rescued'];newdecl=outcomes['gate'];print('declines',olddecl,newdecl,'/',len(good))
    oldpath=ROOT/'raw-old2'/f'{name}.csv'
    if oldpath.exists():
        former=load(oldpath);agree=0;totalagree=0
        for qid,p in groups.items():
            if qid not in former:continue
            oo=former[qid]['sampled'];nn=p['sampled']
            # Accepted pick equality is required even if both say accepted.
            valid=(oo['outcome']=='accepted' and nn['outcome']=='accepted' and oo['pick']==nn['pick']) or (oo['outcome']=='gate' and nn['outcome'] in ('gate','rescued')) or (oo['outcome']==nn['outcome'] and oo['outcome'] not in ('accepted','gate'))
            agree+=valid;totalagree+=1
        print('stage1_old2_agreement',agree,totalagree)
    for p in groups.values():
        for row in p.values():
            if row['median_ns'] and row['runs_ns']:
                rr=[int(v) for v in row['runs_ns'].split(';')]
                assert quantile(rr,F(1,2))==time(row),(name,row['query_id'],row['policy'])
    print('all stored medians equal independently computed run medians')

print('\nSYNTHETIC CONTROLS sampled-policy decisions and exact ratios')
for name in ['skew','uni','medium']:
    old=load(ROOT/'ctl'/f'old_{name}.csv');new=load(ROOT/'ctl'/f'new_{name}.csv')
    for qid,p in new.items():
        oo=old[qid]['sampled'];nn=p['sampled']
        ratio=F(time(nn),time(oo));print(name,qid,'old_ns',time(oo),'new_ns',time(nn),'ratio',ratio,'decimal',float(ratio),'outcome',oo['outcome'],nn['outcome'],'picks',oo['pick'],nn['pick'],'above1.05',ratio>F(21,20))
print('historical answer log SAME count',sum(line.rstrip().endswith(',SAME') for line in (ROOT/'ctl'/'answers.log').read_text().splitlines()))
print('historical gates.rc',repr((ROOT/'logs'/'gates.rc').read_text()))
print('historical build.rc',repr((ROOT/'logs'/'build.rc').read_text()))

print('\nLITERAL FLOOR-SKIPPING COUNTEREXAMPLE')
# Directed shape (x,y),(x,z),(y,z); second relation shares seed subject.
seed={(i,i) for i in range(1000)}
positions={s*1000//64 for s in range(64)}
left={(i,15*i+j) for i in positions for j in range(15)}
right={(i,100000+15*i+j) for i in positions for j in range(15)}
left|={(10000+i,200000+i) for i in range(10000-len(left))}
right|={(30000+i,300000+i) for i in range(20000-len(right))}
edges=[seed,left,right];shape=[(0,1),(0,2),(1,2)]
assert [len(e) for e in edges]==[1000,10000,20000]
assert {z for _,z in left}.isdisjoint(z for _,z in right)

def stats(d,full=False):
    x,y=shape[d];other=[i for i in range(3) if i!=d]
    e2=next(i for i in other if y in shape[i]);e3=next(i for i in other if x in shape[i])
    deg2=Counter(row[shape[e2].index(y)] for row in edges[e2]);deg3=Counter(row[shape[e3].index(x)] for row in edges[e3])
    ordered=sorted(edges[d]);n=len(ordered);k=n if full else min(n,64)
    smin=s2=s3=0
    for s in range(k):
        a,b=ordered[s*n//k];u=deg2[b];v=deg3[a]
        smin+=min(u,v);s2+=u;s3+=v
    return dict(n=n,n2=len(edges[e2]),n3=len(edges[e3]),A=n*smin//k,left=n*s2//k,right=n*s3//k,e2=e2,e3=e3)
def depth(other,n):return max(0,(other//n).bit_length()-1)
def cost(c,branch,floor=False):
    n=c['n'];walk=0 if floor else c['A'];l2=depth(c['n2'],n);l3=depth(c['n3'],n)
    return n*((4+l2+3*l3) if branch=='large' else (8+2*l2+6*l3))+(20 if branch=='large' else 30)*walk
cand=[stats(i) for i in range(3)];print('sampled_candidates',cand);print('exact_candidates',[stats(i,True) for i in range(3)])
probe=cand[0]['e2']==1;path=cand[0]['left'] if probe else cand[0]['right'];greedy=cand[0]['n']+path
sampled=[i==0 or 2*c['n']<=greedy for i,c in enumerate(cand)]
assert sampled==[True,False,False]
assert 2*cand[0]['n']+cand[0]['A']>greedy
budgetS=cand[0]['n']*(40 if probe else 9);budgetL=2*(budgetS+26*path)
print('probe_first',probe,'path',path,'stage1_greedy',greedy,'stage1_seed_kernel',2*cand[0]['n']+cand[0]['A'],'large_3K_budget',budgetL,'structural_K_budget',budgetS)
for i,c in enumerate(cand):print('driver',i,'large',cost(c,'large'),'structural',cost(c,'structural'),'large_floor',cost(c,'large',True),'structural_floor',cost(c,'structural',True))

def rescue(prune):
    available=sampled.copy()
    for i,c in enumerate(cand):
        if available[i]:continue
        failedL=c['n']<16384 or 3*cost(c,'large',True)>budgetL
        if prune and failedL and cost(c,'structural',True)>budgetS:continue
        available[i]=True
    take=[i for i in range(3) if available[i]]
    large=min(take,key=lambda i:(cost(cand[i],'large'),i))
    if cand[large]['n']>=16384 and 3*cost(cand[large],'large')<=budgetL:return available,('large',large)
    small=min(take,key=lambda i:(cost(cand[i],'structural'),i))
    if cost(cand[small],'structural')<=budgetS:return available,('structural',small)
    return available,None
print('floor_filtered',rescue(True),'all_sampled',rescue(False))
assert rescue(True)[1]==('large',2) and rescue(False)[1] is None
print('fully explicit graph, literal sampling: decision preservation REFUTED; output=0')
