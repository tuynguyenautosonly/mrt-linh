// Clean-room illustration of a policy boundary, not a production authorization system.
export const SAMPLE=Object.freeze({id:'DEMO-104',vehicle:'DEMO-CAR-A',owner:'DEMO-CUSTOMER-A',observedAt:'2026-10-27T09:00:00Z',taskState:'reported_done_pending_qc',item:'Inspection of a ventilation assembly',reference:'SYNTHETIC-TASK-42'});
export function serviceContext({record,role,vehicle,customer,now}){
 if(!record||role!=='advisor')return {kind:'withheld',reason:'role'};
 if(vehicle!==record.vehicle||customer!==record.owner)return {kind:'withheld',reason:'identity'};
 const time=Date.parse(record.observedAt);
 if(!Number.isFinite(time)||!Number.isFinite(now)||now<time||now-time>600000)return {kind:'withheld',reason:'freshness'};
 if(record.taskState!=='reported_done_pending_qc')return {kind:'withheld',reason:'unmapped_state'};
 return {kind:'draft',state:'reported_done_pending_qc',reference:record.reference};
}
export const TECH_SCENARIOS=Object.freeze({sourceMissing:{vehicle:'DEMO-PLATFORM-A',question:'A vehicle will not crank after module replacement.',matchedDocument:null},newCase:{vehicle:'DEMO-PLATFORM-B',question:'Start a different vehicle case.',matchedDocument:null}});
