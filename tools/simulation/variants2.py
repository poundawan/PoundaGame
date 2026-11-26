import io,contextlib,re
def go(label,start,**kw):
    g={}; exec(open('sim2.py').read(),g)
    g['P'].update({k:v for k,v in kw.items() if k in g['P']})
    if 'boss' in kw: g['CR']['lumivore']=kw['boss']
    buf=io.StringIO()
    with contextlib.redirect_stdout(buf): g['table'](label,start)
    print('###',label)
    for l in buf.getvalue().splitlines()[1:]:
        p=l.split()[0]; r=l.split()[1]
        m=re.search(r'réussite\s+(\d+%).*héros\s+(\d+%) lanterne\s+(\d+%).*charge avant boss ([\d.]+).*charge finale ([\d.]+) \| (.*)',l)
        print(f"{p[:45]:45s} {r:9s} réussite {m.group(1):>4s} · échec héros {m.group(2):>4s} · échec lanterne {m.group(3):>4s} · avant boss {m.group(4):>5s} · {m.group(6)}")
B=(11,3,24,6,'b')
go('C30: lanterne 30, soin 50% après combat, boss att 11 d6, regen 2',30,heal=0.5,boss=B,regen=2)
go('E: lanterne 26, soin 50%, boss att 11 d6, regen 1 (règle actuelle des Éclats)',26,heal=0.5,boss=B,regen=1)
go('F: lanterne 26, soin 50%, boss att 11 d6, regen 2',26,heal=0.5,boss=B,regen=2)
