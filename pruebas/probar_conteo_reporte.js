// Conteo del reporte semanal (repConsultas_) con el código del motor, sobre un HISTORIAL bajado en JSON (solo lectura).
// Uso: node pruebas/probar_conteo_reporte.js <historial.json> ["Nombre:marca,..."]  — compara ../prod_nuevo.gs (antes) y prod_v76.gs (después).
function cargar(f) {
  const ctx = { console, Utilities: {}, SpreadsheetApp: {}, PropertiesService: {}, CacheService: {}, LockService: {}, Session: {}, DriveApp: {}, UrlFetchApp: {}, ScriptApp: {}, ContentService: {}, HtmlService: {}, CalendarApp: {}, MailApp: {}, Logger: { log() {} } };
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(f, 'utf8') + '\n;this.__r = { repConsultas_, repLunes_, REP_ };', ctx);
  return ctx.__r;
}
const raw = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const vals = (Array.isArray(raw) ? JSON.parse(raw[0].text) : raw).values.slice(1);
const fecha = s => { const m = String(s).trim().match(/^(\d{1,2})\/(\d{1,2})\/(\d{4}) (\d{1,2}):(\d{2}):(\d{2})/); return m ? new Date(+m[3], +m[2] - 1, +m[1], +m[4], +m[5], +m[6]) : s; };
const hv = vals.map(r => { const x = r.slice(); while (x.length < 13) x.push(''); x[0] = fecha(x[0]); return x; });
// Marca de prueba opcional: "fila:texto" para simular resultados cargados en la app
(process.argv[3] || '').split(',').filter(Boolean).forEach(s => { const [nom, txt] = s.split(':'); hv.filter(r => String(r[4]).includes(nom) && /^C$/i.test(String(r[5]).trim())).forEach(r => r[12] = txt); });
for (const [nombre, f] of [['actual', '../prod_nuevo.gs'], ['v76', 'prod_v76.gs']]) {
  const R = cargar(f), cr = R.repConsultas_(hv);
  for (const sem of ['2026-10-26', '2026-11-02']) {
    const wk = R.repLunes_(new Date(sem + 'T12:00:00')).getTime();
    const L = {};
    cr.consultas.filter(q => q.wk === wk).forEach(q => (L[q.res] = L[q.res] || []).push(cr.info[q.key].n));
    const vino = (L['VINO NO FIRMO'] || []).length + (L['VINO NO ES CASO'] || []).length;
    console.log(nombre, sem, 'firmaron', (L.FIRMO || []).length, '| vinieron y no firmaron', vino, '| no show', (L['NO SHOW'] || []).length, '| reagenda', (L.REAGENDA || []).length);
    for (const k of Object.keys(L)) console.log('   ', k + ':', L[k].sort().join(', '));
  }
}
