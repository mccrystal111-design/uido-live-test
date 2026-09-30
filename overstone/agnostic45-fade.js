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
    const id="agnostic45-clean-fade";
    mask.setAttribute("id",id);
    mask.setAttribute("maskUnits","userSpaceOnUse");
    mask.setAttribute("maskContentUnits","userSpaceOnUse");
    mask.setAttribute("x","0");
    mask.setAttribute("y","0");
    mask.setAttribute("width",width);
    mask.setAttribute("height",height);

    const full=document.createElementNS(ns,"rect");
    full.setAttribute("x","0");
    full.setAttribute("y","0");
    full.setAttribute("width",width);
    full.setAttribute("height",height);
    full.setAttribute("fill","white");
    mask.appendChild(full);

    const filter=document.createElementNS(ns,"filter");
    const filterId="agnostic45-clean-edge";
    filter.setAttribute("id",filterId);
    filter.setAttribute("x","-100%");
    filter.setAttribute("y","-100%");
    filter.setAttribute("width","300%");
    filter.setAttribute("height","300%");
    const blur=document.createElementNS(ns,"feGaussianBlur");
    blur.setAttribute("stdDeviation",String(fade*0.5*metresToViewUnits));
    blur.setAttribute("result","softCorridor");
    filter.appendChild(blur);

    // Give the feathered corridor an organic, cloud-like edge while keeping
    // the corridor itself route-relative. The noise only displaces the
    // already-blurred boundary; it does not create a second visual layer.
    const turbulence=document.createElementNS(ns,"feTurbulence");
    turbulence.setAttribute("type","fractalNoise");
    turbulence.setAttribute("baseFrequency","0.008 0.018");
    turbulence.setAttribute("numOctaves","5");
    turbulence.setAttribute("seed","15");
    turbulence.setAttribute("result","cloudNoise");
    filter.appendChild(turbulence);

    const displacement=document.createElementNS(ns,"feDisplacementMap");
    displacement.setAttribute("in","softCorridor");
    displacement.setAttribute("in2","cloudNoise");
    displacement.setAttribute(
      "scale",
      String(Math.min(40,Math.max(24,fade*0.50*metresToViewUnits)))
    );
    displacement.setAttribute("xChannelSelector","R");
    displacement.setAttribute("yChannelSelector","G");
    displacement.setAttribute("result","cloudEdge");
    filter.appendChild(displacement);

    const finalBlur=document.createElementNS(ns,"feGaussianBlur");
    finalBlur.setAttribute("in","cloudEdge");
    finalBlur.setAttribute("stdDeviation","0.8");
    filter.appendChild(finalBlur);

    defs.appendChild(filter);

    const clear=document.createElementNS(ns,"path");
    clear.setAttribute("d",routePath);
    clear.setAttribute("fill","none");
    clear.setAttribute("stroke","black");
    clear.setAttribute("stroke-width",String(corridor*2*metresToViewUnits));
    clear.setAttribute("stroke-linecap","round");
    clear.setAttribute("stroke-linejoin","round");
    clear.setAttribute("filter","url(#"+filterId+")");
    mask.appendChild(clear);

    defs.appendChild(mask);
    svg.appendChild(defs);

    const veil=document.createElementNS(ns,"rect");
    veil.setAttribute("x","0");
    veil.setAttribute("y","0");
    veil.setAttribute("width",width);
    veil.setAttribute("height",height);
    veil.setAttribute("fill","#f4f1e6");
    veil.setAttribute("fill-opacity","0.72");
    veil.setAttribute("mask","url(#"+id+")");
    svg.appendChild(veil);

    screen.appendChild(svg);
  }

  window.UiDoAgnostic45Fade={attach};
})();