# -*- coding: utf-8 -*-
"""Apertura con lo guardado (DATOS FALSOS, muchos). Uso:
    python3 pruebas/probar_apertura.py <carpeta con index.html> [Sol,Mica] [cant_leads] [cpu_x]
Entra una vez (queda lo guardado), vuelve a abrir con getData demorado 8 s y la CPU frenada (cpu_x, como una compu lenta)
y mide lo mismo que manda la app a USO ('abrir app (lo guardado)': performance.now() al primer render) más
las funciones que más tiempo se llevan (perfil de CDP). Todo pedido a Google se responde con datos falsos; lo demás se aborta.
"""
import sys, os, json, threading, functools, http.server, socketserver, re, time, copy, random, collections
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import datos_falsos
from datos_falsos import FakeApi

SRC = os.path.abspath(sys.argv[1]); ROLES = (sys.argv[2] if len(sys.argv) > 2 else 'Sol,Mica').split(',')
N = int(sys.argv[3]) if len(sys.argv) > 3 else 1500; CPU = float(sys.argv[4]) if len(sys.argv) > 4 else 4
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(Q, directory=SRC)); PORT = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = 'http://127.0.0.1:%d/index.html' % PORT
FUENTE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fuentes', 'archivo-latin-wdth-normal.woff2'), 'rb').read()
GOOGLE = re.compile(r'script\.google\.com|googleusercontent\.com|docs\.google\.com')

def api_grande():
    api = FakeApi(); base = api.leads; random.seed(7); extra = []
    for i in range(N):
        l = copy.deepcopy(base[i % len(base)]); l['id'] = 'X%d' % i; l['nombre'] = 'Persona %d Prueba' % i
        l['fecha'] = datos_falsos.D(random.randint(-60, 14)); l['resumen'] = ('Resumen de prueba largo. ' * random.randint(1, 20)).strip()
        extra.append(l)
    api.leads = base + extra
    return api

def medir(browser, who):
    api = api_grande(); est = {'demora': 0}
    ctx = browser.new_context(viewport={'width': 1366, 'height': 599}, locale='es-AR', timezone_id='America/Argentina/Buenos_Aires', service_workers='block')
    page = ctx.new_page(); page.clock.install(time='2026-11-05T11:20:00-03:00')
    def route(r):
        u = r.request.url
        if GOOGLE.search(u):
            try: b = json.loads(r.request.post_data or '{}')
            except Exception: b = {}
            if b.get('fn') == 'getData' and est['demora']: time.sleep(0)  # se retiene abajo
            if b.get('fn') == 'getData' and est['demora']: est.setdefault('held', []).append(r); return
            ok, data = api.handle(b.get('fn'), b.get('arg'))
            r.fulfill(status=200, content_type='application/json', body=json.dumps({'ok': True, 'data': data} if ok else {'ok': False, 'error': data}))
        elif u.startswith('http://127.0.0.1:%d/' % PORT): r.continue_()
        elif 'fonts.googleapis.com/css' in u: r.fulfill(status=200, content_type='text/css', body="@font-face{font-family:'Archivo';src:url(https://fonts.gstatic.com/a.woff2) format('woff2')}")
        elif 'fonts.gstatic.com' in u: r.fulfill(status=200, content_type='font/woff2', body=FUENTE)
        else: r.abort()
    page.route('**/*', route)
    page.goto(BASE); page.wait_for_timeout(1200)
    page.click('button[data-yo="%s"]' % who); page.wait_for_timeout(300)
    page.keyboard.type('1234'); page.wait_for_timeout(3000)
    snap = page.evaluate("() => { for (const k of Object.keys(localStorage)) if (/snap/.test(k)) return [k, localStorage[k].length]; return null; }")
    est['demora'] = 1
    cdp = ctx.new_cdp_session(page); cdp.send('Emulation.setCPUThrottlingRate', {'rate': CPU})
    cdp.send('Profiler.enable'); cdp.send('Profiler.setSamplingInterval', {'interval': 500}); cdp.send('Profiler.start')
    t0 = time.time(); page.reload(wait_until='commit')
    try: page.wait_for_function("() => /Actualizado|Mostrando lo guardado/.test(document.body.innerText)", timeout=30000, polling=50)
    except Exception: page.screenshot(path='/tmp/claude-0/-home-claude-estudio-juridico/3536371b-b611-5cf8-8f24-a4f8f1bb735c/scratchpad/apertura_%s.png' % who); print('no pintó', who, snap, page.evaluate("() => document.body.innerText.slice(0,300)"))
    pinta_ms = round((time.time() - t0) * 1000); page.wait_for_timeout(int(1500 * CPU))
    prof = cdp.send('Profiler.stop')['profile']
    # tiempo propio por función
    nodes = {n['id']: n for n in prof['nodes']}; self_t = collections.Counter()
    ts = prof['timeDeltas']; samples = prof['samples']
    for s, dt in zip(samples, ts[1:] + [0]):
        cf = nodes[s]['callFrame']; self_t['%s:%s' % (cf['functionName'] or '(anon)', cf['lineNumber'] + 1)] += dt
    top = [(k, round(v / 1000)) for k, v in self_t.most_common(15)]
    for r in est.get('held', []):
        try: r.abort()
        except Exception: pass
    ctx.close()
    return {'quien': who, 'snap': snap, 'hasta_ver_la_agenda_ms': pinta_ms, 'top_ms': top}

with sync_playwright() as pw:
    br = pw.chromium.launch()
    for w in ROLES: print(json.dumps(medir(br, w), ensure_ascii=False))
    br.close()
