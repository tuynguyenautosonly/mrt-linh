// New, dependency-free implementation. Rows are claims, not authenticated evidence.
export const HEADERS=['id','site','work','status','updated_at','due_at','evidence_ref'];
export const STATUSES=['received','doing','waiting_parts','reported_done','accepted'];
export function parseCSV(text){
 if(typeof text!=='string'||new TextEncoder().encode(text).length>1024*1024)throw Error('CSV must be at most 1 MB.');
 text=text.replace(/^\uFEFF/,'');const rows=[];let row=[],cell='',quoted=false,closed=false;
 for(let i=0;i<text.length;i++){
  const c=text[i];
  if(quoted){if(c==='"'){if(text[i+1]==='"'){cell+='"';i++;}else{quoted=false;closed=true;}}else cell+=c;continue;}
  if(closed&&!['\r','\n',','].includes(c))throw Error('Unexpected character after closing quote.');
  if(c==='"'){if(cell||closed)throw Error('Quote must start a field.');quoted=true;}
  else if(c===','){row.push(cell);cell='';closed=false;}
  else if(c==='\n'||c==='\r'){if(c==='\r'&&text[i+1]==='\n')i++;row.push(cell);if(row.some(v=>v!==''))rows.push(row);row=[];cell='';closed=false;}
  else cell+=c;
 }
 if(quoted)throw Error('Unclosed quoted field.');
 row.push(cell);if(row.some(v=>v!==''))rows.push(row);
 if(!rows.length||rows[0].join(',')!==HEADERS.join(','))throw Error('Use the seven exact template columns, in order.');
 if(rows.length>1001)throw Error('At most 1,000 work items per import.');
 return rows.slice(1).map((r,i)=>{if(r.length!==HEADERS.length)throw Error(`Row ${i+2}: expected seven columns.`);return Object.fromEntries(HEADERS.map((k,j)=>[k,r[j].trim()]));});
}
function timestamp(s){
 if(!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,3})?(?:Z|[+-]\d{2}:\d{2})$/.test(s))return null;
 const t=Date.parse(s);if(!Number.isFinite(t))return null;
 const date=s.slice(0,10),d=new Date(date+'T00:00:00Z');
 if(d.toISOString().slice(0,10)!==date)return null;
 const hour=Number(s.slice(11,13)),min=Number(s.slice(14,16)),sec=Number(s.slice(17,19));
 return hour<24&&min<60&&sec<60?t:null;
}
export function audit(rows,{now=Date.now(),staleHours=48}={}){
 if(!Array.isArray(rows)||rows.length>1000||!Number.isFinite(now)||!Number.isFinite(staleHours)||staleHours<=0)throw Error('Invalid audit options.');
 const ids=new Map();for(const r of rows)if(r&&typeof r.id==='string')ids.set(r.id,(ids.get(r.id)||0)+1);
 const items=rows.map((raw,index)=>{
  const valid=raw&&typeof raw==='object'&&HEADERS.every(k=>typeof raw[k]==='string'&&raw[k].length<=300)&&Object.keys(raw).every(k=>HEADERS.includes(k));
  const r=valid?{...raw}:{id:`row-${index+2}`,site:'',work:'',status:'',updated_at:'',due_at:'',evidence_ref:''};const flags=[];
  if(!valid||!r.id||!r.site||!r.work)flags.push('INVALID_ROW');
  if(ids.get(r.id)>1)flags.push('DUPLICATE_ID');
  if(!STATUSES.includes(r.status))flags.push('UNKNOWN_STATUS');
  const updated=timestamp(r.updated_at),due=timestamp(r.due_at);
  if(updated===null||due===null)flags.push('INVALID_TIME');
  if(updated!==null&&updated>now+300000)flags.push('FUTURE_UPDATE');
  if(updated!==null&&now-updated>staleHours*3600000)flags.push('STALE');
  const blocked=flags.length>0;
  let bucket='review';
  if(!blocked){
   if(r.status==='accepted'&&!r.evidence_ref)flags.push('MISSING_REFERENCE');
   else if(r.status==='accepted')bucket='accepted';
   else if(r.status==='reported_done')bucket='awaiting_review';
   else bucket='open';
   if(bucket!=='accepted'&&due<now)flags.push('OVERDUE');
  }
  return {...r,index:index+2,flags,bucket};
 });
 const count=b=>items.filter(r=>r.bucket===b).length;
 return {asOf:new Date(now).toISOString(),staleHours,items,total:items.length,open:count('open'),awaiting:count('awaiting_review'),accepted:count('accepted'),review:count('review'),overdue:items.filter(r=>r.flags.includes('OVERDUE')).length};
}
export function report(result){return [
 'PROOFBOARD — SOURCE-BASED WORK REPORT',`As of: ${result.asOf}`,`Freshness threshold: ${result.staleHours} hours`,
 `Rows: ${result.total} | Open: ${result.open} | Reported done, awaiting review: ${result.awaiting} | Source says accepted: ${result.accepted} | Data review: ${result.review}`,
 'Accepted means the imported row declares acceptance and supplies a reference. Proofboard does not authenticate it.',
 'Stale, invalid, future-dated and duplicate rows are withheld from current-work counts. No cash or revenue is inferred.','',
 ...result.items.map(r=>`${r.id} | ${r.site} | ${r.work} | ${r.bucket} | ${r.flags.join(', ')||'no rule flags'} | source row ${r.index} | ref: ${r.evidence_ref||'not supplied'}`)
].join('\n');}
