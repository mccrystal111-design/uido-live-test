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

    // Three nested black strokes create the mask graduation. Each is
    // blurred by a different amount; because they are opaque mask paint,
    // the blur produces real luminance values rather than relying on
    // stroke opacity, which is unreliable inside an SVG luminance mask.
    const treatments=[
      {extraYards:7,  blurYards:4},
      {extraYards:22, blurYards:11},
      {extraYards:45, blurYards:24}
    ];
    treatments.forEach((treatment,index)=>{
      const stroke=document.createElementNS(ns,"path");
      const filterId="agnostic45-fade-treatment-"+index;
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

    // The centre remains genuinely clear, independent of the soft treatments.
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