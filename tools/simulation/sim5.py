import random, statistics as st
R=random.Random(7)
def d(n): return R.randint(1,n)
def hit(s):
    r=d(20); return r==1 or (r!=20 and r<=s)
CLS={'rempart':(12,3,10,2,9,'melee',6),'tisseur':(9,1,11,4,11,'ranged',4),'lamesort':(10,2,12,3,9,'melee',8),
     'pisteur':(9,1,12,3,11,'ranged',6),'elementaliste':(7,0,12,5,10,'ranged',6),'passeombre':(9,2,11,3,11,'melee',6)}
DECK=['seve']*5+['cristal']*4+['eclat']*4+['bulle']*2+['talisman','bottes','pierre','bourse']+['curio']*4
EQUIP={'talisman','bottes','pierre','bourse'}
class H:
    def __init__(s,c,bonus=0):
        s.c=c; s.pv0,s.df,s.m,s.e0,s.inst,s.role,s.die=CLS[c]; s.e0+=bonus; s.dmgb=0; s.pv=s.pv0; s.e=s.e0; s.malus=0; s.down=False
        s.bag=['soin','souffle']
    def give(s,o):
        if o=='talisman': s.df+=1
        elif o=='pierre': s.m+=1
        elif o=='bourse': s.e0+=1; s.e+=1
        elif o=='bottes': pass
        elif len(s.bag)<3: s.bag.append(o); return True
        else: return False
        return True
class C:
    def __init__(s,k,n,P):
        T={'chenille':(8,0,3,4,'c'),'phalene':(11,1,6,4,'f'),'cracheur':(10,2,5,4,'r'),'vesse':(0,0,4,6,'v'),
           'blaireau':(12,3,14,8,'e'),'lumivore':P['boss']}
        s.k=k; s.att,s.df,pv,s.dmg,s.kind=T[k]
        f=P['scale_boss'] if s.kind=='b' else P['scale']
        s.pv=max(1,round(pv*P['base2']*(1+f*(n-2)))); s.pv0=s.pv; s.age=0
def alive(L): return [x for x in L if (x.pv>0 if isinstance(x,C) else not x.down)]
def use_items(h,P):
    # returns True if an action was spent on an item
    if h.pv<=0.4*h.pv0:
        for o,amt in (('soin',6),('seve',None)):
            if o in h.bag: h.bag.remove(o); h.pv=min(h.pv0,h.pv+(amt or d(6))); return True
    if h.e<=0:
        if 'eclat' in h.bag: h.bag.remove('eclat'); h.e=min(h.e0,h.e+2); return True
        if 'souffle' in h.bag: h.bag.remove('souffle'); h.e=h.e0; return True
    return False
