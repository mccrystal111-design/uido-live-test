/**
 * UiDo Hole View Builder
 *
 * Canonical course geometry is physical and course-scoped.
 * A hole contributes only its route/direction. The builder resolves which
 * physical course features are available inside the requested viewing window.
 *
 * No feature type is special-cased for ownership. A bunker, water feature,
 * tee, fairway, path, woodland, etc. is treated identically by the spatial
 * query.
 */
(function(root){
  "use strict";

  const EARTH_RADIUS_M = 6371000;

  function toLocal(point, origin){
    const lat0 = origin[1] * Math.PI / 180;
    return [
      (point[0] - origin[0]) * Math.cos(lat0) * Math.PI / 180 * EARTH_RADIUS_M,
      (point[1] - origin[1]) * Math.PI / 180 * EARTH_RADIUS_M
    ];
  }

  function fromLocal(point, origin){
    const lat0 = origin[1] * Math.PI / 180;
    return [
      origin[0] + point[0] / (Math.cos(lat0) * EARTH_RADIUS_M) * 180 / Math.PI,
      origin[1] + point[1] / EARTH_RADIUS_M * 180 / Math.PI
    ];
  }

  function geometryPoints(geometry){
    if(!geometry) return [];
    if(geometry.type === "Point") return [geometry.coordinates];
    if(geometry.type === "LineString") return geometry.coordinates;
    if(geometry.type === "Polygon") return geometry.coordinates.flat();
    if(geometry.type === "MultiLineString") return geometry.coordinates.flat();
    if(geometry.type === "MultiPolygon") return geometry.coordinates.flat(2);
    if(geometry.type === "GeometryCollection"){
      return geometry.geometries.flatMap(geometryPoints);
    }
    return [];
  }

  function bbox(points){
    if(!points.length) return null;
    let minX=Infinity,minY=Infinity,maxX=-Infinity,maxY=-Infinity;
    points.forEach(p=>{
      minX=Math.min(minX,p[0]); maxX=Math.max(maxX,p[0]);
      minY=Math.min(minY,p[1]); maxY=Math.max(maxY,p[1]);
    });
    return {minX,minY,maxX,maxY};
  }

  function bboxIntersects(a,b){
    return a && b &&
      a.minX <= b.maxX && a.maxX >= b.minX &&
      a.minY <= b.maxY && a.maxY >= b.minY;
  }

  function routeCoordinates(routing){
    const g = routing && routing.geometry;
    if(!g) return [];
    if(g.type === "LineString") return g.coordinates;
    if(g.type === "MultiLineString") return g.coordinates.flat();
    return [];
  }

  function directionFromRoute(coords){
    if(coords.length < 2) throw new Error("Hole route requires at least two coordinates");
    const start = coords[0];
    const end = coords[coords.length-1];
    const origin = start;
    const a = toLocal(start, origin);
    const b = toLocal(end, origin);
    const dx=b[0]-a[0], dy=b[1]-a[1];
    const length=Math.hypot(dx,dy);
    if(!length) throw new Error("Hole route has zero travel length");
    return {
      origin,
      vector:[dx/length,dy/length],
      length_m:length,
      start,
      end
    };
  }

  function projectToHoleSpace(point, origin, direction){
    const p=toLocal(point,origin);
    const forward=direction;
    const right=[forward[1],-forward[0]];
    return {
      forward:p[0]*forward[0]+p[1]*forward[1],
      lateral:p[0]*right[0]+p[1]*right[1]
    };
  }

  function buildWindowPolygon(origin,direction,options){
    const back=options.back_m;
    const forward=options.forward_m;
    const halfWidth=options.width_m/2;
    const f=direction.vector;
    const r=[f[1],-f[0]];
    const corners=[
      [-back,-halfWidth],
      [forward,-halfWidth],
      [forward,halfWidth],
      [-back,halfWidth],
      [-back,-halfWidth]
    ];
    return corners.map(([along,lateral])=>{
      const local=[
        f[0]*along+r[0]*lateral,
        f[1]*along+r[1]*lateral
      ];
      return fromLocal(local,origin);
    });
  }

  function windowBoundsInHoleSpace(features,origin,direction){
    const points=[];
    features.forEach(feature=>{
      geometryPoints(feature.geometry).forEach(point=>{
        points.push(projectToHoleSpace(point,origin,direction));
      });
    });
    if(!points.length) return null;
    return {
      minForward:Math.min(...points.map(p=>p.forward)),
      maxForward:Math.max(...points.map(p=>p.forward)),
      minLateral:Math.min(...points.map(p=>p.lateral)),
      maxLateral:Math.max(...points.map(p=>p.lateral))
    };
  }

  function buildHoleView(course,holeNumber,options){
    options=Object.assign({
      back_m:0,
      forward_m:450,
      width_m:180
    },options||{});

    if(!course || !course.geometry || !Array.isArray(course.geometry.features)){
      throw new Error("Canonical course geometry.features is required");
    }

    const hole=(course.holes||[]).find(h=>Number(h.hole_number)===Number(holeNumber));
    if(!hole) throw new Error("Hole "+holeNumber+" not found");

    const coords=routeCoordinates(hole.routing);
    const direction=directionFromRoute(coords);
    const polygon=buildWindowPolygon(direction.origin,direction,options);

    const windowPoints=polygon.map(p=>toLocal(p,direction.origin));
    const windowBBox=bbox(windowPoints);

    const features=course.geometry.features.filter(feature=>{
      const points=geometryPoints(feature.geometry).map(p=>toLocal(p,direction.origin));
      return bboxIntersects(bbox(points),windowBBox);
    });

    return {
      schema:"uido.hole-view.v2",
      course_id:course.course && course.course.id,
      hole_number:Number(hole.hole_number),
      direction_of_travel:{
        origin:direction.start,
        destination:direction.end,
        unit_vector:direction.vector,
        route_length_m:direction.length_m
      },
      viewing_window:{
        back_m:options.back_m,
        forward_m:options.forward_m,
        width_m:options.width_m,
        polygon
      },
      features,
      feature_ids:features.map(f=>String(f.id)),
      bounds:windowBoundsInHoleSpace(features,direction.origin,direction)
    };
  }

  root.UiDoHoleViewBuilder={buildHoleView,geometryPoints};
})(typeof window !== "undefined" ? window : globalThis);
