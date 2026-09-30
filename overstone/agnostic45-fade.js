(function(){
  "use strict";

  function attach(screen, routePath, metresToViewUnits, options){
    const width=options.width;
    const height=options.height;
    const corridor=options.corridorYards*0.9144;
    const fade=options.fadeYards*0.9144;

    const ns="http://www.w3.org/2000/svg";
    const svg=document.createElementNS(ns,"svg");
    svg.classList.add("fadeLayer");
    svg.setAttribute("viewBox","0 0 "+width+" "+height);
    svg.setAttribute("preserveAspectRatio","none");

    const defs=document.createElementNS(ns,"defs");
    const mask=document.createElementNS(ns,"mask");
    const id="agnostic45-fade-mask";
    mask.setAttribute("id",id);
    mask.setAttribute("maskUnits","userSpaceOnUse");
    mask.setAttribute("maskContentUnits","userSpaceOnUse");
    mask.setAttribute("x","0"); mask.setAttribute("y","0");
    mask.setAttribute("width",width); mask.setAttribute("height",height);

    const full=document.createElementNS(ns,"rect");
    full.setAttribute("width",width); full.setAttribute("height",height);
    full.setAttribute("fill","white");
    mask.appendChild(full);

    // Deterministic luminance mask: paint a series of increasingly lighter
    // route strokes. Unlike opacity/blur combinations, these literal grey
    // values directly define the amount of veil allowed through the mask.
    const treatments=[
      {extraYards:0,  grey:0},
      {extraYards:5,  grey:32},
      {extraYards:10, grey:58},
      {extraYards:18, grey:92},
      {extraYards:28, grey:125},
      {extraYards:40, grey:158},
      {extraYards:55, grey:188},
      {extraYards:75, grey:214}
    ];
    treatments.slice().reverse().forEach(treatment=>{
      const stroke=document.createElementNS(ns,"path");
      stroke.setAttribute("d",routePath);
      stroke.setAttribute("fill","none");
      stroke.setAttribute("stroke","rgb("+treatment.grey+","+treatment.grey+","+treatment.grey+")");
      stroke.setAttribute("stroke-width",String((corridor+treatment.extraYards*0.9144)*2*metresToViewUnits));
      stroke.setAttribute("stroke-linecap","round");
      stroke.setAttribute("stroke-linejoin","round");
      mask.appendChild(stroke);
    });

    defs.appendChild(mask);
    svg.appendChild(defs);

    const veil=document.createElementNS(ns,"rect");
    veil.setAttribute("width",width);
    veil.setAttribute("height",height);
    veil.setAttribute("fill","#f4f1e6");
    veil.setAttribute("fill-opacity","0.68");
    veil.setAttribute("mask","url(#"+id+")");
    svg.appendChild(veil);

    screen.appendChild(svg);
  }

  window.UiDoAgnostic45Fade={attach};
})();