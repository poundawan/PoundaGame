import random, statistics as st, itertools, sys
R=random.Random(11)
def d(n): return R.randint(1,n)
def hit(s):
    r=d(20); return r==1 or (r!=20 and r<=s)
CLS={'rempart':(12,3,10,2,9,'melee',6),'tisseur':(9,1,11,4,11,'ranged',6),'lamesort':(10,2,12,3,9,'melee',8),
     'pisteur':(9,1,12,3,11,'ranged',8),'elementaliste':(7,0,12,5,10,'ranged',6),'passeombre':(9,2,11,3,11,'melee',6)}
FAMS=['gecko','hibou','lynx','chacal','tatou','panda']
DECK=['seve']*5+['cristal']*4+['eclat']*4+['bulle']*2+['talisman','bottes','pierre','bourse']+['curio']*4
EQUIP={'talisman','bottes','pierre','bourse'}
class H:
    def __init__(s,c,P,fam):
        s.c=c; s.pv0,s.df,s.m,s.e0,s.inst,s.role,s.die=CLS[c]; s.e0+=P['ecl_bonus']; s.dmgb=0
        s.pv=s.pv0; s.e=s.e0; s.malus=0; s.down=False; s.bag=['soin','souffle']; s.fam=fam
    def give(s,o):
        if o=='talisman': s.df+=1
        elif o=='pierre': s.m+=1
        elif o=='bourse': s.e0+=1; s.e+=1
        elif o=='bottes': pass
        elif len(s.bag)<3: s.bag.append(o)
        else: return False
        return True
class C:
    def __init__(s,k,n,P):
        T={'chenille':(8,0,3,4,'c'),'phalene':(11,1,6,4,'f'),'cracheur':(10,2,5,4,'r'),'vesse':(0,0,4,6,'v'),
           'blaireau':(12,3,14,8,'e'),'lumivore':(11,3,24,6,'b')}
        s.k=k; s.att,s.df,pv,s.dmg,s.kind=T[k]
        f=P['scale_boss'] if s.kind=='b' else P['scale']
        s.pv=max(1,round(pv*P['base2']*(1+f*(n-2)))); s.pv0=s.pv; s.sleep=False; s.lured=None