def fight(Hs,crs,n,s,P,brume=False,boss=False):
    rounds=0; leurre=6 if boss else 0; phase2=False; dark=0; diving=False
    while alive(Hs) and alive(crs):
        rounds+=1
        if rounds>15: s['timeout']=True; break
        illum=0
        for h in alive(Hs):
            h.e=min(h.e0,h.e+P['regen'])
            acts=2-(1 if rounds==1 and h.role=='melee' else 0)
            for _ in range(acts):
                if use_items(h,P): continue
                foes=[c for c in alive(crs) if not (c.kind=='b' and diving)]
                if (not foes and not leurre) or h.e<=0: break
                hurt=[x for x in alive(Hs) if x.pv<=x.pv0/2]
                if h.c=='tisseur' and hurt:
                    t=min(hurt,key=lambda x:x.pv); t.pv=min(t.pv0,t.pv+d(4)); h.e-=1; continue
                if h.c=='pisteur' and boss and illum==0: illum=2; h.e-=1; continue
                m=h.m-h.malus
                if boss and leurre>0 and h.role=='ranged':
                    h.e-=1
                    if hit(m-5): leurre-=d(h.die)+h.dmgb
                    continue
                if not foes: break
                tgt=min(foes,key=lambda c:c.pv)
                bonus=2 if (illum and tgt.kind in 'be') else 0
                h.e-=1
                if h.c=='elementaliste' and len(foes)>=3:
                    for c in sorted(foes,key=lambda c:c.pv)[:3]: c.pv-=d(4)+h.dmgb
                    continue
                if h.c=='elementaliste' and len(foes)==2:
                    for c in foes:
                        if hit(m-c.df): c.pv-=d(4)+h.dmgb
                    continue
                if hit(m-tgt.df+bonus):
                    tgt.pv-=d(h.die)+h.dmgb
                    if tgt.pv<=0 and tgt.kind=='v' and h.role=='melee': h.pv-=d(6)
                    if tgt.pv<=0 and tgt.kind=='e': s['drop']+=1
            h.malus=0
            if h.pv<=0: h.down=True
        leurre=max(0,leurre)
        if boss:
            lb=[c for c in crs if c.kind=='b'][0]
            if lb.pv>0 and lb.pv<=lb.pv0/2 and not phase2:
                phase2=True; diving=True; dark=P['dark']; crs+=[C('cracheur',n,P),C('cracheur',n,P)]
            elif diving: diving=False
        stole=False
        for c in alive(crs):
            if c.kind=='v' or (c.kind=='b' and diving): continue
            hs=alive(Hs)
            if not hs: break
            front=[h for h in hs if h.role=='melee'] or hs
            t=min(hs,key=lambda h:h.pv) if (c.kind in 'fb' or (c.kind=='e' and rounds%2==0)) else min(front,key=lambda h:h.pv)
            if hit(c.att-t.df):
                t.pv-=d(c.dmg)
                if c.kind=='f': s['charge']-=1
                if c.kind=='b' and leurre>0 and (P['leurre']=='hit' or not stole): s['charge']-=1; stole=True
                if c.kind=='r': t.malus=2
                if t.pv<=0: t.down=True
            elif c.kind=='b' and leurre>0 and P['leurre']=='round' and not stole: s['charge']-=1; stole=True
        for c in list(crs):
            if P.get('chrys',True) and c.kind=='c' and c.pv>0:
                c.age+=1
                if c.age>=3: c.pv=0; crs.append(C('phalene',n,P))
        s['charge']-=2 if brume else 1
        if dark: s['charge']-=1; dark-=1 if dark<90 else 0
        if s['charge']<=0: return rounds
    return rounds
