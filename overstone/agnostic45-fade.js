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

    // Build a long-tailed graduation. The visible fade should not have a
    // detectable outer edge, so the transition continues well beyond the
    // main 40–60 yd presentation zone.
    const steps=32;
    const fadeTailYards=40;
    const fadeTail=fadeTailYards*0.9144;
    for(let i=0;i<steps;i++){
      const t=i/(steps-1);
      const widthMetres=corridor + fadeTail*(1-t);
      const stroke=document.createElementNS(ns,"path");
      stroke.setAttribute("d",routePath);
      stroke.setAttribute("fill","none");
      stroke.setAttribute("stroke","black");
      stroke.setAttribute("stroke-width",String(widthMetres*2*metresToViewUnits));
      stroke.setAttribute("stroke-linecap","round");
      stroke.setAttribute("stroke-linejoin","round");
      // Very light at the outer edge, progressively stronger toward 40 yd.
      const opacity=0.018 + 0.032*t;
      stroke.setAttribute("stroke-opacity",String(opacity));
      mask.appendChild(stroke);
    }

    const clear=document.createElementNS(ns,"path");
    clear.setAttribute("d",routePath);
    clear.setAttribute("fill","none");
    clear.setAttribute("stroke","black");
    clear.setAttribute("stroke-width",String(corridor*2*metresToViewUnits));
    clear.setAttribute("stroke-linecap","round");
    clear.setAttribute("stroke-linejoin","round");
    mask.appendChild(clear);

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