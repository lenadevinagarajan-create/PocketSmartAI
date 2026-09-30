(async()=>{
 if(!requireLogin()) return;
 const form=document.getElementById("jewelryForm"), msg=document.getElementById("message"), result=document.getElementById("result");
 form.addEventListener("submit",async e=>{
  e.preventDefault();msg.textContent="Generating your plan...";
  try{
   const fd=new FormData(form);fd.set("budget",String(Number(fd.get("budget"))));
   const r=await fetch("/api/generate-jewelry",{method:"POST",headers:authHeaders(),body:fd});
   const body=await r.json();if(!r.ok)throw new Error(body.detail||"Request failed");renderResult(result,body);msg.textContent="";
  }catch(e){msg.textContent=e.message}
 });
})();