def mission(party,route,P):
    n=len(party); Hs=[H(c,P.get('ecl_bonus',0)) for c in party]
    deck=DECK[:]; R.shuffle(deck)
    if n==2:
        for h in Hs: h.pv0+=P.get('duo_pv',0); h.pv=h.pv0; h.dmgb=P.get('duo_dmg',0)
    s={'charge':P['start'],'drop':0,'rounds':{},'fail':None,'timeout':False,'items':0}
    def loot(o):
        s['items']+=1
        if o=='cristal': s['charge']+=2; return
        if o=='curio': return
        order=sorted(alive(Hs),key=lambda h:(o=='talisman' and h.role!='melee', o=='pierre' and h.die<8, o=='bourse' and h.c not in('elementaliste','tisseur')))
        for h in order:
            if h.give(o): return
    def search():
        best=max(alive(Hs),key=lambda h:h.inst)
        if hit(best.inst) and deck: loot(deck.pop())
    def explore(cost=1):
        s['charge']-=cost
        for h in alive(Hs): h.e=min(h.e0,h.e+1)
    def F(name,crs,**kw):
        s['rounds'][name]=fight(Hs,crs,n,s,P,**kw)
        while s['drop']>0:
            s['drop']-=1; eq=[o for o in deck if o in EQUIP]
            if eq: deck.remove(eq[0]); loot(eq[0])
        for h in alive(Hs): h.pv=min(h.pv0,h.pv+round(h.pv0*P['heal']))
        # soins hors combat avec les objets
        for h in alive(Hs):
            while h.pv<=0.5*h.pv0 and 'seve' in h.bag: h.bag.remove('seve'); h.pv=min(h.pv0,h.pv+d(6))
        if not alive(Hs): s['fail']='héros'; return False
        if s['charge']<=0: s['fail']='lanterne'; return False
        if s['timeout']: s['fail']='trop long'; return False
        return True
    explore(); search()                                   # T1
    explore(); search()                                   # T2
    if R.random()<0.5 and not F('T2',[C('chenille',n,P) for _ in range(3)]): return Hs,s
    explore(); search()                                   # T3
    explore()                                             # T4
    if not F('T4',[C('chenille',n,P) for _ in range(5)]+[C('phalene',n,P)]): return Hs,s
    search()
    if route=='raccourci':
        explore(2)
        if not F('T5',[C('phalene',n,P)],brume=True): return Hs,s
        search()
    else:
        explore()
        crs=[C('cracheur',n,P) for _ in range(P.get('t6c',4))]+[C('vesse',n,P) for _ in range(P.get('t6v',3))]
        if R.random()<P.get('blaireau_p',0.5): crs.append(C('blaireau',n,P))
        if not F('T6',crs): return Hs,s
        s['charge']+=min(4,len(alive(Hs))); search()
    deficit=max(h.e0-h.e for h in alive(Hs))
    for _ in range(max(0,min(deficit,s['charge']-P['buffer']))):
        explore()
        t=[h for h in Hs if h.c=='tisseur' and not h.down]
        if t and t[0].e>0:
            low=min(alive(Hs),key=lambda h:h.pv); low.pv=min(low.pv0,low.pv+d(4)); t[0].e-=1
    explore()
    s['avant_boss']=s['charge']
    if not F('T7',[C('lumivore',n,P)],boss=True): return Hs,s
    return Hs,s
PARTIES=[['lamesort','tisseur'],['rempart','elementaliste'],['pisteur','passeombre'],
         ['rempart','tisseur','elementaliste'],['lamesort','pisteur','passeombre'],
         ['rempart','tisseur','lamesort','elementaliste'],['pisteur','passeombre','lamesort','tisseur'],
         ['rempart','tisseur','lamesort','elementaliste','pisteur'],['tisseur','lamesort','elementaliste','pisteur','passeombre']]
def table(P,N=3000):
    print(f"{'groupe':44s} {'route':9s} réussite | échec héros / lanterne / trop long | à terre | charge avant boss → fin | rounds par combat")
    for p in PARTIES:
        for route in ['raccourci','detour']:
            ok=0; f={'héros':0,'lanterne':0,'trop long':0}; down=[]; ab=[]; fin=[]; rr={}
            for _ in range(N):
                Hs,s=mission(p,route,P)
                if s['fail']: f[s['fail']]+=1
                else: ok+=1; fin.append(s['charge'])
                down.append(sum(h.down for h in Hs))
                if 'avant_boss' in s: ab.append(s['avant_boss'])
                for k,v in s['rounds'].items(): rr.setdefault(k,[]).append(v)
            m=lambda L: st.mean(L) if L else 0
            print(f"{'+'.join(x[:4] for x in p):44s} {route:9s} {ok/N:7.0%} | {f['héros']/N:4.0%} / {f['lanterne']/N:4.0%} / {f['trop long']/N:4.0%} | {m(down):.1f} | {m(ab):4.1f} → {m(fin):4.1f} | "+' '.join(f"{k}:{m(v):.1f}" for k,v in sorted(rr.items())))
BASE=dict(start=16,regen=1,heal=0.0,boss=(13,3,24,10,'b'),leurre='hit',dark=99,scale=0.25,scale_boss=0.5,base2=1.0,buffer=9)
NEW=dict(start=28,regen=2,heal=0.5,boss=(11,3,24,6,'b'),leurre='round',dark=2,scale=0.35,scale_boss=0.5,base2=0.85,buffer=12)
if __name__=='__main__':
    print('### 1. Règles actuelles + objets (potions de départ, paquet de 23 cartes)'); table(BASE)
    print('\n### 2. Objets + les 5 changements proposés'); table(NEW)
