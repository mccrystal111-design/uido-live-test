/* UiDo round-state logic — presentation-independent field-test state.
 * Keep this module free of DOM/UI code so the skin can be replaced independently.
 */
(function(root){
'use strict';
var STORAGE_KEY='uido-field-test-round-v1';
function stamp(){return new Date().toISOString()}
function freshState(){return{schema:'uido.field-test-round.v1',round_id:'uido-'+new Date().toISOString().replace(/[:.]/g,'-'),course_id:'overstone-park',course_name:'Overstone Park Golf Club',started_at_utc:stamp(),ended_at_utc:null,current_hole:1,current_step:0,latest_gps:null,holes:{},events:[]}}
function loadState(storage){try{var s=JSON.parse(storage.getItem(STORAGE_KEY)||'null');if(s&&s.round_id&&!s.ended_at_utc)return s}catch(e){}return freshState()}
function create(options){options=options||{};var storage=options.storage||root.localStorage;var onError=options.onError||function(){};var state=loadState(storage);
function persist(){try{storage.setItem(STORAGE_KEY,JSON.stringify(state));return true}catch(e){onError(e);return false}}
function holeData(n){if(!state.holes[n])state.holes[n]={hole_number:n,shot:{},score:null,putts:null,penalties:null,events:[]};return state.holes[n]}
function replaceState(next){state=next;persist();return state}
function setCurrentHole(n){state.current_hole=n;return state}
function setCurrentStep(n){state.current_step=n;return state}
function setLatestGPS(gps){state.latest_gps=gps;return state}
function currentShotNumber(){var h=holeData(state.current_hole);return(h.shot_count||0)+1}
function addEvent(event){state.events.push(event);var h=holeData(state.current_hole);h.events.push(event.event_id);if(event.event_type==='tile_selected')h.shot[event.tile_id]=event.selected_value;return persist()}
function buildExportPayload(endedAt){state.ended_at_utc=endedAt||stamp();return{schema:'uido.field-test-round.v1',round_id:state.round_id,course_id:state.course_id,course_name:state.course_name,started_at_utc:state.started_at_utc,ended_at_utc:state.ended_at_utc,hole_count:18,completed_holes:Object.keys(state.holes).map(Number).sort(function(a,b){return a-b}),holes:state.holes,event_count:state.events.length,events:state.events}}
return{get state(){return state},persist:persist,holeData:holeData,replaceState:replaceState,setCurrentHole:setCurrentHole,setCurrentStep:setCurrentStep,setLatestGPS:setLatestGPS,currentShotNumber:currentShotNumber,addEvent:addEvent,buildExportPayload:buildExportPayload,stamp:stamp,freshState:freshState};
}
root.UiDoRoundState={create:create,storageKey:STORAGE_KEY};
})(window);
