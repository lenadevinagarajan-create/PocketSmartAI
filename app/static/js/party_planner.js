(async()=>{
 if(!requireLogin()) return;
 const form=document.getElementById("partyForm"), msg=document.getElementById("message"), result=document.getElementById("result");
 form.addEventListener("submit",async e=>{
  e.preventDefault();msg.textContent="Generating your plan...";
  try{
   const data=Object.fromEntries(new FormData(form).entries());data.budget=Number(data.budget);data.guests=Number(data.guests);
   const r=await fetch("/api/generate-party",{method:"POST",headers:authHeaders({"Content-Type":"application/json"}),body:JSON.stringify(data)});
   const body=await r.json();if(!r.ok)throw new Error(body.detail||"Request failed");renderResult(result,body);msg.textContent="";
  }catch(e){msg.textContent=e.message}
 });
})();
