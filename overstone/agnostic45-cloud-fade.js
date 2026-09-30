(function(){
  "use strict";

  function attach(screen, routePath, metresToViewUnits, options){
    const width=options.width;
    const height=options.height;
    const contentWidth=options.contentWidth||width;
    const corridorYards=options.corridorYards;
    const cloudStartGapYards=options.cloudStartGapYards;
    const cloudFadeYards=options.cloudFadeYards;
    const ns="http://www.w3.org/2000/svg";

    const corridor=corridorYards*0.9144;
    const outerHalf=(corridorYards+cloudStartGapYards+cloudFadeYards)*0.9144;

    const svg=document.createElementNS(ns,"svg");
    svg.classList.add("fadeLayer");
    svg.setAttribute("viewBox","0 0 "+width+" "+height);
    svg.setAttribute("preserveAspectRatio","none");

    const defs=document.createElementNS(ns,"defs");

    const mask=document.createElementNS(ns,"mask");
    const maskId="agnostic45-cloud-mask";
    mask.setAttribute("id",maskId);
    mask.setAttribute("maskUnits","userSpaceOnUse");
    mask.setAttribute("maskContentUnits","userSpaceOnUse");
    mask.setAttribute("x","0");
    mask.setAttribute("y","0");
    mask.setAttribute("width",contentWidth);
    mask.setAttribute("height",height);

    const full=document.createElementNS(ns,"rect");
    full.setAttribute("x","0");
    full.setAttribute("y","0");
    full.setAttribute("width",contentWidth);
    full.setAttribute("height",height);
    full.setAttribute("fill","white");
    mask.appendChild(full);

    // The cloud boundary is a broad route-relative field. It starts well
    // outside the 40-yard clear corridor and follows every bend in the route.
    const cloudFilter=document.createElementNS(ns,"filter");
    const cloudFilterId="agnostic45-cloud-edge";
    cloudFilter.setAttribute("id",cloudFilterId);
    cloudFilter.setAttribute("x","-50%");
    cloudFilter.setAttribute("y","-50%");
    cloudFilter.setAttribute("width","200%");
    cloudFilter.setAttribute("height","200%");

    const turbulence=document.createElementNS(ns,"feTurbulence");
    turbulence.setAttribute("type","fractalNoise");
    turbulence.setAttribute("baseFrequency","0.004 0.011");
    turbulence.setAttribute("numOctaves","5");
    turbulence.setAttribute("seed","27");
    turbulence.setAttribute("result","cloudNoise");
    cloudFilter.appendChild(turbulence);

    const displacement=document.createElementNS(ns,"feDisplacementMap");
    displacement.setAttribute("in","SourceGraphic");
    displacement.setAttribute("in2","cloudNoise");
    displacement.setAttribute(
      "scale",
      String(Math.max(55,Math.min(105,cloudFadeYards*0.9*metresToViewUnits)))
    );
    displacement.setAttribute("xChannelSelector","R");
    displacement.setAttribute("yChannelSelector","G");
    displacement.setAttribute("result","organicEdge");
    cloudFilter.appendChild(displacement);

    const blur=document.createElementNS(ns,"feGaussianBlur");
    blur.setAttribute("in","organicEdge");
    blur.setAttribute("stdDeviation",String(Math.max(1.2,cloudFadeYards*0.12*metresToViewUnits)));
    cloudFilter.appendChild(blur);

    defs.appendChild(cloudFilter);

    const outer=document.createElementNS(ns,"path");
    outer.setAttribute("d",routePath);
    outer.setAttribute("fill","none");
    outer.setAttribute("stroke","black");
    outer.setAttribute("stroke-width",String(outerHalf*2*metresToViewUnits));
    outer.setAttribute("stroke-linecap","round");
    outer.setAttribute("stroke-linejoin","round");
    outer.setAttribute("filter","url(#"+cloudFilterId+")");
    mask.appendChild(outer);

    // Keep the 40-yard route corridor fully clear and stable.
    const inner=document.createElementNS(ns,"path");
    inner.setAttribute("d",routePath);
    inner.setAttribute("fill","none");
    inner.setAttribute("stroke","black");
    inner.setAttribute("stroke-width",String(corridor*2*metresToViewUnits));
    inner.setAttribute("stroke-linecap","round");
    inner.setAttribute("stroke-linejoin","round");
    mask.appendChild(inner);

    defs.appendChild(mask);
    svg.appendChild(defs);

    const veil=document.createElementNS(ns,"rect");
    veil.setAttribute("x","0");
    veil.setAttribute("y","0");
    veil.setAttribute("width",contentWidth);
    veil.setAttribute("height",height);
    veil.setAttribute("fill","#f4f1e6");
    veil.setAttribute("fill-opacity","0.84");
    veil.setAttribute("mask","url(#"+maskId+")");
    svg.appendChild(veil);

    screen.appendChild(svg);
  }

  window.UiDoAgnostic45Cloud={attach};
})();