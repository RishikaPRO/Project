import json

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
:root { --a: #4f8dff; --b: #7c5cff; --c: #00e5cc; --d: #ffb432; --g: rgba(255,255,255,.05); --gb: rgba(255,255,255,.1); --t: #f0f4ff; --m: #8899bb; }
html, body { font-family: 'Inter', sans-serif; background: #070b14; color: var(--t); min-height: 100vh; width: 100%; overflow-x: hidden; }
#cv { position: fixed; inset: 0; z-index: 0; pointer-events: none; width: 100vw; height: 100vh; }
.sh { position: relative; z-index: 1; padding: 24px 30px; min-height: 100vh; width: 100%; max-width: 100%; margin: 0 auto; }
.orb { position: fixed; border-radius: 50%; pointer-events: none; z-index: 0; filter: blur(90px); opacity: .15; }
.o1 { width: 500px; height: 500px; background: var(--a); top: -200px; left: -100px; }
.o2 { width: 400px; height: 400px; background: var(--b); bottom: -100px; right: -100px; }
/* Header Elements */
.hdr { display: flex; align-items: center; justify-content: space-between; margin-bottom: 28px; padding: 16px 24px; background: var(--g); border: 1px solid var(--gb); border-radius: 16px; backdrop-filter: blur(20px); flex-wrap: wrap; gap: 15px; }
.logo { display: flex; align-items: center; gap: 10px; }
.li { width: 34px; height: 34px; border-radius: 10px; background: linear-gradient(135deg,var(--a),var(--b)); }
.lt { font-family: 'Inter', sans-serif; font-size: 20px; font-weight: 700; background: linear-gradient(90deg,var(--a),var(--c)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.nav { display: flex; gap: 8px; margin: 0 auto; justify-content: center; }
.nb { padding: 8px 16px; border-radius: 8px; border: 1px solid var(--gb); background: var(--g); color: var(--t); font-size: 13px; cursor: pointer; transition: all .2s; font-family: 'Inter', sans-serif; font-weight: 500; }
.nb:hover, .nb.on { background: rgba(79,141,255,.20); border-color: var(--a); color: #ffffff; }
.av { width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg,var(--b),var(--c)); display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; color: #070b14; }
/* General Grid Frameworks */
.st { font-family: 'Inter', sans-serif; font-size: 22px; font-weight: 700; margin-bottom: 18px; display: flex; align-items: center; gap: 10px; }
.st span { font-size: 12px; font-weight: 400; color: var(--m); background: rgba(79,141,255,.1); border: 1px solid rgba(79,141,255,.2); padding: 3px 12px; border-radius: 20px; }
.mg { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin-bottom: 28px; }
.fc { height: 180px; perspective: 1000px; }
.fi { position: relative; width: 100%; height: 100%; transform-style: preserve-3d; transition: transform .6s cubic-bezier(.4,0,.2,1); cursor: pointer; }
.fc:hover .fi { transform: rotateY(180deg); }
.ff, .fb { position: absolute; inset: 0; backface-visibility: hidden; border-radius: 16px; padding: 20px; border: 1px solid var(--gb); backdrop-filter: blur(20px); }
.fb { transform: rotateY(180deg); overflow-y: auto; background: #0e1629; }
.ci { font-size: 18px; margin-bottom: 6px; opacity: 0.8; }
.cl { font-size: 11px; color: var(--m); text-transform: uppercase; letter-spacing: .8px; margin-bottom: 4px; }
.cv2 { font-family: 'Inter', sans-serif; font-size: 32px; font-weight: 700; }
.ct { font-size: 11px; margin-top: 6px; color: var(--m); }
.bt { font-size: 12px; font-weight: 600; margin-bottom: 8px; color: var(--a); text-transform: uppercase; }
.bs { display: flex; justify-content: space-between; font-size: 12px; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.05); color: var(--m); }
.bs span:last-child { color: var(--t); font-weight: 600; }
.c1 .ff { background: linear-gradient(135deg,rgba(79,141,255,.12),rgba(79,141,255,.03)); }
.c2 .ff { background: linear-gradient(135deg,rgba(124,92,255,.12),rgba(124,92,255,.03)); }
.c3 .ff { background: linear-gradient(135deg,rgba(0,229,204,.12),rgba(0,229,204,.03)); }
.c4 .ff { background: linear-gradient(135deg,rgba(255,180,50,.12),rgba(255,180,50,.03)); }
/* Charts & Display Content */
.cr { display: grid; grid-template-columns: repeat(2, minmax(520px, 1fr)); gap: 28px; margin-bottom: 32px; }
.cc { position: relative; overflow: hidden; border-radius: 22px; padding: 28px; min-height: 360px; color: var(--t); }
.cc::before { content: ""; position: absolute; inset: 0; opacity: 0.12; pointer-events: none; }
.cc h3 { font-size: 16px; font-weight: 700; margin-bottom: 24px; color: #ffffff; text-transform: uppercase; letter-spacing: .08em; }
.cc-dept { background: linear-gradient(180deg, rgba(79,141,255,.18) 0%, rgba(79,141,255,.05) 100%); border: 1px solid rgba(79,141,255,.22); }
.cc-dept::before { background: radial-gradient(circle at top left, rgba(79,141,255,.28), transparent 42%); }
.cc-status { background: linear-gradient(180deg, rgba(124,92,255,.18) 0%, rgba(124,92,255,.05) 100%); border: 1px solid rgba(124,92,255,.22); }
.cc-status::before { background: radial-gradient(circle at top right, rgba(124,92,255,.28), transparent 42%); }
.dw { display: flex; align-items: center; gap: 28px; flex-wrap: wrap; }
.dw canvas { width: 240px !important; height: 240px !important; }
.lg { display: flex; flex-direction: column; gap: 10px; flex: 1; }
.li2 { display: flex; align-items: center; gap: 10px; font-size: 13px; color: #e6efff; }
.ld { width: 12px; height: 12px; border-radius: 50%; }
/* Form Fields & Directory Filtering */
.df { display: flex; gap: 12px; margin-bottom: 20px; }
.di { background: rgba(255,255,255,.04); border: 1px solid var(--gb); border-radius: 10px; padding: 11px 14px; font-size: 13px; color: var(--t); outline: none; flex: 2; transition: border-color 0.2s; }
.di:focus { border-color: var(--a); }
.ds { background: #070b14; border: 1px solid var(--gb); border-radius: 10px; padding: 11px 14px; font-size: 13px; color: var(--t); outline: none; flex: 1; cursor: pointer; }
.eg { display: grid; grid-template-columns: repeat(auto-fill, minmax(290px, 1fr)); gap: 16px; }
.ec { background: var(--g); border: 1px solid var(--gb); border-radius: 16px; padding: 20px; transition: all .3s ease; cursor: pointer; }
.ec:hover { transform: translateY(-4px); border-color: rgba(79,141,255,.3); }
.eh { display: flex; align-items: center; gap: 14px; margin-bottom: 16px; }
.ea { width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-weight: 700; }
.en { font-size: 15px; font-weight: 600; }
.er { font-size: 12px; color: var(--m); }
.ed { display: inline-block; font-size: 11px; padding: 2px 8px; border-radius: 20px; background: rgba(79,141,255,.1); color: var(--a); margin-top: 5px; }
.es { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 14px; }
.ev { background: rgba(255,255,255,.03); border-radius: 8px; padding: 8px; text-align: center; }
.evl { font-size: 10px; color: var(--m); text-transform: uppercase; }
.evv { font-size: 15px; font-weight: 700; margin-top: 3px; }
.sd { width: 8px; height: 8px; border-radius: 50%; display: inline-block; margin-right: 6px; }
.sa { background: #00e5cc; box-shadow: 0 0 8px #00e5cc; }
.sl { background: #ffb432; box-shadow: 0 0 8px #ffb432; }
.ef { margin-top: 16px; padding-top: 12px; border-top: 1px solid var(--gb); display: flex; justify-content: space-between; align-items: center; }
.vb { font-size: 12px; color: var(--a); background: transparent; border: none; cursor: pointer; }
/* Modal Presentation Overlays */
.ov { display: none; position: fixed; inset: 0; background: rgba(7,11,20,.85); z-index: 100; backdrop-filter: blur(12px); align-items: center; justify-content: center; padding: 20px; }
.ov.op { display: flex; }
.dp { background: #0e1629; border: 1px solid var(--gb); border-radius: 20px; padding: 32px; width: 640px; max-width: 100%; max-height: 90vh; overflow-y: auto; position: relative; }
.dc { position: absolute; top: 20px; right: 20px; background: rgba(255,255,255,.05); border: 1px solid var(--gb); color: var(--m); border-radius: 8px; padding: 6px 14px; cursor: pointer; }
.ds2 { margin-top: 24px; padding-top: 18px; border-top: 1px solid var(--gb); }
.ds2 h3 { font-size: 12px; font-weight: 700; color: var(--a); margin-bottom: 14px; text-transform: uppercase; }
.dg { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.df2 { background: rgba(255,255,255,.03); border-radius: 10px; padding: 10px 14px; }
.df2 label { font-size: 10px; color: var(--m); display: block; }
.df2 span { font-size: 13px; font-weight: 500; }
.mr { display: grid; grid-template-columns: repeat(3,1fr); gap: 10px; }
.mb { background: rgba(79,141,255,.06); border: 1px solid rgba(79,141,255,.15); border-radius: 10px; padding: 12px; text-align: center; }
.mb .v { font-size: 22px; font-weight: 700; color: var(--a); }
.mb .l { font-size: 11px; color: var(--m); }
.pm { background: rgba(255,255,255,.03); border: 1px solid var(--gb); border-radius: 12px; padding: 14px; margin-bottom: 10px; }
.pmh { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.pmn { font-size: 14px; font-weight: 600; }
.pmg { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 12px; color: var(--m); }
.pmg span { color: var(--t); display: block; }
.sc { display: none; }
.sc.on { display: block; }
.em { text-align: center; color: var(--m); padding: 40px; font-size: 14px; }
</style>
</head>
<body>
<div class="orb o1"></div><div class="orb o2"></div>
<canvas id="cv"></canvas>
<div class="sh">
<div class="hdr">
<div class="nav">
<button class="nb on" onclick="sw('overview',this)">Overview</button>
<button class="nb" onclick="sw('directory',this)">Directory</button>
</div>
</div>
<div class="sc on" id="tab-overview">
<div class="st">Dashboard <span id="dl"></span></div>
<div class="mg">
<div class="fc c1"><div class="fi"><div class="ff"><div class="ci"></div><div class="cl">Total Employees</div><div class="cv2" style="color:var(--a)" id="m1">—</div><div class="ct"></div></div><div class="fb"><div class="bt">By Department</div><div id="mb1"></div></div></div></div>
<div class="fc c2"><div class="fi"><div class="ff"><div class="ci"></div><div class="cl">Total Projects</div><div class="cv2" style="color:var(--b)" id="m2">—</div><div class="ct"></div></div><div class="fb"><div class="bt">By Status</div><div id="mb2"></div></div></div></div>
<div class="fc c3"><div class="fi"><div class="ff"><div class="ci"></div><div class="cl">Leave This Month</div><div class="cv2" style="color:var(--c)" id="m3">—</div><div class="ct"></div></div><div class="fb"><div class="bt">Leave Details</div><div id="mb3"></div></div></div></div>
<div class="fc c4"><div class="fi"><div class="ff"><div class="ci"></div><div class="cl">Leave This Year</div><div class="cv2" style="color:var(--d)" id="m4">—</div><div class="ct"></div></div><div class="fb"><div class="bt">Year Stats</div><div id="mb4"></div></div></div></div>
</div>
<div class="cr">
<div class="cc cc-dept"><h3>Department Distribution</h3><div class="dw"><canvas id="dc" width="180" height="180"></canvas><div class="lg" id="dl2"></div></div></div>
<div class="cc cc-status"><h3>Project Status</h3><div class="dw"><canvas id="pc2" width="180" height="180"></canvas><div class="lg" id="pl2"></div></div></div>
</div>
</div>
<div class="sc" id="tab-directory">
<div class="st">Employee Directory <span id="dc2"></span></div>
<div class="cc">
<div class="df"><input class="di" placeholder="Search by name or role…" oninput="fe(this.value)"/><select class="ds" onchange="fd(this.value)" id="dsel"><option value="All">All Departments</option></select></div>
<div class="eg" id="eg"></div>
</div>
</div>
</div>
<div class="ov" id="ov" onclick="if(event.target===this)this.classList.remove('op')">
<div class="dp"><button class="dc" onclick="document.getElementById('ov').classList.remove('op')">✕ Close</button><div id="dcnt"></div></div>
</div>
<script>
const D=__DATA__;
const PAL=["#4f8dff","#7c5cff","#00e5cc","#ffb432","#ff6b9d","#ff8c55","#a78bfa","#34d399"];
const SBC={"In Progress":"ba","Review":"br","Completed":"bd","On Hold":"bh"};
function ini(n){return(n||'').split(' ').map(x=>x[0]||'').join('').toUpperCase().slice(0,2)}
function bs(k,v){return`<div class="bs"><span>${k}</span><span>${v}</span></div>`}
// Build Dashboard Cards Data
const M=D.metrics;
document.getElementById('m1').textContent=M.totalEmployees;
document.getElementById('m2').textContent=M.totalProjects;
document.getElementById('m3').textContent=M.leaveThisMonth;
document.getElementById('m4').textContent=M.leaveThisYear;
document.getElementById('mb1').innerHTML=Object.entries(D.deptCounts).map(([k,v])=>bs(k,v)).join('');
document.getElementById('mb2').innerHTML=Object.entries(D.projStatus).map(([k,v])=>bs(k,v)).join('');
const ol=D.employees.filter(e=>!e.active).length, ac=D.employees.length-ol;
document.getElementById('mb3').innerHTML=bs('Active',ac)+bs('On Leave',ol)+bs('Days Off',M.leaveThisMonth);
const avg=D.employees.length>0?(M.leaveThisYear/D.employees.length).toFixed(1):0;
document.getElementById('mb4').innerHTML=bs('Total Days',M.leaveThisYear)+bs('Avg/Employee',avg)+bs('Avg Remaining',Math.max(0,24-avg).toFixed(1));
document.getElementById('dl').textContent=new Date().toLocaleDateString('en-IN',{month:'long',year:'numeric'});
// Render Charts
function donut(cid,lid,entries){
 const ctx=document.getElementById(cid).getContext('2d');
 new Chart(ctx,{type:'doughnut',data:{labels:entries.map(d=>d.l),datasets:[{data:entries.map(d=>d.v),backgroundColor:entries.map(d=>d.c),borderWidth:0,hoverOffset:5}]},options:{cutout:'72%',plugins:{legend:{display:false}},responsive:false,animation:{duration:1100}}});
 document.getElementById(lid).innerHTML=entries.map(d=>`<div class="li2"><div class="ld" style="background:${d.c}"></div>${d.l}: <strong style="color:var(--t);margin-left:3px">${d.v}</strong></div>`).join('');
}
const projectStatusColors = ["#4f8dff", "#00e5cc"];
setTimeout(()=>{
 const de=Object.entries(D.deptCounts).map(([k,v],i)=>({l:k,v,c:PAL[i%PAL.length]}));
 if(de.length)donut('dc','dl2',de);
 const se=Object.entries(D.projStatus).map(([k,v], i)=>({
   l:k,
   v:v,
   c: projectStatusColors[i % projectStatusColors.length]
 }));
 if(se.length)donut('pc2','pl2',se);
},350);
// Directory Layout Logic
let st2='',df2='All';
function fe(v){st2=v.toLowerCase();render()}
function fd(v){df2=v;render()}
function render(){
 const list=D.employees.filter(e=> (e.name.toLowerCase().includes(st2)||e.role.toLowerCase().includes(st2))&&(df2==='All'||e.dept===df2));
 document.getElementById('dc2').textContent=list.length+' members';
 const g=document.getElementById('eg');
 if(!list.length){g.innerHTML='<div class="em">No employees found.</div>';return}
 g.innerHTML=list.map(e=>`
<div class="ec" onclick='od(${JSON.stringify(e).replace(/'/g, "&apos;")})'>
<div class="eh"><div class="ea" style="background:${e.color}22;color:${e.color}">${ini(e.name)}</div>
<div><div class="en">${e.name}</div><div class="er">${e.role}</div><span class="ed">${e.dept}</span></div></div>
<div class="es">
<div class="ev"><div class="evl">Projects</div><div class="evv" style="color:${e.color}">${e.projects}</div></div>
<div class="ev"><div class="evl">Leave/mo</div><div class="evv" style="color:var(--d)">${e.leaveMonth}</div></div>
<div class="ev"><div class="evl">Remaining</div><div class="evv" style="color:var(--c)">${e.leaveRemaining}</div></div>
</div>
</div>`).join('');
}
// Modal Details Overlay
function od(e){
 const ep=D.projects.filter(p=>p.members.toLowerCase().includes(e.name.toLowerCase()));
 const ph=ep.length?ep.map(p=>`<div class="pm"><div class="pmh"><div class="pmn">${p.name}</div><span class="sb ${SBC[p.status]||'bd'}">${p.status}</span></div><div class="pmg"><div>ID<span>${p.id||'—'}</span></div><div>Type<span>${p.type}</span></div><div>Lang<span>${p.lang||'—'}</span></div><div>Start<span>${p.start}</span></div><div>Release<span>${p.release}</span></div><div>Team<span>${p.team}</span></div></div></div>`).join(''):'<p style="color:var(--m);font-size:13px">No projects assigned.</p>';
 document.getElementById('dcnt').innerHTML=`
<div style="display:flex;align-items:center;gap:12px;margin-bottom:4px">
<div style="width:52px;height:52px;border-radius:13px;background:${e.color}22;color:${e.color};display:flex;align-items:center;justify-content:center;font-size:19px;font-weight:700">${ini(e.name)}</div>
<div><div style="font-size:19px;font-weight:700;font-family:'Inter',sans-serif">${e.name}</div><div style="font-size:12px;color:var(--m);margin-top:1px">${e.role} · ${e.dept}</div></div>
</div>
<div class="ds2"><h3>Contact & Info</h3><div class="dg">
<div class="df2"><label>Employee ID</label><span>${e.empId||'—'}</span></div>
<div class="df2"><label>Username</label><span>${e.username||'—'}</span></div>
<div class="df2"><label>Email</label><span>${e.email||'—'}</span></div>
<div class="df2"><label>Phone</label><span>${e.phone||'—'}</span></div>
<div class="df2"><label>Date of Birth</label><span>${e.dob||'—'}</span></div>
<div class="df2"><label>Date of Joining</label><span>${e.joined||'—'}</span></div>
</div></div>
<div class="ds2"><h3>Leave</h3><div class="mr">
<div class="mb"><div class="v">${e.leaveMonth}</div><div class="l">This Month</div></div>
<div class="mb"><div class="v">${e.leaveYear}</div><div class="l">This Year</div></div>
<div class="mb" style="background:rgba(0,229,204,.08);border-color:rgba(0,229,204,.2)"><div class="v" style="color:var(--c)">${e.leaveRemaining}</div><div class="l">Remaining</div></div>
</div></div>
<div class="ds2"><h3>Projects (${ep.length})</h3>${ph}</div>`;
 document.getElementById('ov').classList.add('op');
}
// Navigation Controls
function sw(tab,btn){
 document.querySelectorAll('.sc').forEach(s=>s.classList.remove('on'));
 document.querySelectorAll('.nb').forEach(b=>b.classList.remove('on'));
 document.getElementById('tab-'+tab).classList.add('on');
 btn.classList.add('on');
}
// Dropdown Populate
const dsel=document.getElementById('dsel');
[...new Set(D.employees.map(e=>e.dept).filter(Boolean))].sort().forEach(d=>{const o=document.createElement('option');o.value=d;o.textContent=d;dsel.appendChild(o);});
render();
// Ambient Canvas Animation
(function(){
 const c=document.getElementById('cv'),x=c.getContext('2d');
 let W,H,P=[];
 function rs(){W=c.width=innerWidth;H=c.height=innerHeight;
   P=Array.from({length:45},()=>({x:Math.random()*W,y:Math.random()*H,r:Math.random()*1.2+.4,
     vx:(Math.random()-.5)*.2,vy:(Math.random()-.5)*.2,a:Math.random()*.3+.08,
     c:['rgba(79,141,255,','rgba(124,92,255,','rgba(0,229,204,'][Math.floor(Math.random()*3)]}));}
 function dr(){x.clearRect(0,0,W,H);
   P.forEach((p,i)=>{
     x.beginPath();x.arc(p.x,p.y,p.r,0,Math.PI*2);x.fillStyle=p.c+p.a+')';x.fill();
     p.x+=p.vx;p.y+=p.vy;
     if(p.x<0||p.x>W)p.vx*=-1;if(p.y<0||p.y>H)p.vy*=-1;
     P.slice(i+1).forEach(q=>{const dx=p.x-q.x,dy=p.y-q.y,d=Math.sqrt(dx*dx+dy*dy);
       if(d<115){x.beginPath();x.moveTo(p.x,p.y);x.lineTo(q.x,q.y);
         x.strokeStyle=`rgba(79,141,255,${.05*(1-d/115)})`;x.lineWidth=.5;x.stroke();}});});
   requestAnimationFrame(dr);}
 addEventListener('resize',rs);rs();dr();
})();
</script>
</body>
</html>"""


def build_dashboard_html(data, init):
    return HTML_TEMPLATE.replace("__DATA__", json.dumps(data)).replace("JD", init, 1)
