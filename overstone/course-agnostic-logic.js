/* UiDo course-agnostic logic: derive bunker sides from the hole's line of play.
 * Coordinate contracts: line_of_play points are [longitude, latitude];
 * bunker front_gps/back_gps points are [latitude, longitude].
 * This is geometry-relative, never dependent on the player's current GPS/heading.
 */
(function(root){
  'use strict';
  function xy(lat,lon,lat0){
    const rad=Math.PI/180;
    return {x:lon*111320*Math.cos(lat0*rad),y:lat*111320};
  }
  function getBunkerSide(hole,bunker){
    if(!hole||!Array.isArray(hole.line_of_play)||hole.line_of_play.length<2||
       !bunker||!Array.isArray(bunker.front_gps)||!Array.isArray(bunker.back_gps)){
      return bunker&&bunker.side==='left'?'left':'right';
    }
    const lat0=(bunker.front_gps[0]+bunker.back_gps[0])/2;
    const lon0=(bunker.front_gps[1]+bunker.back_gps[1])/2;
    const point=xy(lat0,lon0,lat0);
    const line=hole.line_of_play.map(p=>xy(p[1],p[0],lat0));
    let best=null;
    for(let i=0;i<line.length-1;i++){
      const a=line[i],b=line[i+1],dx=b.x-a.x,dy=b.y-a.y;
      const length2=dx*dx+dy*dy;
      if(!length2) continue;
      const t=Math.max(0,Math.min(1,((point.x-a.x)*dx+(point.y-a.y)*dy)/length2));
      const px=a.x+t*dx,py=a.y+t*dy;
      const ex=point.x-px,ey=point.y-py;
      const d2=ex*ex+ey*ey;
      if(!best||d2<best.d2) best={d2,cross:dx*(point.y-a.y)-dy*(point.x-a.x)};
    }
    if(!best||Math.abs(best.cross)<0.01) return bunker.side==='left'?'left':'right';
    // Looking along the tee-to-green line: positive cross product is left.
    return best.cross>0?'left':'right';
  }
  root.UIDO_COURSE_LOGIC=root.UIDO_COURSE_LOGIC||{};
  root.UIDO_COURSE_LOGIC.getBunkerSide=getBunkerSide;
})(window);
