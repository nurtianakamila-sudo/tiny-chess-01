import json,os,urllib.request as r
U=os.environ.get("MAKEFUN_ENV_URL")
V=[0,100,320,330,500,900,0]
KN=[31,33,14,18,-31,-33,-14,-18];KI=[1,-1,16,-16,15,17,-15,-17]
B=[0]*128;S=1;C=0;G=-1;A=4;Z=116;N=0;M=20000;H=[];tt={}
I=10**6
class X(Exception):pass
def n(s):return "abcdefgh"[s&7]+chr(49+(s>>4))
def u(m):return n(m&127)+n((m>>7)&127)+(" pnbrqk"[(m>>14)&7]).strip()
def F(f):
 global B,S,C,G,A,Z
 B=[0]*128;p=f.split();s=112
 for c in p[0]:
  if c=="/":s-=24
  elif c.isdigit():s+=int(c)
  else:
   q="PNBRQK".index(c.upper())+1
   if c.islower():q=-q
   B[s]=q
   if q==6:A=s
   elif q==-6:Z=s
   s+=1
 S=1-(p[1]=="b")*2
 C=sum(1<<i for i,c in enumerate("KQkq")if c in p[2])
 G=(ord(p[3][0])-97)+(ord(p[3][1])-49)*16 if p[3]!="-" else -1
def T(s,b):
 for ds,o in((((-15,-17),(15,17))[b<0],1),(KN,2),(KI,6)):
  for d in ds:
   t=s+d
   if not t&136 and B[t]==o*b:return 1
 for d in KI:
  t=s+d
  while not t&136:
   q=B[t]
   if q:
    if q==5*b or q==(3 if abs(d)in(15,17) else 4)*b:return 1
    break
   t+=d
 return 0
def W(f,x):
 return [f|x<<7|q<<14 for q in(5,4,3,2)]if(f>>4)==6-5*(S<0)else[f|x<<7]
def g():
 m=[]
 for f in range(128):
  if f&136:continue
  p=B[f]
  if p*S<=0:continue
  t=abs(p);r=f>>4
  if t==1:
   d=16*S;x=f+d
   if not x&136 and not B[x]:
    m+=W(f,x)
    if r==1+5*(S<0) and not B[f+2*d]:m.append(f|(f+2*d)<<7)
   for dd in(d-1,d+1):
    x=f+dd
    if x&136:continue
    if B[x]*S<0 or x==G:m+=W(f,x)
  elif t==2 or t==6:
   for d in KN if t==2 else KI:
    x=f+d
    if not x&136 and B[x]*S<=0:m.append(f|x<<7)
  else:
   ds=KI[4*(t==3):4*(t==4)or 8]
   for d in ds:
    x=f+d
    while not x&136:
     if B[x]:
      if B[x]*S<0:m.append(f|x<<7)
      break
     m.append(f|x<<7);x+=d
 return m
def D(m,p):
 f=m&127;t=(m>>7)&127
 if abs(p)==6 and abs(t-f)==2:
  w=t+1 if t>f else t-2;v=t-1 if t>f else t+1;B[w],B[v]=B[v],B[w]
def K(m):
 global S,C,G,A,Z
 f=m&127;t=(m>>7)&127;q=(m>>14)&7;p=B[f];c=B[t];z=-1
 if abs(p)==1 and t==G and not c:z=t-16*S;B[z]=0
 H.append((m,c,p,C,G,A,Z,z))
 D(m,p)
 B[t]=q*S if q else p;B[f]=0
 if abs(p)==6:A,Z=(t,Z)if p>0 else(A,t);C&=~(3 if p>0 else 12)
 for s,v in((0,2),(7,1),(112,8),(119,4)):
  if f==s or t==s:C&=~v
 G=f+16*S if abs(p)==1 and abs(t-f)==32 else -1
 S=-S
def J():
 global S,C,G,A,Z
 m,c,p,C,G,A,Z,z=H.pop()
 f=m&127;t=(m>>7)&127
 S=-S;B[f]=p;B[t]=c
 if z>=0:B[z]=-p
 D(m,p)
def L():
 ms=g()
 for rt in(1,2,4,8):
  k=116-112*(rt<4);di=1 if rt&5 else -1
  if C&rt and not B[k+di]and not B[k+2*di]and(rt&5 or not B[k+3*di])and not any(T(x,-S) for x in(k,k+di,k+2*di)):ms.append(k|(k+2*di)<<7)
 return [m for m in ms if(K(m),not T([Z,A][S<0],S),J())[1]]
def E():
 s=0
 for x,p in enumerate(B):
  if x&136 or not p:continue
  t=abs(p);f=x&7;r=x>>4
  v=V[t]+((r if p>0 else 7-r)*(15-abs(f-3))if t==1 else(7-abs(f-3)-abs(r-3))*int("0064000"[t]))
  s+=v if p>0 else -v
 return s
def O(ms,t=0):
 return sorted(ms,key=lambda m:(m!=t,-V[abs(B[(m>>7)&127])]))
def z():
 global N;N+=1
 if N>M:raise X
def Q(a,b,pl):
 z()
 if T([A,Z][S<0],-S):
  ms=L()
  if not ms:return -I+pl
 else:
  s=E()*S
  if s>=b:return b
  if s>a:a=s
  ms=[m for m in g() if(B[(m>>7)&127]or((m>>14)&7)or(m>>7)&127==G)and(K(m),not T([Z,A][S<0],S),J())[1]]
  if not ms:return a
 for m in O(ms):
  K(m);s=-Q(-b,-a,pl+1);J()
  if s>a:a=s
  if a>=b:break
 return a
def R(a,b,d,pl):
 z()
 if d<=0:return Q(a,b,pl)
 y=tuple(B);t=tt.get(y)
 ms=L()
 if not ms:return -I+pl if T([A,Z][S<0],-S) else 0
 s=-I;bm=0
 for m in O(ms,t):
  K(m);s2=-R(-b,-a,d-1,pl+1);J()
  if s2>s:s=s2;bm=m
  if s>a:a=s
  if a>=b:break
 tt[y]=bm
 return s
def Y(fen,legal):
 global N
 F(fen);ms=L()
 c=[m for m in ms if u(m) in legal]
 if not c:return legal[0]
 b=c[0]
 for d in range(1,6):
  N=0;al=cs=-I;cb=b
  try:
   for m in c:
    K(m);s=-R(-I,-al,d-1,1);J()
    if s>cs:cs=s;cb=m
    if s>al:al=s
  except X:break
  b=cb
 return u(b)
def P(p,b):
 return json.load(r.urlopen(r.Request(U+p,json.dumps(b).encode())))
h=P("/game",{})
while h["status"]!="done":
 while h["status"]=="your_move":h=P("/move",{"game":h["game"],"move":Y(h["fen"],h["legal_moves"])})
 h=P("/game",{})
