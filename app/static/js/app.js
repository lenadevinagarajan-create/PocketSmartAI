const TOKEN_KEY = "pocketsmart_token";
function getToken(){ return localStorage.getItem(TOKEN_KEY); }
function authHeaders(extra={}){ return {...extra, ...(getToken()?{"Authorization":"Bearer "+getToken()}: {})}; }
function requireLogin(){ if(!getToken()){ window.location.href="/login"; return false; } return true; }
function money(v){ return new Intl.NumberFormat("en-IN",{style:"currency",currency:"INR",maximumFractionDigits:0}).format(v); }
function renderResult(el, data){
  el.classList.remove("hidden");
  el.innerHTML = `<h2>${data.summary}</h2>
    <p><b>Budget:</b> ${money(data.budget)} · <b>Estimated used:</b> ${money(data.budget_used)}</p>
    ${data.warning?`<p class="message">${data.warning}</p>`:""}
    <div>${(data.recommendations||[]).map(x=>`<article class="rec">
      <div class="rec-head"><strong>${escapeHtml(x.name)}</strong><span class="price">${money(x.estimated_price)}</span></div>
      <p><span class="pill">${escapeHtml(x.category)}</span> <span class="pill">${escapeHtml(x.platform)}</span></p>
      <p>${escapeHtml(x.reason)}</p><a href="${x.url}" target="_blank" rel="noopener">View search results →</a>
    </article>`).join("")}</div>`;
}
function escapeHtml(s){return String(s??"").replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[m]));}
