(function(){
  "use strict";

  /*
   * UiDo generic hole-view builder.
   *
   * Course geometry is physical and hole-agnostic. A hole contributes only its
   * route: start/tee, direction of travel and destination. The resolver then
   * asks which physical features intersect that route's viewing window.
   *
   * This adapter currently accepts the existing Overstone source packet while
   * the generated canonical-course.v2 JSON becomes the runtime course-loader
   * contract. It deliberately deduplicates by physical feature id.
   */
  function keyForFeature(f){
    return String(f && (f.id || f["@id"] || ""));
  }

  function allPhysicalFeatures(courseHoles){
    const byId = new Map();
    Object.keys(courseHoles || {}).forEach(holeNo=>{
      const hole = courseHoles[holeNo] || {};
      (hole.features || []).forEach(feature=>{
        const id = keyForFeature(feature);
        if(!id) return;
        if(!byId.has(id)) byId.set(id, feature);
      });
    });
    return Array.from(byId.values());
  }

  function pointSet(geometry){
    if(!geometry) return [];
    const t=geometry.type, c=geometry.coordinates;
    if(t==="Point") return [c];
    if(t==="LineString") return c || [];
    if(t==="Polygon") return (c && c[0]) || [];
    if(t==="MultiLineString") return (c||[]).flat();
    if(t==="MultiPolygon") return (c||[]).flatMap(poly=>(poly&&poly[0])||[]);
    return [];
  }

  function metresPerDegree(latitude){
    const r=Math.PI/180;
    return {
      x:111320*Math.cos(latitude*r),
      y:111320
    };
  }

  function local(point, origin, scale){
    return [
      (point[0]-origin[0])*scale.x,
      (point[1]-origin[1])*scale.y
    ];
  }

  function routeFor(hole){
    const line=hole.line_of_play || [];
    if(line.length<2) throw new Error("Hole route requires at least two line-of-play points");
    const start=line[0];
    const end=line[line.length-1];
    const greenMiddle=hole.green_fmb && hole.green_fmb.middle
      ? [hole.green_fmb.middle[1], hole.green_fmb.middle[0]]
      : end;
    const dx=end[0]-start[0], dy=end[1]-start[1];
    const length=Math.hypot(dx,dy);
    if(!length) throw new Error("Hole route has zero travel direction");
    return {
      hole_number:hole.hole,
      par:hole.par,
      line_of_play:line,
      start,
      destination:greenMiddle,
      direction:[dx/length,dy/length],
      length_degrees:length,
      green_fmb:hole.green_fmb || null
    };
  }

  function build(courseHoles, holeNumber, options){
    const hole=courseHoles && courseHoles[String(holeNumber)];
    if(!hole) throw new Error("Hole "+holeNumber+" not found in course source");
    const route=routeFor(hole);
    const features=allPhysicalFeatures(courseHoles);
    const origin=route.start;
    const scale=metresPerDegree(origin[1]);

    /*
     * The viewing window is an oriented corridor along direction of travel.
     * Defaults are intentionally generous: the renderer remains responsible
     * for the final camera fit and clipping. This layer decides relevance,
     * not presentation.
     */
    const opts=Object.assign({
      lateralMarginM:80,
      startMarginM:20,
      endMarginM:40
    },options||{});

    const dirM=[
      route.direction[0]*scale.x,
      route.direction[1]*scale.y
    ];
    const dirLen=Math.hypot(dirM[0],dirM[1]);
    const ux=dirM[0]/dirLen, uy=dirM[1]/dirLen;
    const px=-uy, py=ux;

    const greenLocal=local(route.destination,origin,scale);
    const routeLengthM=Math.max(
      dirLen,
      Math.hypot(greenLocal[0],greenLocal[1])
    );
    const minAlong=-opts.startMarginM;
    const maxAlong=routeLengthM+opts.endMarginM;
    const halfWidth=opts.lateralMarginM;

    function intersects(feature){
      const points=pointSet(feature.geometry);
      if(!points.length) return false;
      let minAlongF=Infinity,maxAlongF=-Infinity,minCross=Infinity,maxCross=-Infinity;
      points.forEach(p=>{
        const q=local(p,origin,scale);
        const along=q[0]*ux+q[1]*uy;
        const cross=q[0]*px+q[1]*py;
        minAlongF=Math.min(minAlongF,along);
        maxAlongF=Math.max(maxAlongF,along);
        minCross=Math.min(minCross,cross);
        maxCross=Math.max(maxCross,cross);
      });
      return maxAlongF>=minAlong &&
             minAlongF<=maxAlong &&
             maxCross>=-halfWidth &&
             minCross<=halfWidth;
    }

    const selected=features.filter(intersects);
    return {
      schema:"uido.hole-view.v1",
      hole_number:route.hole_number,
      route,
      viewing_window:{
        coordinate_system:"course-local-metres",
        orientation:"hole.direction_of_travel",
        lateral_margin_m:opts.lateralMarginM,
        start_margin_m:opts.startMarginM,
        end_margin_m:opts.endMarginM,
        route_length_m:routeLengthM
      },
      features:selected,
      physical_feature_count:selected.length,
      feature_ids:selected.map(keyForFeature)
    };
  }

  window.UIDO_HOLE_VIEW_BUILDER={build};
})();
