import random, statistics as st, sys
R=random.Random(1)
P={'heal':0.0,'regen':1,'t4':5,'chrys':True}
d=lambda n: R.randint(1,n)
def hit(score):  # d20 <= score, 1 always, 20 never
    r=d(20); return r==1 or (r!=20 and r<=score)
CLS={ # pv, def, mait, ecl, inst, role
 'rempart':(12,3,10,2,9,'melee'),'tisseur':(9,1,11,4,11,'ranged'),'lamesort':(10,2,12,3,9,'melee'),
 'pisteur':(9,1,12,3,11,'ranged'),'elementaliste':(7,0,12,5,10,'ranged'),'passeombre':(9,2,11,3,11,'melee')}
CR={ # att, def, pv, dmg, kind
 'chenille':(8,0,3,4,'c'),'phalene':(11,1,6,4,'f'),'cracheur':(10,2,5,4,'r'),'vesse':(0,0,4,6,'v'),
 'blaireau':(12,3,14,8,'e'),'lumivore':(13,3,24,10,'b')}
class H:
    def __init__(s,c):
        s.c=c; s.pv0,s.df,s.m,s.e0,s.inst,s.role=CLS[c]; s.pv=s.pv0; s.e=s.e0; s.malus=0; s.down=False; s.armor=0
class C:
    def __init__(s,k,n,extra=None):
        s.k=k; s.att,s.df,pv,s.dmg,s.kind=CR[k]
        f=0.5 if s.kind=='b' else 0.25
        s.pv=round(pv*(1+f*(n-2))) if pv else 0
        s.pv0=s.pv; s.age=0; s.dove=False
def alive(L): return [x for x in L if (x.pv>0 if isinstance(x,C) else not x.down)]
def fight(H_,crs,n,st_,brume=False,boss=False):
    rounds=0; leurre=6 if boss else 0; phase2=False; dark=False; diving=False
    while alive(H_) and alive(crs):
        rounds+=1
        if rounds>15: break
        # heroes
        illum=0
        for h in alive(H_):
            h.e=min(h.e0,h.e+P['regen'])
            acts=2
            if rounds==1 and h.role=='melee': acts-=1  # approach
            for _ in range(acts):
                foes=[c for c in alive(crs) if not (c.kind=='b' and diving)]
                if not foes and not (boss and leurre>0): break
                if h.e<=0: break
                hurt=[x for x in alive(H_) if x.pv<=x.pv0/2]
                if h.c=='tisseur' and hurt:
                    t=min(hurt,key=lambda x:x.pv); t.pv=min(t.pv0,t.pv+d(4)); h.e-=1; st_['heal']+=1; continue
                if h.c=='pisteur' and boss and illum==0 and rounds%2==1: illum=2; h.e-=1; continue
                m=h.m-h.malus
                # target choice
                if boss and leurre>0 and h.role=='ranged':
                    h.e-=1
                    if hit(m-5+illum*0): leurre-=d(6 if h.c!='tisseur' else 4)
                    continue
                if not foes: break
                tgt=min(foes,key=lambda c:c.pv)
                bonus=2 if (illum and tgt.kind in 'be') else 0
                if h.c=='elementaliste' and len(foes)>=3:
                    h.e-=1
                    for c in sorted(foes,key=lambda c:c.pv)[:3]: c.pv-=d(4)   # Gravillons auto
                    continue
                if h.c=='elementaliste' and len(foes)==2:
                    h.e-=1
                    for c in foes:
                        if hit(m-c.df): c.pv-=d(4)
                    continue
                die={'rempart':6,'tisseur':4,'lamesort':8,'pisteur':6,'elementaliste':6,'passeombre':6}[h.c]
                h.e-=1
                if hit(m-tgt.df+bonus):
                    tgt.pv-=d(die)
                    if tgt.pv<=0 and tgt.kind=='v' and h.role=='melee': h.pv-=d(6)
            h.malus=0
            if h.pv<=0: h.down=True
        if boss:
            lb=[c for c in crs if c.kind=='b'][0]
            if lb.pv>0 and lb.pv<=lb.pv0/2 and not phase2:
                phase2=True; diving=True; dark=True
                crs+= [C('cracheur',n),C('cracheur',n)]
            elif diving: diving=False
        if leurre<0: leurre=0
        # creatures
        for c in alive(crs):
            if c.kind=='v': continue
            if c.kind=='b' and diving: continue
            hs=alive(H_)
            if not hs: break
            front=[h for h in hs if h.role=='melee'] or hs
            if c.kind in 'fb' or (c.kind=='e' and rounds%2==0): t=min(hs,key=lambda h:h.pv)
            else: t=min(front,key=lambda h:h.pv)
            if hit(c.att-t.df):
                t.pv-=d(c.dmg)
                if c.kind=='f' or (c.kind=='b' and leurre>0): st_['charge']-=1; st_['stolen']+=1
                if c.kind=='r': t.malus=2
                if t.pv<=0: t.down=True
        # chrysalides
        for c in list(crs):
            if P['chrys'] and c.kind=='c' and c.pv>0:
                c.age+=1
                if c.age>=3: c.pv=0; crs.append(C('phalene',n)); st_['chrys']+=1
        st_['charge']-= 2 if (brume) else 1
        if dark: st_['charge']-=1
        if st_['charge']<=0: return rounds
    return rounds
