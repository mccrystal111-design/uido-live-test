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

    // Full-screen route-relative vignette. The fade is defined by distance
    // from the route, but its outer field reaches the screen boundary so the
    // capture window never creates a second visible rectangle.
    const treatments=[
      {extraYards:4,  blurYards:9},
      {extraYards:18, blurYards:18},
      {extraYards:42, blurYards:34},
      {extraYards:70, blurYards:52}
    ];
    treatments.forEach((treatment,index)=>{
      const stroke=document.createElementNS(ns,"path");
      const filterId="agnostic45-vignette-"+index;
      const filter=document.createElementNS(ns,"filter");
      filter.setAttribute("id",filterId);
      filter.setAttribute("x","-100%"); filter.setAttribute("y","-100%");
      filter.setAttribute("width","300%"); filter.setAttribute("height","300%");
      const blur=document.createElementNS(ns,"feGaussianBlur");
      blur.setAttribute("stdDeviation",String(treatment.blurYards*0.9144*metresToViewUnits));
      filter.appendChild(blur);
      defs.appendChild(filter);

      stroke.setAttribute("d",routePath);
      stroke.setAttribute("fill","none");
      stroke.setAttribute("stroke","black");
      stroke.setAttribute("stroke-width",String((corridor+treatment.extraYards*0.9144)*2*metresToViewUnits));
      stroke.setAttribute("stroke-linecap","round");
      stroke.setAttribute("stroke-linejoin","round");
      stroke.setAttribute("filter","url(#"+filterId+")");
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