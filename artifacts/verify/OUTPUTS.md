# Recorded outputs of the verification scripts

Run on 2026-10-09 with Python 3.11.9 (macOS 26.7, Apple M4 Max), from this directory, as part of assembling the artifacts. Every run below exited 0.

| Run | Command | Exit | Wall (s) | Checks |
|---|---|---:|---:|---|
| `chk_exact` | `python3 -I chk_exact.py --max 15 --random 3000 --seed 7 --pell 6` | 0 | 7 | Theorem B, exact: the referee's 1..15 grid, random certified instances, Pell family |
| `chk_exact25` | `python3 -I chk_exact.py --max 25 --random 10000 --seed 11 --pell 8` | 0 | 90 | Theorem B, exact: extended grid 1..25 (34,328,125 vectors) |
| `chk` | `../e2/venv/bin/python -I chk.py` | 0 | 1 | Theorem B, original float check (numpy 2.4.6) |
| `g8` | `python3 -I g8.py` | 0 | 0 | G8 gadget and rotation union, m = 2, 3 |
| `fams_G8` | `python3 -I thm1/fams.py G8 2 3 4` | 0 | 2 | Theorem 1.L |
| `fams_F11` | `python3 -I thm1/fams.py F 1 1 2 3` | 0 | 0 | Theorem 1.L', F(1,1) |
| `fams_F21` | `python3 -I thm1/fams.py F 2 1 2` | 0 | 0 | Theorem 1.L', F(2,1) |
| `fams_F22` | `python3 -I thm1/fams.py F 2 2 2` | 0 | 1 | Theorem 1.L', F(2,2) |
| `fams2_2a` | `python3 -I thm1/fams2.py 2a 2 4 8 16` | 0 | 0 | Theorem 2(a), fixed-order family |
| `fams2_min` | `python3 -I thm1/fams2.py min 2 3` | 0 | 0 | Theorem 2(b), GMIN and padded GMIN |
| `fams2_mr` | `python3 -I thm1/fams2.py mr 2 3 4` | 0 | 1 | Theorem 2(a), GMR and padded GMR |
| `fams2_fer` | `python3 -I thm1/fams2.py fer 2 4 8 16` | 0 | 0 | Proposition 4, Ferrers family |
| `rnd` | `python3 -I thm1/rnd.py 1 4500` | 0 | 5 | Lemma 1.4, Theorem 1.U, Prop. 1.3, Lemma 1.2, Prop. 3 scheduler |

The "Checks" column uses the scripts' internal names. Their mapping to the
paper (revision 2): Theorem B = Theorem 3.1 (`thm-main`); Pell family =
Theorem 3.7 (`thm-sharp`); Lemma 1.2 = Lemma 5.1 (`lem-sum`); Prop. 1.3 =
Corollary 5.4(3) (`cor-pb`); Lemma 1.4 = Lemma 5.2 (`lem-perroot`);
Theorem 1.U = Theorem 5.3 (`thm-pb-upper`); Theorem 1.L = Theorem 5.5
(`thm-pb-lower`); Theorem 1.L' = Theorem 5.9 (`thm-pb-slopes`);
Theorem 2(a) and 2(b) = Theorem 5.10(1) and (2) (`thm-sep`); Prop. 3 =
Proposition 5.14 (`prop-ptr`); Proposition 4 = Proposition 5.16
(`prop-ferrers`). `README.md` has the full table.

Script digests (sha256):

```
a8a40e367751cbd2df1f1294c79fdd460dfe9950f8b47af443a356e4fc010d40  chk_exact.py
c32134ca82add01f57fd578a19479b61a6c8cdacf705c40dafa85d1648e181ff  chk.py
fb1b5b57873b6f83a1faaf00e5d2b05f793c16d1652ac934a630204d2c10e2f7  g8.py
21f52e8bc85600b98ebc0f8603a10ba1c5b6dc4c8440ef60764dca1e5da181b6  thm1/ev.py
83b7af85475a5d35913300201c733201c9c235ddeb82dc3d95a072b1825b22f9  thm1/fams.py
49d42fec8c7a2a9ed5ac8d72a6e8f0677f609bbf6086d971e38ab7e26d712f67  thm1/fams2.py
c83057325e1d5e2b1df8530ae2dd5c160431f78824f9b1fcb7c8d202177040ef  thm1/rnd.py
```

