import sys,json,math
sys.path.insert(0,'bretagne/jeu_carte'); from geo import l93, anneaux
from PIL import Image,ImageDraw,ImageFont
S=2;W,H=1080*S,1350*S
CR=(244,239,228);NAVY=(20,40,80);INK=(25,25,30)
img=Image.new('RGB',(W,H),CR);d=ImageDraw.Draw(img)
P='bretagne/polices/InterDisplay-';F=lambda w,s:ImageFont.truetype(P+w+'.otf',int(s*S))
X0,X1,Y0,Y1=96000,406000,6646000,6889000
mx,my,mw=10*S,262*S,1060*S; sc=mw/(X1-X0); mh=(Y1-Y0)*sc
def px(x,y): return (mx+(x-X0)*sc, my+(Y1-y)*sc)
g=json.load(open('bretagne/jeu_carte/departements.geojson'))
for f in g['features']:
    br=f['properties']['code'] in ('22','29','35','44','56')
    for poly in anneaux(f['geometry']):
        pts=[px(*l93(p[0],p[1])) for p in poly[0]]
        d.polygon(pts,fill=(255,255,255) if br else (226,222,212),outline=(150,160,175) if br else (205,200,190),width=3*S if br else 2*S)
d.rectangle([0,0,W,250*S],fill=(20,20,22))
d.text((W//2,70*S),'LES SPÉCIALITÉS',font=F('ExtraBold',62),fill='white',anchor='mm')
d.text((W//2,150*S),'DE BRETAGNE',font=F('ExtraBold',72),fill=(240,196,110),anchor='mm')
d.text((W//2,212*S),'Où goûter quoi ? Notre carte gourmande',font=F('Medium',28),fill=(220,220,225),anchor='mm')
d.rectangle([0,250*S,W,256*S],fill=(30,78,121))
W_=(255,255,255)
M=[("Kouign-amann",48.093,-4.329,(170,100,30),W_,"Douarnenez"),("Crêpes dentelle",47.996,-4.102,(200,140,40),INK,"Quimper"),
("Palets",47.855,-3.747,(180,120,40),W_,"Pont-Aven"),("Kig ha farz",48.684,-3.985,(120,60,30),W_,"Saint-Pol-de-Léon"),
("Oignon rosé",48.726,-3.985,(170,40,90),W_,"Roscoff"),("Fraises",48.373,-4.370,(210,30,40),W_,"Plougastel"),
("Huîtres",47.811,-3.698,(60,90,100),W_,"Belon"),("Langoustines",47.797,-4.284,(220,90,50),W_,"Le Guilvinec"),
("Cidre",47.893,-4.000,(200,150,20),INK,"Fouesnant"),("Coco de Paimpol",48.778,-3.047,(150,40,40),W_,"Paimpol"),
("Saint-Jacques",48.632,-2.462,(230,120,60),W_,"Erquy"),("Caramel beurre salé",47.484,-3.120,(160,90,30),W_,"Quiberon"),
("Andouille",48.067,-3.207,(90,40,30),W_,"Guémené-sur-Scorff"),("Huîtres du Golfe",47.569,-2.946,(40,90,110),W_,"Locmariaquer"),
("Galette-saucisse",48.112,-1.680,(150,70,30),W_,"Rennes"),("Huîtres",48.676,-1.851,(50,100,120),W_,"Cancale"),
("Craquelins",48.649,-2.025,(210,170,90),INK,"Saint-Malo"),("Moules de bouchot",48.601,-1.766,(20,40,90),W_,"Le Vivier-sur-Mer"),
("Gâteau nantais",47.218,-1.554,(190,130,50),INK,"Nantes"),("Berlingots",47.218,-1.554,(220,60,120),W_,"Nantes"),
("Sel de Guérande",47.328,-2.429,(110,130,150),W_,"Guérande"),("Muscadet",47.163,-1.264,(140,160,40),INK,"Vallet"),
]
fb=F('ExtraBold',19); fs=F('Medium',13)
pts=[px(*l93(lo,la)) for _,la,lo,*_ in M]
ymax=my+mh
placed=[]
def ok(b):
    x0,y0,x1,y1=b
    if x0<8*S or x1>W-8*S or y0<262*S or y1>ymax: return False
    for q in placed:
        if not (x1+6*S<q[0] or x0-6*S>q[2] or y1+6*S<q[1] or y0-6*S>q[3]): return False
    for (px_,py_) in pts:
        if x0-8*S<px_<x1+8*S and y0-8*S<py_<y1+8*S: return False
    return True
L=[]
order=sorted(range(len(M)),key=lambda i:-sum(1 for p in pts if math.dist(p,pts[i])<120*S))
for i in order:
    n,la,lo,bg,fg,v=M[i]; x,y=pts[i]
    bw=max(fb.getlength(n),fs.getlength(v))+20*S; bh=42*S
    best=None
    for r in range(35,600,8):
        for k in range(36):
            a=2*math.pi*k/36; cx=x+r*S*math.cos(a); cy=y+r*S*math.sin(a)*0.8
            b=(cx-bw/2,cy-bh/2,cx+bw/2,cy+bh/2)
            if ok(b): best=b;break
        if best: break
    assert best,M[i][0]
    placed.append(best); L.append((i,best))
for i,b in L:
    x,y=pts[i]; cx,cy=(b[0]+b[2])/2,(b[1]+b[3])/2
    d.line([x,y,cx,cy],fill=(130,140,155),width=2*S)
for i,b in L:
    n,la,lo,bg,fg,v=M[i]; cx,cy=(b[0]+b[2])/2,(b[1]+b[3])/2
    d.rounded_rectangle(b,radius=9*S,fill=bg,outline='white',width=2*S)
    d.text((cx,cy-6*S),n,font=fb,fill=fg,anchor='mm'); d.text((cx,cy+12*S),v,font=fs,fill=fg,anchor='mm')
for x,y in pts:
    r=6*S; d.ellipse([x-r,y-r,x+r,y+r],fill=NAVY,outline='white',width=2*S)
d.text((W//2,H-110*S),"Il en manque ? Dites-le en commentaire !",font=F('Bold',34),fill=NAVY,anchor='mm')
d.rectangle([0,H-70*S,W,H],fill=(20,20,22))
d.text((W//2,H-35*S),'CAP SUR LA BRETAGNE',font=F('ExtraBold',30),fill='white',anchor='mm')
img.resize((1080,1350),Image.LANCZOS).save(sys.argv[1]); print(round(ymax/S))
