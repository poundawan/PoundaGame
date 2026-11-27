const { chromium } = require('playwright');
const VARIANTS=JSON.parse(process.argv[3]);const N=+process.argv[2];
(async () => {
 const b = await chromium.launch(); const errs=[];
 for(const V of VARIANTS){
  const p = await b.newPage(); p.on('pageerror',e=>errs.push(e.message));
  await p.goto('file:///home/user/PoundaGame/jeu/index.html'); await p.waitForTimeout(200);
  const out=await p.evaluate(([V,N])=>{window.PG_TUNE(V);
   const C=['rempart','tisseur','lamesort','pisteur','elementaliste','passeombre'],RA=['humain','marque','saurien','oiseau','loutre','astreen'],FA=['gecko','hibou','lynx','chacal','tatou','panda'];
   const combos=[];const rec=(st,k,acc)=>{if(acc.length===k){combos.push(acc.slice());return;}for(let i=st;i<C.length;i++){acc.push(C[i]);rec(i+1,k,acc);acc.pop();}};
   for(const k of [2,3,4,5])rec(0,k,[]);const pick=(a)=>a[Math.floor(Math.random()*a.length)];const res=[];
   for(const cb of combos)for(let i=0;i<N;i++){const cfg=cb.map((c,j)=>({name:'H'+j,cls:c,race:pick(RA),fam:pick(FA)}));const r=window.PG_HEADLESS(cfg);res.push([cb,r.over==='victoire'?1:0,r.cause,r.charge,r.down,r.route]);}
   return res;},[V,N]);
  const by={};const cls={};
  for(const [cb,w,cause,ch,down,route] of out){const k=cb.length;(by[k]=by[k]||[]).push([w,cause,ch,down]);for(const c of cb){cls[c]=cls[c]||{};(cls[c][k]=cls[c][k]||[]).push(w);} }
  const pct=a=>Math.round(100*a.reduce((x,y)=>x+y,0)/a.length)+'%';
  const line=Object.keys(by).map(k=>`${k}h ${pct(by[k].map(x=>x[0]))} (lanterne ${pct(by[k].map(x=>x[1]==='lanterne'?1:0))}, héros ${pct(by[k].map(x=>x[1]==='heros'?1:0))})`).join(' · ');
  console.log('### '+V.name+'\n  '+line);
  // duos par classe
  const dl=Object.keys(cls).map(c=>`${c.slice(0,5)} ${pct(cls[c][2])}`).join('  ');console.log('  duos avec : '+dl);
  const tl=Object.keys(cls).map(c=>`${c.slice(0,5)} ${pct(cls[c][3])}`).join('  ');console.log('  trios avec : '+tl);
  await p.close();
 }
 console.log('errors',JSON.stringify(errs.slice(0,3)));await b.close();
})();