## `chk_exact`

`python3 -I chk_exact.py --max 15 --random 3000 --seed 7 --pell 6` (exit 0)

```
grid 1<=s_i<=r_i<=15: 1728000 statistic vectors, 0 failures
  max (U/mabc)^2 = 441/32 (< 16 required) at r=(7, 14, 15) s=(5, 9, 9) U^2=882 (a,b,c,m)=(2, 1, 4, 1)
random 0/1 instances: 2324 with nonempty relations, 2324 certified Out <= U_lo <= U (exact); max (Out/U_lo)^2 = 1 ~ 1.0000
pell sharpness family, 6 terms: ok
  (p,q)=(7,5)  U/W = 2401/625 ~ 3.841600000
  (p,q)=(41,29)  U/W = 2825761/707281 ~ 3.995245171
  (p,q)=(239,169)  U/W = 3262808641/815730721 ~ 3.999859950
  (p,q)=(1393,985)  U/W = 3765342321601/941336550625 ~ 3.999995877
  (p,q)=(8119,5741)  U/W = 4345203949621921/1086301020364561 ~ 3.999999879
  (p,q)=(47321,33461)  U/W = 5014361666349715681/1253590417707067441 ~ 3.999999996
PASS
```

## `chk_exact25`

`python3 -I chk_exact.py --max 25 --random 10000 --seed 11 --pell 8` (exit 0)

```
grid 1<=s_i<=r_i<=25: 34328125 statistic vectors, 0 failures
  max (U/mabc)^2 = 44/3 (< 16 required) at r=(11, 12, 23) s=(8, 9, 16) U^2=2112 (a,b,c,m)=(3, 1, 4, 1)
random 0/1 instances: 7984 with nonempty relations, 7984 certified Out <= U_lo <= U (exact); max (Out/U_lo)^2 = 1 ~ 1.0000
pell sharpness family, 8 terms: ok
  (p,q)=(7,5)  U/W = 2401/625 ~ 3.841600000
  (p,q)=(41,29)  U/W = 2825761/707281 ~ 3.995245171
  (p,q)=(239,169)  U/W = 3262808641/815730721 ~ 3.999859950
  (p,q)=(1393,985)  U/W = 3765342321601/941336550625 ~ 3.999995877
  (p,q)=(8119,5741)  U/W = 4345203949621921/1086301020364561 ~ 3.999999879
  (p,q)=(47321,33461)  U/W = 5014361666349715681/1253590417707067441 ~ 3.999999996
  (p,q)=(275807,195025)  U/W = 5786569020271612560001/1446642255105937890625 ~ 4.000000000
  (p,q)=(1607521,1136689)  U/W = 6677695635116972385924481/1669423908780535158363841 ~ 4.000000000
PASS
```

## `chk`

`../e2/venv/bin/python -I chk.py` (exit 0)

```
max Out/U over random instances: 1.0 (must be <= 1)
max U/Out_construction: 3.6155 (theorem: < 4)
```

## `g8`

`python3 -I g8.py` (exit 0)

```
m=2: G8 A=(576,32,256) | U: N=2208 fw=(1280, 1280, 1280) B2=1280 A=864 A/(N+B2)=0.248 thm1U=4752 triangles=0
m=3: G8 A=(20412,243,6561) | U: N=48843 fw=(32805, 32805, 32805) B2=32805 A=27216 A/(N+B2)=0.333 thm1U=141384 triangles=0
```

## `fams_G8`

`python3 -I thm1/fams.py G8 2 3 4` (exit 0)

```
G8 m=2 single:Ax=576 Ay=32 Az=256 N=736  union: A=864 N=2208 B2=1280 A/(N+B2)=0.248 A/ThmA=0.182 minM=1024
G8 m=3 single:Ax=20412 Ay=243 Az=6561 N=16281  union: A=27216 N=48843 B2=32805 A/(N+B2)=0.333 A/ThmA=0.192 minM=39366
G8 m=4 single:Ax=266240 Ay=1024 Az=65536 N=152576  union: A=332800 N=457728 B2=327680 A/(N+B2)=0.424 A/ThmA=0.200 minM=524288
```

