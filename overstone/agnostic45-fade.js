(function(){
  "use strict";

  function node(ns,name,attrs){
    const el=document.createElementNS(ns,name);
    Object.keys(attrs||{}).forEach(k=>el.setAttribute(k,String(attrs[k])));
    return el;
  }

  function parseRoute(routePath){
    const nums=(routePath.match(/[-+]?\\d*\\.?\\d+(?:e[-+]?\\d+)?/gi)||[]).map(Number);
    const points=[];
    for(let i=0;i+1<nums.length;i+=2) points.push([nums[i],nums[i+1]]);
    return points;
  }

  function attach(screen, routePath, metresToViewUnits, options){
    const width=options.width;
    const height=options.height;
    const corridor=options.corridorYards*0.9144*metresToViewUnits;
    const fade=options.fadeYards*0.9144*metresToViewUnits;
    const total=corridor+fade;
    const ns="http://www.w3.org/2000/svg";

    const svg=node(ns,"svg",{
      viewBox:"0 0 "+width+" "+height,
      preserveAspectRatio:"none"
    });
    svg.classList.add("fadeLayer");

    const defs=node(ns,"defs");
    const maskId="agnostic45-gradient-fade";
    const mask=node(ns,"mask",{
      id:maskId,
      maskUnits:"userSpaceOnUse",
      maskContentUnits:"userSpaceOnUse",
      x:0,y:0,width:width,height:height
    });
    mask.setAttribute("mask-type","luminance");

    // White = veil visible. The route-relative gradient strokes below
    // punch a smooth, transparent corridor through that veil.
    mask.appendChild(node(ns,"rect",{
      x:0,y:0,width:width,height:height,fill:"#ffffff"
    }));

    const points=parseRoute(routePath);
    const innerRatio=corridor/total;
    const startFade=(1-innerRatio)/2;
    const endFade=1-startFade;

    points.slice(0,-1).forEach((p,i)=>{
      const q=points[i+1];
      const dx=q[0]-p[0];
      const dy=q[1]-p[1];
      const len=Math.hypot(dx,dy);
      if(len<0.001) return;

      const nx=-dy/len;
      const ny=dx/len;
      const mx=(p[0]+q[0])/2;
      const my=(p[1]+q[1])/2;

      const gradId="agnostic45-segment-"+i;
      const grad=node(ns,"linearGradient",{
        id:gradId,
        gradientUnits:"userSpaceOnUse",
        x1:mx-nx*total,
        y1:my-ny*total,
        x2:mx+nx*total,
        y2:my+ny*total
      });

      grad.appendChild(node(ns,"stop",{offset:0,stopColor:"#ffffff"}));
      grad.appendChild(node(ns,"stop",{offset:startFade,stopColor:"#000000"}));
      grad.appendChild(node(ns,"stop",{offset:endFade,stopColor:"#000000"}));
      grad.appendChild(node(ns,"stop",{offset:1,stopColor:"#ffffff"}));
      defs.appendChild(grad);

      mask.appendChild(node(ns,"line",{
        x1:p[0],y1:p[1],x2:q[0],y2:q[1],
        stroke:"url(#"+gradId+")",
        strokeWidth:2*total,
        strokeLinecap:"round"
      }));
    });

    // Radial endpoint fades give the route corridor naturally rounded
    // transitions at the tee and green rather than a flat cap.
    if(points.length){
      [[points[0],"tee"],[points[points.length-1],"green"]].forEach(([p,label])=>{
        const gradId="agnostic45-end-"+label;
        const grad=node(ns,"radialGradient",{
          id:gradId,
          gradientUnits:"userSpaceOnUse",
          cx:p[0],cy:p[1],r:total
        });
        grad.appendChild(node(ns,"stop",{offset:0,stopColor:"#000000"}));
        grad.appendChild(node(ns,"stop",{offset:innerRatio,stopColor:"#000000"}));
        grad.appendChild(node(ns,"stop",{offset:1,stopColor:"#ffffff"}));
        defs.appendChild(grad);
        mask.appendChild(node(ns,"circle",{
          cx:p[0],cy:p[1],r:total,
          fill:"url(#"+gradId+")"
        }));
      });
    }

    defs.appendChild(mask);
    svg.appendChild(defs);

    svg.appendChild(node(ns,"rect",{
      x:0,y:0,width:width,height:height,
      fill:"#f4f1e6",
      fillOpacity:0.68,
      mask:"url(#"+maskId+")"
    }));

    screen.appendChild(svg);
  }

  window.UiDoAgnostic45Fade={attach};
})();