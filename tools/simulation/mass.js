const { chromium } = require('playwright');const fs=require('fs');
(async () => {
 const b = await chromium.launch(); const p = await b.newPage();
 const errs=[]; p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/user/PoundaGame/jeu/index.html'); await p.waitForTimeout(300);
 const N=+process.argv[2]||60;
 const res = await p.evaluate((N)=>{
  const C=['rempart','tisseur','lamesort','pisteur','elementaliste','passeombre'],RA=['humain','marque','saurien','oiseau','loutre','astreen'],FA=['gecko','hibou','lynx','chacal','tatou','panda'];
  const combos=[];const rec=(st,k,acc)=>{if(acc.length===k){combos.push(acc.slice());return;}for(let i=st;i<C.length;i++){acc.push(C[i]);rec(i+1,k,acc);acc.pop();}};
  for(const k of [2,3,4,5])rec(0,k,[]);
  const out=[];const pick=(a)=>a[Math.floor(Math.random()*a.length)];
  for(const cb of combos)for(let i=0;i<N;i++){const cfg=cb.map((c,j)=>({name:'H'+j,cls:c,race:pick(RA),fam:pick(FA)}));
   const r=window.PG_HEADLESS(cfg);out.push({cls:cb,races:cfg.map(c=>c.race),fams:cfg.map(c=>c.fam),...r});}
  return out;},N);
 fs.writeFileSync('mass.json',JSON.stringify(res));
 console.log('parties',res.length,'erreurs',JSON.stringify(errs.slice(0,3)));
 await b.close();
})();