## `fams_F11`

`python3 -I thm1/fams.py F 1 1 2 3` (exit 0)

```
F(1,1) u=2 A=864 N=1440 B2=1024 A/(N+B2)=0.351 A/(N^3/8 B2^3/4)=0.312
F(1,1) u=3 A=27216 N=29160 B2=26244 A/(N+B2)=0.491 A/(N^3/8 B2^3/4)=0.279
```

## `fams_F21`

`python3 -I thm1/fams.py F 2 1 2` (exit 0)

```
F(2,1) u=2 A=2187264 N=368640 B2=3211264 A/(N+B2)=0.611 A/(N^3/8 B2^3/4)=0.236
```

## `fams_F22`

`python3 -I thm1/fams.py F 2 2 2` (exit 0)

```
F(2,2) u=2 A=332800 N=261120 B2=262144 A/(N+B2)=0.636 A/(N^3/8 B2^3/4)=0.267
```

## `fams2_2a`

`python3 -I thm1/fams2.py 2a 2 4 8 16` (exit 0)

```
2a a=2: N=12 B2=6 A=8 (Ax,Ay,Az)=(8,8,8) M=(8,4,4) A/(N+B2)=0.436 minM/(N+B2)=0.218 MR/(N+B2)=0.436 Q=4
2a a=4: N=48 B2=40 A=32 (Ax,Ay,Az)=(32,32,32) M=(64,16,16) A/(N+B2)=0.362 minM/(N+B2)=0.181 MR/(N+B2)=0.725 Q=16
2a a=8: N=192 B2=256 A=128 (Ax,Ay,Az)=(128,128,128) M=(512,64,64) A/(N+B2)=0.286 minM/(N+B2)=0.143 MR/(N+B2)=1.143 Q=64
2a a=16: N=768 B2=1625 A=512 (Ax,Ay,Az)=(512,512,512) M=(4096,256,256) A/(N+B2)=0.214 minM/(N+B2)=0.107 MR/(N+B2)=1.711 Q=256
```

## `fams2_min`

`python3 -I thm1/fams2.py min 2 3` (exit 0)

```
GMIN m=2: N=168 B2=96 A=40 (Ax,Ay,Az)=(40,40,40) M=(64,64,64) A/(N+B2)=0.152 minM/(N+B2)=0.242 MR/(N+B2)=0.242 Q=0
GMIN m=2 padded: N=492 B2=268 A=296 (Ax,Ay,Az)=(296,296,296) M=(212,212,212) A/(N+B2)=0.389 minM/(N+B2)=0.279 MR/(N+B2)=0.279 Q=108
GMIN m=3: N=1053 B2=729 A=270 (Ax,Ay,Az)=(270,270,270) M=(729,729,729) A/(N+B2)=0.152 minM/(N+B2)=0.409 MR/(N+B2)=0.409 Q=0
GMIN m=3 padded: N=3321 B2=1971 A=2052 (Ax,Ay,Az)=(2052,2052,2052) M=(1755,1755,1755) A/(N+B2)=0.388 minM/(N+B2)=0.332 MR/(N+B2)=0.332 Q=756
```

## `fams2_mr`

`python3 -I thm1/fams2.py mr 2 3 4` (exit 0)

