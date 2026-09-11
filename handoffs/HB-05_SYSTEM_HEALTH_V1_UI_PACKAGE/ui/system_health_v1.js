export const HB04_SCHEMA = 'TANGRA_SYSTEM_HEALTH_V1';
export const CANONICAL_CONCEPTS = [
  'RUNTIME_HEALTH','SYSTEM_CPU','SYSTEM_RAM','CPU_TEMPERATURE',
  'RUNTIME_PERFORMANCE','HQ_CAMERA_HEALTH','WIDE_PIPELINE_HEALTH','HAILO_HEALTH',
  'CA_AUTHORITY_STATE','METRIC_HEALTH','HOROS_HEALTH','TELEMETRY_EDGE_HEALTH'
];
export const STATES = ['NOMINAL','DEGRADED','FAULT','STALE','UNAVAILABLE','NOT_VERIFIED'];

const LABELS = {
  RUNTIME_HEALTH:'Runtime', SYSTEM_CPU:'System CPU', SYSTEM_RAM:'System RAM',
  CPU_TEMPERATURE:'CPU Temperature', RUNTIME_PERFORMANCE:'Runtime Performance',
  HQ_CAMERA_HEALTH:'HQ Camera', WIDE_PIPELINE_HEALTH:'WIDE Pipeline', HAILO_HEALTH:'Hailo',
  CA_AUTHORITY_STATE:'CA Authority', METRIC_HEALTH:'Metric', HOROS_HEALTH:'HOROS',
  TELEMETRY_EDGE_HEALTH:'Telemetry / EDGE'
};

const VALUE_KEYS = {
  RUNTIME_HEALTH:['runtime_state','controller_state','uptime_s','ai_status'],
  SYSTEM_CPU:['usage','unit'], SYSTEM_RAM:['usage','unit'], CPU_TEMPERATURE:['temperature','unit'],
  RUNTIME_PERFORMANCE:['fps','fps_unit','stage_ms'],
  HQ_CAMERA_HEALTH:['camera_state','controller_camera_state'],
  WIDE_PIPELINE_HEALTH:['running','last_age_s','last_fresh','max_age_s','failures','last_error'],
  HAILO_HEALTH:['backend','hailo_state','controller_hailo_available','inference_ms','observation_age_s'],
  CA_AUTHORITY_STATE:['kalman_algorithm','tracking_authority','authority_match'],
  METRIC_HEALTH:['metric_usable','physical_metric_state','validity','horos_authoritative','geometry_status'],
  HOROS_HEALTH:['mode','runtime_role','authoritative','age_s','errors','degraded_reasons'],
  TELEMETRY_EDGE_HEALTH:['source','pi_http_status','pi_http_age_s','pc_cache_status','remote_ingest_status']
};

function esc(value) {
  return String(value).replace(/[&<>'"]/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[ch]));
}
function printable(value) {
  if (value === null) return 'null';
  if (typeof value === 'object') return JSON.stringify(value);
  return String(value);
}

export function validateHealthContract(payload) {
  const errors = [];
  if (!payload || typeof payload !== 'object') return {ok:false, errors:['PAYLOAD_MISSING']};
  if (payload.schema !== HB04_SCHEMA) errors.push('SCHEMA_MISMATCH');
  const concepts = payload.concepts;
  if (!concepts || typeof concepts !== 'object') return {ok:false, errors:[...errors,'CONCEPTS_MISSING']};
  const keys = Object.keys(concepts);
  if (keys.length !== CANONICAL_CONCEPTS.length || CANONICAL_CONCEPTS.some((c,i)=>keys[i]!==c)) errors.push('CANONICAL_CONCEPT_SET_MISMATCH');
  for (const concept of CANONICAL_CONCEPTS) {
    const item = concepts[concept];
    if (!item || typeof item !== 'object') { errors.push(`${concept}:MISSING`); continue; }
    if (item.concept !== concept) errors.push(`${concept}:IDENTITY_MISMATCH`);
    if (!STATES.includes(item.state)) errors.push(`${concept}:STATE_INVALID`);
    if (!Array.isArray(item.reason_codes)) errors.push(`${concept}:REASON_CODES_INVALID`);
    if (!item.values || typeof item.values !== 'object' || Array.isArray(item.values)) errors.push(`${concept}:VALUES_INVALID`);
    if (!item.freshness || typeof item.freshness !== 'object') errors.push(`${concept}:FRESHNESS_INVALID`);
    if (!Array.isArray(item.provenance)) errors.push(`${concept}:PROVENANCE_INVALID`);
    if (!Array.isArray(item.not_verified)) errors.push(`${concept}:NOT_VERIFIED_INVALID`);
  }
  return {ok:errors.length===0, errors};
}

export function buildViewModel(payload) {
  const validation = validateHealthContract(payload);
  if (!validation.ok) return {ok:false, errors:validation.errors, cards:[]};
  const cards = CANONICAL_CONCEPTS.map(concept => {
    const src = payload.concepts[concept];
    const diagnostics = [];
    for (const key of VALUE_KEYS[concept] || []) {
      if (Object.prototype.hasOwnProperty.call(src.values,key)) diagnostics.push({key, value:src.values[key]});
    }
    return {
      concept,
      label: LABELS[concept],
      state: src.state,
      reasons:[...src.reason_codes],
      diagnostics,
      freshness:{...src.freshness},
      notVerified:[...src.not_verified]
    };
  });
  return {ok:true, errors:[], cards};
}

export function renderSystemHealth(container, payload) {
  if (!container) throw new Error('SYSTEM_HEALTH_CONTAINER_REQUIRED');
  const vm = buildViewModel(payload);
  container.classList.add('system-health-v1');
  if (!vm.ok) {
    container.innerHTML = `<div class="sh-contract-error" role="status"><strong>System Health unavailable</strong><span>${esc(vm.errors.join(' · '))}</span></div>`;
    return vm;
  }
  container.innerHTML = `<div class="sh-grid">${vm.cards.map(card => {
    const reasons = card.reasons.length ? card.reasons.map(r=>`<span class="sh-reason">${esc(r)}</span>`).join('') : '<span class="sh-reason sh-muted">NO_REASON_CODE</span>';
    const diagnostics = card.diagnostics.length ? card.diagnostics.map(d=>`<div class="sh-value"><span>${esc(d.key)}</span><strong>${esc(printable(d.value))}</strong></div>`).join('') : '<div class="sh-value sh-muted">No diagnostic values</div>';
    const nv = card.notVerified.length ? `<div class="sh-not-verified">Not verified: ${card.notVerified.map(esc).join(', ')}</div>` : '';
    return `<section class="sh-card state-${esc(card.state)}" data-concept="${esc(card.concept)}" data-state="${esc(card.state)}">
      <header><span class="sh-title">${esc(card.label)}</span><span class="sh-state">${esc(card.state)}</span></header>
      <div class="sh-reasons">${reasons}</div>
      <div class="sh-values">${diagnostics}</div>${nv}
    </section>`;
  }).join('')}</div>`;
  return vm;
}

export function attachSystemHealthView({root, getHealthSnapshot}) {
  if (!root || typeof getHealthSnapshot !== 'function') throw new Error('SYSTEM_HEALTH_ADAPTER_INVALID');
  return {
    refresh() { return renderSystemHealth(root, getHealthSnapshot()); }
  };
}
