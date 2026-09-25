/* ICONS-095: one drawn line-icon family for primary navigation plus the brand emblem.
 * Presentation only: no state, no wallet, no simulation reads. 24px grid, 1.8 stroke,
 * round joins; shapes marked .fill get a soft tint on the active tab (see css/10-polish95). */
(function(root){'use strict';
 const P={
  hq:'<path d="M3 20.5h18"/><path class="fill" d="M5 20.5V15a7 7 0 0 1 14 0v5.5z"/><path d="M10 20.5v-3a2 2 0 0 1 4 0v3"/><path d="M12 8V3"/><path d="M12 3h4.2l-1.2 1.5 1.2 1.5H12"/>',
  cards:'<path d="M9 3.2h9.3a1.5 1.5 0 0 1 1.5 1.5v11.6"/><rect class="fill" x="4.2" y="6.2" width="11.8" height="14.6" rx="1.6"/><path d="m10.1 10.6 2.2 2.3-2.2 2.3-2.2-2.3z"/>',
  gift:'<path class="fill" d="M4.6 10.6h14.8v8.9a1 1 0 0 1-1 1H5.6a1 1 0 0 1-1-1z"/><rect x="3.2" y="7.4" width="17.6" height="3.2" rx=".8"/><path d="M12 7.4v13.1"/><path d="M12 7.4C10.6 4.6 7.4 4.2 7.4 6s3 1.4 4.6 1.4c1.6 0 4.6.4 4.6-1.4S13.4 4.6 12 7.4z"/>',
  map:'<path class="fill" d="m3.2 6.4 5.6-2 6.4 2 5.6-2v13.2l-5.6 2-6.4-2-5.6 2z"/><path d="M8.8 4.4v13.2"/><path d="M15.2 6.4v13.2"/><path d="M11.1 14.2V9.1l2.6 1.2-2.6 1.3"/>',
  more:'<rect class="fill" x="4" y="4" width="6.6" height="6.6" rx="1.6"/><rect x="13.4" y="4" width="6.6" height="6.6" rx="1.6"/><rect x="4" y="13.4" width="6.6" height="6.6" rx="1.6"/><path d="M16.7 14v5.4M14 16.7h5.4"/>'
 };
 function svg(id,cls=''){const body=P[id];if(!body)return '';
  return `<svg class="ui-icon ti95 ${cls}" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${body}</svg>`;}
 /* Brand emblem: gold T-pylon over the horizon line, cyan core. Used by favicon and boot screen. */
 const EMBLEM='<svg class="emblem95" viewBox="0 0 64 64" aria-hidden="true"><rect x="2" y="2" width="60" height="60" rx="14" fill="#0a2932" stroke="#63cedb" stroke-opacity=".45" stroke-width="2"/><path d="M14 20h36" stroke="#f4cc79" stroke-width="6" stroke-linecap="round"/><path d="M32 20v28" stroke="#f4cc79" stroke-width="6" stroke-linecap="round"/><path d="M10 46.5h44" stroke="#84dfdc" stroke-opacity=".55" stroke-width="2" stroke-linecap="round"/><path d="m32 26 5 5-5 5-5-5z" fill="#84dfdc" stroke="#0a2932" stroke-width="1.6"/></svg>';
 root.TerraIcons95=Object.freeze({version:'ICONS-095',svg,has:id=>Object.hasOwn(P,id),emblem:()=>EMBLEM});
})(globalThis);