def alive(L): return [x for x in L if (x.pv>0 if isinstance(x,C) else not x.down)]
def fight(Hs,crs,n,s,P,brume=False,boss=False,big=False):
    rounds=0; leurre=6 if boss else 0; phase2=False; dark=0; diving=False
    useF=P['fams']
    atout={id(h):useF for h in Hs}; famrest={id(h):0 for h in Hs}
    while alive(Hs) and alive(crs):
        rounds+=1
        if rounds>15: s['timeout']=True; break
        illum=0; blind=False; immune=set(); dodge=set(); blocked=0; chacal_bonus={}
        for h in alive(Hs):
            h.e=min(h.e0,h.e+1)
            acts=2-(1 if rounds==1 and h.role=='melee' else 0)
            fam_ok = useF and famrest[id(h)]==0
            # atouts (gratuits, 1 fois par combat)
            if atout[id(h)] and (big or boss or h.pv<=0.5*h.pv0):
                f=h.fam
                if f=='gecko' and len(alive(crs))>=2: blind=True; atout[id(h)]=False
                elif f=='tatou' and h.pv<=0.5*h.pv0: immune.add(id(h)); atout[id(h)]=False
                elif f=='lynx' and h.pv<=0.6*h.pv0: dodge.add(id(h)); atout[id(h)]=False
                elif f=='panda' and h.e<=1:
                    h.e=min(h.e0,h.e+1); o=[x for x in alive(Hs) if x is not h]
                    if o: m_=min(o,key=lambda x:x.e); m_.e=min(m_.e0,m_.e+1)
                    atout[id(h)]=False
                elif f=='chacal': chacal_bonus[id(h)]=True; atout[id(h)]=False
                elif f=='hibou' and h.role=='ranged': chacal_bonus[id(h)]='hibou'; atout[id(h)]=False
            for a in range(acts):
                # objets
                if h.pv<=0.4*h.pv0 and any(o in h.bag for o in ('soin','seve')):
                    o='soin' if 'soin' in h.bag else 'seve'; h.bag.remove(o); h.pv=min(h.pv0,h.pv+(6 if o=='soin' else d(6))); continue
                if h.e<=0 and 'eclat' in h.bag: h.bag.remove('eclat'); h.e=min(h.e0,h.e+2); continue
                if h.e<=0 and 'souffle' in h.bag and (boss or big): h.bag.remove('souffle'); h.e=h.e0; continue
                foes=[c for c in alive(crs) if not (c.kind=='b' and diving)]
                if not foes and not leurre: break
                # mission du familier (sans Éclat), si plus d'Éclat ou au 1er round d'un gros combat
                if fam_ok and foes and (h.e<=0 or (rounds==1 and (big or boss) and h.fam in ('panda','tatou','lynx'))):
                    f=h.fam; done=True
                    if f in ('chacal','lynx'):
                        t=min(foes,key=lambda c:c.pv)
                        if hit(h.m-t.df): t.pv-=d(4)+h.dmgb
                        if f=='lynx': t.lured=id(h)
                    elif f=='panda':
                        cand=[c for c in foes if c.kind not in 'bv']
                        if cand: max(cand,key=lambda c:c.att).sleep=True
                        else: done=False
                    elif f=='tatou': blocked+=1
                    else: done=False
                    if done: fam_ok=False; continue
                if h.e<=0: break
                hurt=[x for x in alive(Hs) if x.pv<=x.pv0/2]
                if h.c=='tisseur' and hurt:
                    t=min(hurt,key=lambda x:x.pv); t.pv=min(t.pv0,t.pv+d(6)); h.e-=1; continue
                if h.c=='pisteur' and boss and illum==0: illum=2; h.e-=1; continue
                m=h.m-h.malus; b2=0
                if chacal_bonus.get(id(h))=='hibou': b2=2
                if boss and leurre>0 and h.role=='ranged':
                    h.e-=1
                    if hit(m-5+b2): leurre-=d(h.die)+h.dmgb
                    continue
                if not foes: break
                tgt=min(foes,key=lambda c:c.pv)
                bonus=(2 if (illum and tgt.kind in 'be') else 0)+b2
                h.e-=1
                if h.c=='elementaliste' and len(foes)>=3:
                    for c in sorted(foes,key=lambda c:c.pv)[:3]:
                        if hit(m-c.df+b2): c.pv-=d(4)+h.dmgb
                    continue
                if h.c=='elementaliste' and len(foes)==2:
                    for c in foes:
                        if hit(m-c.df+b2): c.pv-=d(4)+h.dmgb
                    continue
                if hit(m-tgt.df+bonus):
                    dmg=d(h.die)+h.dmgb
                    if chacal_bonus.get(id(h)) is True: dmg+=d(4); chacal_bonus[id(h)]=False
                    tgt.pv-=dmg
                    if tgt.pv<=0 and tgt.kind=='v' and h.role=='melee': h.pv-=d(6)
                    if tgt.pv<=0 and tgt.kind=='e': s['drop']+=1
            h.malus=0
            if h.pv<=0: h.down=True
        leurre=max(0,leurre)
        if boss:
            lb=[c for c in crs if c.kind=='b'][0]
            if lb.pv>0 and lb.pv<=lb.pv0/2 and not phase2:
                phase2=True; diving=True; dark=2; crs+=[C('cracheur',n,P),C('cracheur',n,P)]
            elif diving: diving=False
        stole=False
        for h in Hs:
            if famrest[id(h)]>0: famrest[id(h)]-=1
        for c in alive(crs):
            if c.kind=='v' or (c.kind=='b' and diving): continue
            if c.sleep: c.sleep=False; continue
            hs=alive(Hs)
            if not hs: break
            if c.lured is not None:
                owner=c.lured; c.lured=None
                if hit(c.att-2): famrest[owner]=1
                continue
            front=[h for h in hs if h.role=='melee'] or hs
            t=min(hs,key=lambda h:h.pv) if (c.kind in 'fb' or (c.kind=='e' and rounds%2==0)) else min(front,key=lambda h:h.pv)
            if blocked and t.role=='ranged' and c.kind in 'ce': blocked-=1; continue
            att=c.att-(3 if blind else 0)-(2 if id(t) in dodge else 0)
            if hit(att-t.df):
                if id(t) not in immune: t.pv-=d(c.dmg)
                if c.kind=='f': s['charge']-=1
                if c.kind=='b' and leurre>0 and not stole: s['charge']-=1; stole=True
                if c.kind=='r': t.malus=2
                if t.pv<=0: t.down=True
            elif c.kind=='b' and leurre>0 and not stole: s['charge']-=1; stole=True
        s['charge']-=2 if brume else 1
        if dark: s['charge']-=1; dark-=1
        if s['charge']<=0: return rounds
    return rounds
