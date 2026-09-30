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

    const soft=document.createElementNS(ns,"path");
    soft.setAttribute("d",routePath);
    soft.setAttribute("fill","none");
    soft.setAttribute("stroke","black");
    soft.setAttribute("stroke-width",String((corridor+fade)*2*metresToViewUnits));
    soft.setAttribute("stroke-linecap","round");
    soft.setAttribute("stroke-linejoin","round");

    const filter=document.createElementNS(ns,"filter");
    filter.setAttribute("id","agnostic45-fade-blur");
    filter.setAttribute("x","-50%"); filter.setAttribute("y","-50%");
    filter.setAttribute("width","200%"); filter.setAttribute("height","200%");
    const blur=document.createElementNS(ns,"feGaussianBlur");
    blur.setAttribute("stdDeviation",String(fade*1.0*metresToViewUnits));
    filter.appendChild(blur);
    defs.appendChild(filter);
    soft.setAttribute("filter","url(#agnostic45-fade-blur)");
    mask.appendChild(soft);

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