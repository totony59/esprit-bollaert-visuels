import json
from PIL import Image,ImageDraw,ImageFont
S=2
im=Image.open('fond.png').convert('RGB').resize((1254*S,1254*S),Image.LANCZOS)
ov=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
COL={'Phares':(30,60,140),'Coups de cœur insolites':(200,50,60),'Plages et criques':(230,170,20),'Villages':(120,40,90),'Ports':(20,110,170),'Balades et nature':(40,130,70)}
for n,c,(x,y) in json.load(open('pos.json')):
    x*=S;y*=S; rr=10*S
    d.ellipse([x-rr+2*S,y-rr+3*S,x+rr+2*S,y+rr+3*S],fill=(0,0,0,70))
    d.ellipse([x-rr,y-rr,x+rr,y+rr],fill=COL[c]+(255,),outline=(255,255,255,255),width=3*S)
P='/home/claude/esprit-bollaert-visuels/bretagne/polices/InterDisplay-'
f=ImageFont.truetype(P+'Bold.otf',19*S)
x0,y0,x1,y1=612*S,1012*S,992*S,1098*S
d.rounded_rectangle([x0,y0,x1,y1],radius=16*S,fill=(250,243,225,235),outline=(20,40,80,255),width=2*S)
items=[('Phares','Phares'),('Plages','Plages et criques'),('Villages','Villages'),('Ports','Ports'),('Balades','Balades et nature'),('Insolites','Coups de cœur insolites')]
for i,(t,k) in enumerate(items):
    cx=x0+(22+(i%3)*125)*S; cy=y0+(25+(i//3)*36)*S; rr=9*S
    d.ellipse([cx-rr,cy-rr,cx+rr,cy+rr],fill=COL[k]+(255,),outline=(255,255,255,255),width=2*S)
    d.text((cx+16*S,cy),t,font=f,fill=(20,40,80,255),anchor='lm')
im=Image.alpha_composite(im.convert('RGBA'),ov).convert('RGB').resize((1254,1254),Image.LANCZOS)
im.save('La_Bretagne_vue_par_vous_118_lieux.png')