def mission(party,route,P):
    n=len(party); fams=[R.choice(FAMS) for _ in party]
    Hs=[H(c,P,f) for c,f in zip(party,fams)]
    if n==2:
        for h in Hs: h.pv0+=3; h.pv=h.pv0; h.dmgb=1
    deck=DECK[:]; R.shuffle(deck)
    s={'charge':P['start'],'drop':0,'fail':None,'timeout':False,'fams':fams}
    def loot(o):
        if o=='cristal': s['charge']+=2; return
        if o=='curio': return
        order=sorted(alive(Hs),key=lambda h:(o=='talisman' and h.role!='melee', o=='pierre' and h.die<8, o=='bourse' and h.c not in('elementaliste','tisseur')))
        for h in order:
            if h.give(o): return
    def search():
        best=max(alive(Hs),key=lambda h:h.inst)
        tries=2 if (P['fams'] and any(h.fam=='gecko' for h in alive(Hs))) else 1
        for _ in range(tries):
            if hit(best.inst) and deck: loot(deck.pop()); return
    def explore(cost=1):
        s['charge']-=cost
        for h in alive(Hs): h.e=min(h.e0,h.e+1)
    def F(crs,**kw):
        fight(Hs,crs,n,s,P,**kw)
        while s['drop']>0:
            s['drop']-=1; eq=[o for o in deck if o in EQUIP]
            if eq: deck.remove(eq[0]); loot(eq[0])
        for h in alive(Hs): h.pv=min(h.pv0,h.pv+round(h.pv0*0.5))
        for h in alive(Hs):
            while h.pv<=0.5*h.pv0 and 'seve' in h.bag: h.bag.remove('seve'); h.pv=min(h.pv0,h.pv+d(6))
        if not alive(Hs): s['fail']='héros'; return False
        if s['charge']<=0: s['fail']='lanterne'; return False
        if s['timeout']: s['fail']='long'; return False
        return True
    explore(); search(); explore(); search()
    if R.random()<0.5 and not F([C('chenille',n,P) for _ in range(3)]): return s
    explore(); search(); explore()
    if not F([C('chenille',n,P) for _ in range(5)]+[C('phalene',n,P)],big=True): return s
    search()
    if route=='raccourci':
        explore(2)
        if not F([C('phalene',n,P)],brume=True): return s
        search()
    else:
        explore()
        crs=[C('cracheur',n,P) for _ in range(4)]+[C('vesse',n,P) for _ in range(3)]
        if R.random()<0.5: crs.append(C('blaireau',n,P))
        if not F(crs,big=True): return s
        s['charge']+=2*min(4,len(alive(Hs))); search()
        eq=[o for o in deck if o in EQUIP]
        if eq: deck.remove(eq[0]); loot(eq[0])
    deficit=max(h.e0-h.e for h in alive(Hs))
    for _ in range(max(0,min(deficit,s['charge']-12))):
        explore()
        t=[h for h in Hs if h.c=='tisseur' and not h.down]
        if t and t[0].e>0:
            low=min(alive(Hs),key=lambda h:h.pv); low.pv=min(low.pv0,low.pv+d(4)); t[0].e-=1
    explore()
    if not F([C('lumivore',n,P)],boss=True): return s
    return s
P0=dict(start=30,ecl_bonus=2,base2=0.75,scale=0.25,scale_boss=0.5,fams=True)
AB={'rempart':'Rem','tisseur':'Tis','lamesort':'Lam','pisteur':'Pis','elementaliste':'Élé','passeombre':'Pas'}
if __name__=='__main__':
    N=int(sys.argv[1]) if len(sys.argv)>1 else 800
    res={}
    famstat={f:[0,0] for f in FAMS}; famstat_no=None
    for k in (2,3,4,5):
        for combo in itertools.combinations(list(CLS),k):
            for route in ('raccourci','detour'):
                for fams in (True,False):
                    P=dict(P0); P['fams']=fams; ok=0
                    for _ in range(N):
                        s=mission(list(combo),route,P); w=s['fail'] is None; ok+=w
                        if fams:
                            for f in set(s['fams']): famstat[f][0]+=w; famstat[f][1]+=1
                    res[(combo,route,fams)]=ok/N
    import json
    json.dump({'|'.join(k[0])+'|'+k[1]+'|'+str(k[2]):v for k,v in res.items()},open('res8.json','w'))
    for k in (2,3,4,5):
        for route in ('raccourci','detour'):
            for fams in (True,False):
                vals=[(v,c) for (c,r,f),v in res.items() if len(c)==k and r==route and f==fams]
                vs=[v for v,_ in vals]; lo=min(vals); hi=max(vals)
                print(f"{k} héros · {route:9s} · familiers {'oui' if fams else 'non'} : moyenne {st.mean(vs):4.0%} | min {lo[0]:4.0%} ({'+'.join(AB[x] for x in lo[1])}) | max {hi[0]:4.0%} ({'+'.join(AB[x] for x in hi[1])})")
    print('\nRéussite moyenne quand le familier est présent dans le groupe :')
    for f,(w,t) in famstat.items(): print(f"  {f:7s} {w/t:5.1%}")