```
GMR m=2: N=36 B2=16 A=0 (Ax,Ay,Az)=(16,4,0) M=(32,0,0) A/(N+B2)=0.000 minM/(N+B2)=0.000 MR/(N+B2)=0.615 Q=0
GMR m=2 padded: N=90 B2=44 A=36 (Ax,Ay,Az)=(68,44,36) M=(50,22,34) A/(N+B2)=0.268 minM/(N+B2)=0.164 MR/(N+B2)=0.373 Q=18
GMR m=3: N=171 B2=81 A=0 (Ax,Ay,Az)=(81,9,0) M=(243,0,0) A/(N+B2)=0.000 minM/(N+B2)=0.000 MR/(N+B2)=0.964 Q=0
GMR m=3 padded: N=423 B2=228 A=168 (Ax,Ay,Az)=(330,186,168) M=(327,93,165) A/(N+B2)=0.258 minM/(N+B2)=0.143 MR/(N+B2)=0.502 Q=84
GMR m=4: N=528 B2=256 A=0 (Ax,Ay,Az)=(256,16,0) M=(1024,0,0) A/(N+B2)=0.000 minM/(N+B2)=0.000 MR/(N+B2)=1.306 Q=0
GMR m=4 padded: N=1308 B2=753 A=520 (Ax,Ay,Az)=(1032,552,520) M=(1284,276,516) A/(N+B2)=0.252 minM/(N+B2)=0.134 MR/(N+B2)=0.623 Q=260
```

## `fams2_fer`

`python3 -I thm1/fams2.py fer 2 4 8 16` (exit 0)

```
Ferrers m=2: N=36 B2=40 A=12 (Ax,Ay,Az)=(16,16,12) M=(24,8,8) A/(N+B2)=0.158 minM/(N+B2)=0.105 MR/(N+B2)=0.316 Q=0
Ferrers m=4: N=144 B2=320 A=80 (Ax,Ay,Az)=(96,96,80) M=(192,64,64) A/(N+B2)=0.172 minM/(N+B2)=0.138 MR/(N+B2)=0.414 Q=0
Ferrers m=8: N=576 B2=2560 A=576 (Ax,Ay,Az)=(640,640,576) M=(1536,512,512) A/(N+B2)=0.184 minM/(N+B2)=0.163 MR/(N+B2)=0.490 Q=0
Ferrers m=16: N=2304 B2=20480 A=4352 (Ax,Ay,Az)=(4608,4608,4352) M=(12288,4096,4096) A/(N+B2)=0.191 minM/(N+B2)=0.180 MR/(N+B2)=0.539 Q=0
```

## `rnd`

`python3 -I thm1/rnd.py 1 4500` (exit 0)

```
4500 instances OK; worst ratios {'A': 0.639, 'root': 0.69, 'LL': 0.828, 'M': 0.419, 'P3': 3.5}
```

## Notes

- `chk_exact` reproduces the referee's exhaustive check exactly. The grid 1 ≤ s_i ≤ r_i ≤ 15 has 1,728,000 vectors and no failures, with maximum construction ratio (U/mabc)² = 441/32 at r = (7, 14, 15), s = (5, 9, 9), (a, b, c, m) = (2, 1, 4, 1); that is, U/mabc = √(441/32) ≈ 3.71. On the extended grid up to 25 the maximum is (U/mabc)² = 44/3, at r = (11, 12, 23), s = (8, 9, 16). The Pell rows match the referee's 2401/625, 2825761/707281 and 3262808641/815730721.
- An earlier draft of `chk_exact.py` certified σ² only through power iterates of 𝟙. It left 7 of 2,324 random instances uncertified (exit 1). All 7 were equality cases where a maximum-degree term of U is tight, and power iteration approaches σ² only from below. The final script adds unit vectors and rows of A as Rayleigh candidates (their quotients are the column degrees, and at least the row degrees), and then certifies all instances. The table records the final script's run.
- `rnd.py` at other seeds, each with 4,500 instances and exit 0 (worst-ratio dictionaries):
  - seed 0: `{'A': 0.495, 'root': 0.66, 'LL': 0.885, 'M': 0.446, 'P3': 3.2}`
  - seed 2: `{'A': 0.553, 'root': 0.654, 'LL': 0.816, 'M': 0.418, 'P3': 3.0}`
  - seed 3: `{'A': 0.604, 'root': 0.663, 'LL': 0.844, 'M': 0.449, 'P3': 3.0}`
  - seed 7: `{'A': 0.599, 'root': 0.653, 'LL': 0.876, 'M': 0.421, 'P3': 3.0}`
  - seed 42: `{'A': 0.476, 'root': 0.614, 'LL': 0.857, 'M': 0.433, 'P3': 3.0}`
  See `README.md` for how `P3` relates to the paper's quoted 2.33/2.83.
