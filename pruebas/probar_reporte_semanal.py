# -*- coding: utf-8 -*-
"""Banco (DATOS FALSOS): Sol confirma clientes seguidos en "Cargar reporte semanal" (publicado el 27/11, d797eee).
Uso real 27/11: Sol hizo 15 saveFin2 (6-10 s) y 18 getFin2 lentos (12-15 s) en Finanzas.
Simula esos tiempos: saveFin2 tarda SAVE_MS y getFin2 tarda GET_MS (con lo que había en la planilla AL EMPEZAR a leer).
  Sol confirma a Ana; apenas vuelve el guardado (empieza la lectura) confirma a Beto; después a Caro.
Mira: si cada confirmado se ve como confirmado al instante, si al final queda alguno "para confirmar" que ya se guardó,
cuántos saveFin2 y getFin2 salen. Uso: python3 pruebas/probar_reporte_semanal.py <carpeta con index.html> <carpeta de capturas> [rapido]"""
import sys, os, json, threading, time, copy, re, shutil, tempfile
RAPIDO = len(sys.argv) > 3 and sys.argv[3] == 'rapido'
sys.argv = sys.argv[:3] + ['Sol']
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import explora_base as B
from playwright.sync_api import sync_playwright

FALLA = int(os.environ.get('FALLA') or 0)  # fila cuyo guardado falla (para ver que vuelve a 'para confirmar')
SAVE_MS, GET_MS = (1500, 2500) if RAPIDO else (6000, 9000)
ATIENDE = ['Mica', 'Cele', 'Sol']
def form_cliente():
    return [{'k': 'fecha', 'label': 'Fecha de firma', 'tipo': 'fecha', 'req': True}, {'k': 'nombre', 'label': 'Nombre', 'tipo': 'texto', 'req': True},
            {'k': 'tipo', 'label': 'Tipo', 'tipo': 'opcion', 'ops': ['Accidente de trabajo', 'In itinere', 'Enfermedad profesional']},
            {'k': 'lesion', 'label': 'Lesión / diagnóstico', 'tipo': 'texto'}, {'k': 'atiende', 'label': 'Atiende', 'tipo': 'opcion', 'quien': True, 'ops': ATIENDE},
            {'k': 'notas', 'label': 'Notas', 'tipo': 'texto'}]

class Planilla:
    def __init__(self):
        self.lock = threading.Lock()
        self.clientes = [
            {'fila': 11, 'fecha': '2026-11-03', 'nombre': 'Ana Prueba Gómez', 'tipo': 'In itinere', 'lesion': 'Fractura de muñeca (prueba)', 'atiende': 'Mica', 'app': True},
            {'fila': 12, 'fecha': '2026-11-03', 'nombre': 'Beto Prueba Díaz', 'tipo': 'Accidente de trabajo', 'lesion': 'Lumbalgia (prueba)', 'atiende': 'Cele', 'app': True},
            {'fila': 13, 'fecha': '2026-11-04', 'nombre': 'Caro Prueba Ruiz', 'tipo': 'Accidente de trabajo', 'lesion': 'Hombro (prueba)', 'atiende': 'Mica', 'app': True}]
    def foto(self, arg):
        with self.lock:
            return {'rama': 'ART', 'ramas': ['ART', 'LABORAL'], 'modo': 'carga', 'alias': {}, 'periodo': {'tipo': 'semana', 'desde': '2026-11-02', 'hasta': '2026-11-08'},
                    'tieneClientes': True, 'tieneAcuerdos': False, 'tieneFacturas': False, 'acuerdoNombre': '', 'cobros': [], 'facturas': [], 'acuerdos': [], 'casos': [],
                    'clientes': copy.deepcopy(self.clientes), 'posiblesRep': [], 'firmados': [], 'resumen': {'cobrado': 0, 'facturado': 0},
                    'gastos': [], 'porCobrar': [], 'retiros': [], 'tieneRetiros': False, 'forms': {'cliente': form_cliente()}}
    def guardar(self, arg):
        with self.lock:
            c = next((x for x in self.clientes if x['fila'] == arg.get('fila')), None)
            if c:
                for k, v in (arg.get('datos') or {}).items():
                    if k in ('fecha', 'nombre', 'tipo', 'lesion', 'atiende', 'notas'): c[k] = v
                if arg.get('confirmar'): c['app'] = False
        return {'ok': True}

