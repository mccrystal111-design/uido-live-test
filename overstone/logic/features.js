/* Optional feature registry. UI/settings may disable a feature without removing its implementation. */
(function(root){
'use strict';
var KEY='uido-feature-settings-v1';
var defaults={gps:true,wind:true,lie:true,club:true,shotCapture:true,strike:true,trajectory:true,scoring:true,scorecard:true,export:true};
function read(){try{var saved=JSON.parse(root.localStorage.getItem(KEY)||'{}');return Object.assign({},defaults,saved)}catch(e){return Object.assign({},defaults)}}
var flags=read();
function enabled(name){return Object.prototype.hasOwnProperty.call(flags,name)?!!flags[name]:false}
function setEnabled(name,value){if(!Object.prototype.hasOwnProperty.call(defaults,name))throw new Error('Unknown UiDo feature: '+name);flags[name]=!!value;try{root.localStorage.setItem(KEY,JSON.stringify(flags))}catch(e){}return flags[name]}
function all(){return Object.assign({},flags)}
root.UiDoFeatures={defaults:Object.assign({},defaults),enabled:enabled,setEnabled:setEnabled,all:all,reset:function(){flags=Object.assign({},defaults);try{root.localStorage.setItem(KEY,JSON.stringify(flags))}catch(e){}return all()}};
})(window);