def mission(party,route,start=16,blaireau_p=0.5):
    n=len(party); Hs=[H(c) for c in party]
    s={'charge':start,'heal':0,'stolen':0,'chrys':0,'rounds':{},'fail':None}
    def explore(cost=1):
        s['charge']-=cost
        for h in alive(Hs): h.e=min(h.e0,h.e+1)
    def F(name,crs,**kw):
        r=fight(Hs,crs,n,s,**kw); s['rounds'][name]=r
        for h in alive(Hs): h.pv=min(h.pv0,h.pv+round(h.pv0*P['heal']))
        if not alive(Hs): s['fail']='héros' ; return False
        if s['charge']<=0: s['fail']='lanterne'; return False
        return True
    explore()                         # T1
    explore()                         # T2
    if R.random()<0.5 and not F('T2',[C('chenille',n) for _ in range(3)]): return Hs,s
    explore()                         # T3
    if R.random() < max(h.inst for h in Hs)/20: s['charge']+=2
    explore()                         # T4
    if not F('T4',[C('chenille',n) for _ in range(P['t4'])]+[C('phalene',n)]): return Hs,s
    if route=='raccourci':
        explore(2)
        if not F('T5',[C('phalene',n)],brume=True): return Hs,s
    else:
        explore()
        crs=[C('cracheur',n) for _ in range(4)]+[C('vesse',n) for _ in range(3)]
        if R.random()<blaireau_p: crs.append(C('blaireau',n))
        if not F('T6',crs): return Hs,s
        s['charge']+=min(4,len(alive(Hs)))
    # repos avant le boss : Eclats + soins du Tisseur
    deficit=max(h.e0-h.e for h in alive(Hs))
    turns=max(0,min(deficit,s['charge']-9))
    for _ in range(turns):
        explore()
        t=[h for h in Hs if h.c=='tisseur' and not h.down]
        if t and t[0].e>0:
            low=min(alive(Hs),key=lambda h:h.pv); low.pv=min(low.pv0,low.pv+d(4)); t[0].e-=1
    explore()                         # T7
    s['charge_avant_boss']=s['charge']
    if not F('T7',[C('lumivore',n)],boss=True): return Hs,s
    if alive([c for c in []]): pass
    return Hs,s
def run(party,route,N=4000,start=16):
    ok=0; fails={'héros':0,'lanterne':0,'timeout':0}; down=[]; ch=[]; br=[]; rr={}; stolen=[]
    for _ in range(N):
        Hs,s=mission(party,route,start)
        won = s['fail'] is None and alive(Hs) and s['rounds'].get('T7',99)<=15
        if won: ok+=1; ch.append(s['charge'])
        elif s['fail']: fails[s['fail']]+=1
        else: fails['timeout']+=1
        down.append(sum(h.down for h in Hs)); stolen.append(s['stolen'])
        for k,v in s['rounds'].items(): rr.setdefault(k,[]).append(v)
        if 'charge_avant_boss' in s: br.append(s['charge_avant_boss'])
    print(f"{'+'.join(party):55s} {route:9s} réussite {ok/N:5.0%} | échecs héros {fails['héros']/N:4.0%} lanterne {fails['lanterne']/N:4.0%} | héros à terre moy {st.mean(down):.1f} | charge avant boss {st.mean(br):.1f} | charge finale {st.mean(ch) if ch else 0:.1f} | " + ' '.join(f"{k}:{st.mean(v):.1f}r" for k,v in sorted(rr.items())))

def table(label,start):
    print('###',label)
    for p in [['lamesort','tisseur'],['rempart','elementaliste'],['rempart','tisseur','lamesort','elementaliste'],['rempart','tisseur','lamesort','elementaliste','pisteur','passeombre']]:
        for r in ['raccourci','detour']:
            run(p,r,N=3000,start=start)
