(function(){
  const options=[...document.querySelectorAll('.option')];
  const confirm=document.getElementById('confirm');
  const status=document.getElementById('selectionStatus');
  let selected=null;
  options.forEach(button=>button.addEventListener('click',()=>{
    selected=button.dataset.value;
    options.forEach(item=>item.setAttribute('aria-pressed',String(item===button)));
    confirm.disabled=false;
    status.textContent=selected+' selected';
  }));
  confirm.addEventListener('click',()=>{
    if(!selected)return;
    document.documentElement.dataset.confirmed='true';
    status.textContent='Strike confirmed: '+selected;
    window.dispatchEvent(new CustomEvent('uido:strike-confirmed',{detail:{value:selected}}));
    if(window.parent!==window){
      window.parent.postMessage({type:'uido:strike-confirmed',value:selected},window.location.origin);
    }
  });
})();