import json,csv,sys
import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage as nd
from scipy.interpolate import RBFInterpolator
sys.path.insert(0,'/home/claude/esprit-bollaert-visuels/bretagne/jeu_carte'); from geo import l93
CP=[  # (lat,lon) -> (x,y)
(48.36,-4.77,42,445),(48.27,-4.62,62,540),(48.04,-4.73,45,625),(47.80,-4.37,110,728),(47.87,-3.92,250,705),
(48.72,-3.98,235,355),(48.68,-3.70,410,345),(48.83,-3.48,600,290),(48.79,-3.05,700,330),(48.53,-2.75,760,400),
(48.68,-2.32,880,345),(48.65,-2.02,960,405),(48.62,-1.55,1110,420),(48.11,-1.68,1040,570),(47.75,-3.37,380,770),
(47.48,-3.12,415,840),(47.62,-2.75,590,790),(47.50,-2.50,700,860),(47.30,-2.52,690,905),(47.27,-2.20,770,905),
(47.22,-1.55,1050,890),(47.11,-2.10,800,990),(48.07,-2.96,560,640),(48.27,-3.57,370,560),(47.85,-1.40,1100,700),
(47.65,-2.08,860,720),(48.45,-4.40,170,450),(48.60,-2.85,720,470)]
src=np.array([l93(lo,la) for la,lo,x,y in CP]); dst=np.array([(x,y) for *_,x,y in CP],float)
f=RBFInterpolator(src,dst,kernel='thin_plate_spline',smoothing=0)
M=np.load('masks.npy'); K=['29','22','56','35','44']
DN={'Finistère':'29',"Côtes-d'Armor":'22','Morbihan':'56','Ille-et-Vilaine':'35','Loire-Atlantique':'44'}
ISL={'ouessant':(28,438),'sein':(38,622),'glénan':(130,772),'groix':(332,830),'belle':(362,858),'hoëdic':(432,878),'bréhat':(700,300),'batz':(318,322)}
def island(r):
    la,lo=float(r['Latitude']),float(r['Longitude']); n=r['Nom'].lower()
    if 'ouessant' in n: return 'ouessant'
    if ('sein' in n and 'île' in n) or 'ar-men' in n: return 'sein'
    if 'glénan' in n: return 'glénan'
    if 47.27<la<47.40 and -3.27<lo<-3.04: return 'belle'
    if 'hoëdic' in n: return 'hoëdic'
    if 'bréhat' in n: return 'bréhat'
    if 'batz' in n: return 'batz'
rows=list(csv.DictReader(open(sys.argv[1])))
pts=[];fixed=[]
for r in rows:
    k=DN[r['Département']]; m=M[K.index(k)]; isl=island(r)
    if isl:
        pts.append(np.array(ISL[isl],float)); fixed.append(None); continue
    p=f(np.array([l93(float(r['Longitude']),float(r['Latitude']))]))[0]
    me=nd.binary_erosion(m,iterations=7)
    ys,xs=np.where(me); i=np.argmin((xs-p[0])**2+(ys-p[1])**2)
    pts.append(np.array([xs[i],ys[i]],float)); fixed.append(me)
pts=np.array(pts)
# séparation
for it in range(60):
    moved=False
    for i in range(len(pts)):
        for j in range(i+1,len(pts)):
            d=pts[j]-pts[i]; dist=np.hypot(*d)
            if dist<19:
                v=d/dist if dist>0 else np.array([1.0,0]); s=(19-dist)/2+0.5
                for idx,sg in ((i,-1),(j,1)):
                    q=pts[idx]+sg*v*s; me=fixed[idx]
                    if me is None: pts[idx]=q; moved=True
                    else:
                        x,y=int(round(q[0])),int(round(q[1]))
                        if 0<=x<me.shape[1] and 0<=y<me.shape[0] and me[y,x]: pts[idx]=q; moved=True
                        else:
                            ys,xs=np.where(me[max(0,y-25):y+25,max(0,x-25):x+25])
                            if len(xs):
                                k=np.argmin((xs+max(0,x-25)-q[0])**2+(ys+max(0,y-25)-q[1])**2); pts[idx]=np.array([xs[k]+max(0,x-25),ys[k]+max(0,y-25)],float); moved=True
    if not moved: break
COL={'Phares':(30,60,140),'Coups de cœur insolites':(200,50,60),'Plages et criques':(225,170,20),'Villages':(120,40,90),'Ports':(20,110,170),'Balades et nature':(40,130,70)}
json.dump([[r['Nom'],r['Calque'],list(map(float,p))] for r,p in zip(rows,pts)],open('pos.json','w'),ensure_ascii=False)
im=Image.open('fond.png').convert('RGB'); d=ImageDraw.Draw(im)
for r,(x,y) in zip(rows,pts):
    rr=9; d.ellipse([x-rr,y-rr,x+rr,y+rr],fill=COL[r['Calque']],outline='white',width=3)
im.save('test.png')