def correr(br, vp):
    api = B.FakeApi(); pl = Planilla(); ped = []; errs = []
    ctx = br.new_context(viewport={'width': vp[0], 'height': vp[1]}, device_scale_factor=2, is_mobile=True, has_touch=True, locale='es-AR', timezone_id='America/Argentina/Buenos_Aires', service_workers='block')
    pg = ctx.new_page(); pg.clock.install(time='2026-11-05T11:20:00-03:00')
    pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    pg.on('console', lambda m: m.type == 'error' and 'ERR_FAILED' not in m.text and errs.append('console: ' + m.text[:200]))
    import http.server, socketserver
    COPIA = tempfile.mkdtemp()
    for f in os.listdir(B.SRC):
        if os.path.isfile(os.path.join(B.SRC, f)): shutil.copy(os.path.join(B.SRC, f), COPIA)
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k): super().__init__(*a, directory=COPIA, **k)
        def log_message(self, *a): pass
        def do_POST(self):
            b = json.loads(self.rfile.read(int(self.headers.get('Content-Length') or 0)) or b'{}'); fn, arg = b.get('fn'), b.get('arg') or {}
            t0 = time.time(); ped.append([fn, {k: arg.get(k) for k in ('fila', 'confirmar', 'fresco', 'semana')}, round(t0, 2)])
            if fn == 'getFin2':
                d = pl.foto(arg); time.sleep(GET_MS / 1000.0); ok = True
            elif fn == 'saveFin2':
                time.sleep(SAVE_MS / 1000.0)
                if FALLA and arg.get('fila') == FALLA: ok, d = False, 'La planilla está ocupada, probá de nuevo en unos segundos.'
                else: d = pl.guardar(arg); ok = True
            elif fn in ('getFin2Panel', 'fin2Calentar'): ok, d = True, {}
            else:
                with pl.lock: ok, d = api.handle(fn, arg)
            body = json.dumps({'ok': ok, 'data': d} if ok else {'ok': False, 'error': d}).encode()
            self.send_response(200); self.send_header('Content-Type', 'application/json'); self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Length', str(len(body))); self.end_headers(); self.wfile.write(body)
    class TS(socketserver.ThreadingMixIn, http.server.HTTPServer): daemon_threads = True
    api_srv = TS(('127.0.0.1', 0), H); threading.Thread(target=api_srv.serve_forever, daemon=True).start()
    ORIG = 'http://127.0.0.1:%d' % api_srv.server_address[1]
    idx = open(os.path.join(COPIA, 'index.html'), encoding='utf-8').read()
    open(os.path.join(COPIA, 'index.html'), 'w', encoding='utf-8').write(re.sub(r'window\.API_URL="[^"]*"', 'window.API_URL="%s/api"' % ORIG, idx))
    def route(r):
        u = r.request.url
        if u.startswith(ORIG + '/'): r.continue_()
        else: r.abort()
    pg.route('**/*', route)
    tag = '%d' % vp[0]
    def shot(n): pg.screenshot(path=os.path.join(B.OUT, 'semanal_%s_%s.png' % (tag, n)))
    def estado():
        return pg.evaluate("""() => ({para: [...document.querySelectorAll('.rs-cli .rs-cli-tx b')].map(e=>e.textContent),
            conf: [...document.querySelectorAll('#main .todo li')].map(e=>e.innerText.split('\\n')[0]).filter(Boolean),
            guardando: !!document.querySelector('.f2-pend'), actualizando: document.body.innerText.includes('Actualizando…')})""")
    pg.goto(ORIG + '/index.html'); pg.wait_for_timeout(1000); pg.click('button[data-yo="Sol"]'); pg.wait_for_timeout(300)
    pg.fill('#pin', '1234'); pg.wait_for_timeout(2200)
    pg.click('#nav button[data-view="finanzas"]'); pg.wait_for_timeout(800)
    if pg.get_by_text('Finanzas protegidas').count():
        pg.locator('input:visible').first.click(); pg.keyboard.type('135792'); pg.wait_for_timeout(300)
        if pg.get_by_role('button', name='Entrar').count(): pg.get_by_role('button', name='Entrar').click()
    pg.wait_for_selector('[data-rsabrir]', timeout=40000); pg.click('[data-rsabrir]')
    pg.wait_for_selector('.rs-cli [data-rsconf]', timeout=40000); pg.wait_for_timeout(300)
    res = {'inicio': estado(), 'linea': []}
    shot('1_para_confirmar')
    def confirmar(fila):
        pg.click('.rs-cli [data-rsconf="%d"]' % fila); pg.wait_for_timeout(400)
        pg.click('#sheet.on [data-f2save]'); pg.wait_for_timeout(300)
        res['linea'].append(['confirmó fila %d' % fila, estado()])
    confirmar(11)
    # espera a que vuelva el guardado y arranque la lectura
    pg.wait_for_timeout(SAVE_MS + 600); res['linea'].append(['volvió el guardado de Ana', estado()])
    shot('2_leyendo')
    ok_b = pg.query_selector('.rs-cli [data-rsconf="12"]')
    if ok_b: confirmar(12)
    else: res['linea'].append(['Beto ya no estaba para confirmar', estado()])
    shot('3_beto')
    pg.wait_for_timeout(1500)
    ok_c = pg.query_selector('.rs-cli [data-rsconf="13"]')
    if ok_c: confirmar(13)
    shot('4_caro')
    # cada medio segundo: ¿vuelve a aparecer "para confirmar" alguien ya confirmado?
    vuelve = set()
    for s in range(1, 2 * (2 * SAVE_MS + 2 * GET_MS) // 1000):
        pg.wait_for_timeout(500); e = estado(); vuelve.update(e['para'])
        if s % 6 == 0: res['linea'].append(['+%.1f s' % (s / 2.0), e])
    res['reaparecen_para_confirmar'] = sorted(vuelve)
    shot('5_final')
    res['final'] = estado(); res['hoja_abierta'] = bool(pg.query_selector('#sheet.on')); res['toast'] = (pg.text_content('#toast') or '')[:90]
    res['planilla_app'] = [c['nombre'] for c in pl.clientes if c['app']]
    res['saveFin2'] = sum(1 for p in ped if p[0] == 'saveFin2'); res['getFin2'] = sum(1 for p in ped if p[0] == 'getFin2')
    res['pedidos'] = [p[:2] for p in ped if p[0] in ('saveFin2', 'getFin2')]
    res['errores'] = errs
    ctx.close(); api_srv.shutdown(); return res

out = {}
with sync_playwright() as pw:
    br = pw.chromium.launch()
    for vp in [(390, 844)]:
        out['%d' % vp[0]] = correr(br, vp)
    br.close()
B.srv.shutdown()
print(json.dumps(out, ensure_ascii=False, indent=1))
