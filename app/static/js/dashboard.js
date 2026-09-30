(async()=>{
 if(!requireLogin()) return;
 const welcome=document.getElementById("welcome"), history=document.getElementById("history");
 try{
  const [s,h]=await Promise.all([
   fetch("/api/session-info",{headers:authHeaders()}).then(r=>r.json()),
   fetch("/api/history",{headers:authHeaders()}).then(r=>r.json())
  ]);
  if(s.detail) throw new Error(s.detail);
  welcome.textContent=`Welcome, ${s.name}. You have ${h.length} recent recommendation(s).`;
  history.innerHTML=h.length?h.map(x=>`<div class="history-row"><b>${x.planner.toUpperCase()}</b> · ${new Date(x.created_at).toLocaleString()}<br>${x.response.summary||"Recommendation plan"}</div>`).join(""):"<p>No recommendations yet.</p>";
 }catch(e){history.innerHTML=`<p class="message">${e.message}</p>`}
 document.getElementById("logoutBtn").onclick=()=>{localStorage.removeItem("pocketsmart_token");location.href="/login";}
})();
