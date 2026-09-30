async function submitAuth(formId, url){
  const form=document.getElementById(formId), msg=document.getElementById("message");
  form.addEventListener("submit", async e=>{
    e.preventDefault(); msg.textContent="Working...";
    const data=Object.fromEntries(new FormData(form).entries());
    try{
      const r=await fetch(url,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)});
      const body=await r.json();
      if(!r.ok) throw new Error(body.detail||"Request failed");
      localStorage.setItem("pocketsmart_token",body.access_token);
      location.href="/dashboard";
    }catch(err){msg.textContent=err.message}
  });
}
if(document.getElementById("loginForm")) submitAuth("loginForm","/api/login");
if(document.getElementById("registerForm")) submitAuth("registerForm","/api/register");
