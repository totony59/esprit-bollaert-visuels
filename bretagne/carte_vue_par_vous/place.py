import json,csv,math,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from scipy import ndimage as nd
from matplotlib.path import Path
REPO='/home/claude/esprit-bollaert-visuels/'
a=np.asarray(Image.open('fond.png').convert('RGB')).astype(int)
r,g,b=a[...,0],a[...,1],a[...,2]
cream=(r>215)&(g>195)&(b>140)&(b<215)&(r-b>25)
dark=(r<90)&(g<100)&(b<140)
land=cream & ~nd.binary_dilation(dark,iterations=2)
land=nd.binary_opening(land,iterations=1)
sea=nd.binary_opening((b>110)&(b>r+30),iterations=4)
lab,n=nd.label(land)
H,W=land.shape; yy,xx=np.mgrid[0:H,0:W]
def comp_at(x,y): return lab[y,x]
masks={}
masks['29']=np.isin(lab,[comp_at(200,450)])|np.isin(lab,[comp_at(120,650)] if lab[650,120] else [])
masks['22']=lab==comp_at(450,400) if lab[400,450] else None
masks['35']=lab==lab[540,1100]
sz=np.bincount(lab.ravel()); sz[0]=0; order=np.argsort(-sz)
big=None
for L in order[:6]:
    ys,xs=np.where(lab==L)
    if xs.min()>300 and ys.min()>500 and ys.max()<1100 and xs.max()>1100: big=lab==L;break
border=Path([(915,560),(915,600),(905,660),(895,720),(890,775),(830,785),(780,790),(750,835),(740,1000),(1300,1000),(1300,560)])
inside=border.contains_points(np.c_[xx.ravel(),yy.ravel()]).reshape(H,W)
masks['56']=big&~inside; masks['44']=big&inside
for k,m in masks.items():
    ys,xs=np.where(m); print(k,m.sum(),xs.min(),xs.max(),ys.min(),ys.max())
np.save('masks.npy',np.stack([masks[k] for k in ['29','22','56','35','44']]))
np.save('sea.npy',sea)
