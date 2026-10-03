/* UiDo core round state. No renderer, DOM, course name, or course geometry dependencies. */
(function(root){
'use strict';
var STORAGE_KEY='uido-round-state-v1';
function stamp(){return new Date().toISOString()}
function freshState(options){options=options||{};var now=stamp();return{schema:'uido.round.v1',round_id:'uido-'+now.replace(/[:.]/g,'-'),course_id:options.courseId||'unselected-course',course_name:options.courseName||'Course',started_at_utc:now,ended_at_utc:null,current_hole:1,current_step:0,latest_gps:null,holes:{},events:[]}}
function readState(storage){try{var s=JSON.parse(storage.getItem(STORAGE_KEY)||'null');if(s&&s.round_id&&!s.ended_at_utc)return s}catch(e){}return null}
function create(options){options=options||{};var storage=options.storage||root.localStorage;var onError=options.onError||function(){};var state=readState(storage)||freshState(options);
function persist(){try{storage.setItem(STORAGE_KEY,JSON.stringify(state));return true}catch(e){onError(e);return false}}
function holeData(n){n=Number(n);if(!state.holes[n])state.holes[n]={hole_number:n,shot:{},score:null,putts:null,penalties:null,shot_count:0,events:[]};return state.holes[n]}
function replaceState(next){state=next;persist();return state}
function setCurrentHole(n){state.current_hole=Number(n);return persist()}
function setCurrentStep(n){state.current_step=Number(n);return persist()}
function setLatestGPS(gps){state.latest_gps=gps?Object.assign({},gps):null;return persist()}
function currentShotNumber(){return(Number(holeData(state.current_hole).shot_count)||0)+1}
function recordEvent(event){if(!event||!event.event_type)throw new Error('event_type is required');var e=Object.assign({schema:'uido.event.v1',event_id:'event-'+Date.now()+'-'+Math.random().toString(16).slice(2),round_id:state.round_id,hole_number:state.current_hole,shot_number:currentShotNumber(),timestamp_utc:stamp()},event);state.events.push(e);var h=holeData(e.hole_number);h.events.push(e.event_id);if(e.event_type==='tile_selected'&&e.tile_id)h.shot[e.tile_id]=e.selected_value;if(e.event_type==='shot_captured'){h.shot_count=(Number(h.shot_count)||0)+1;h.shot.started_at_utc=e.timestamp_utc;h.shot.gps_at_hit=e.position||state.latest_gps||null;h.shot.pre_shot_snapshot=Object.assign({},h.shot)}persist();return e}
function buildExportPayload(endedAt){return{schema:'uido.round.v1',round_id:state.round_id,course_id:state.course_id,course_name:state.course_name,started_at_utc:state.started_at_utc,ended_at_utc:endedAt||stamp(),hole_count:18,completed_holes:Object.keys(state.holes).map(Number).sort(function(a,b){return a-b}),holes:state.holes,event_count:state.events.length,events:state.events}}
return{get state(){return state},persist:persist,holeData:holeData,replaceState:replaceState,setCurrentHole:setCurrentHole,setCurrentStep:setCurrentStep,setLatestGPS:setLatestGPS,currentShotNumber:currentShotNumber,recordEvent:recordEvent,buildExportPayload:buildExportPayload,stamp:stamp,freshState:freshState};
}
root.UiDoRoundState={create:create,storageKey:STORAGE_KEY};
})(window);
