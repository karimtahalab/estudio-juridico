# -*- coding: utf-8 -*-
"""Banco (DATOS FALSOS): la pantalla nueva llega a una app que queda abierta (service worker), 24/11.
Sirve una COPIA de la carpeta con index.html y sw.js, con API_URL cambiado a un /api local que responde datos falsos
(además se aborta todo lo externo). Service worker PERMITIDO (en correr.py está bloqueado).
  a) ventana abierta todo el tiempo (compu): pasan 31 min sin esconderse y se publica otra versión
  b) vuelve a la app (visibilitychange) con nada a medio hacer
  c) vuelve a la app con una hoja abierta (la ficha de una consulta)
  d) recarga forzada (sin service worker al abrir) y después sale otra versión
Uso: python3 pruebas/probar_actualizacion.py <carpeta con index.html y sw.js> <carpeta de capturas>"""
import sys, os, json, re, shutil, tempfile, threading, functools, http.server, socketserver
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from datos_falsos import FakeApi

SRC = os.path.abspath(sys.argv[1]); OUT = os.path.abspath(sys.argv[2]); os.makedirs(OUT, exist_ok=True)
TMP = tempfile.mkdtemp()
for f in os.listdir(SRC):
    if os.path.isfile(os.path.join(SRC, f)) and not f.startswith('.'): shutil.copy(os.path.join(SRC, f), TMP)
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(Q, directory=TMP)); PORT = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
ORIG = 'http://127.0.0.1:%d' % PORT
idx = open(os.path.join(TMP, 'index.html'), encoding='utf-8').read()
idx = re.sub(r'window\.API_URL="[^"]*"', 'window.API_URL="%s/api"' % ORIG, idx)
open(os.path.join(TMP, 'index.html'), 'w', encoding='utf-8').write(idx)
FUENTE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fuentes', 'archivo-latin-wdth-normal.woff2'), 'rb').read()
nver = [0]
def publicar():  # otra versión de sw.js (cambia el nombre del cache, como cada publicación)
    nver[0] += 1; p = os.path.join(TMP, 'sw.js'); s = open(p, encoding='utf-8').read()
    s = re.sub(r"const V = '[^']*';", "const V = 'consultas-prueba%d';" % nver[0], s); open(p, 'w', encoding='utf-8').write(s)
    return 'prueba%d' % nver[0]
R = {}; ERR = []
def ctx_nuevo(b):
    api = FakeApi()
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, is_mobile=True, has_touch=True, locale='es-AR', timezone_id='America/Argentina/Buenos_Aires', service_workers='allow')
    def route(r):
        u = r.request.url
        if u.startswith(ORIG + '/api'):
            try: body = json.loads(r.request.post_data or '{}')
            except Exception: body = {}
            ok, data = api.handle(body.get('fn'), body.get('arg'))
            r.fulfill(status=200, content_type='application/json', headers={'Access-Control-Allow-Origin': '*'}, body=json.dumps({'ok': True, 'data': data} if ok else {'ok': False, 'error': data}))
        elif u.startswith(ORIG): r.continue_()
        elif 'fonts.googleapis.com/css' in u: r.fulfill(status=200, content_type='text/css', body="@font-face{font-family:'Archivo';src:url(https://fonts.gstatic.com/a.woff2) format('woff2')}")
        elif 'fonts.gstatic.com' in u: r.fulfill(status=200, content_type='font/woff2', body=FUENTE)
        else: r.abort()
    ctx.route('**/*', route)
    pg = ctx.new_page()
    pg.on('pageerror', lambda e: ERR.append('EXC: ' + str(e)[:200]))
    return ctx, pg
def entrar(pg):
    pg.goto(ORIG + '/index.html'); pg.wait_for_timeout(1200)
    if pg.query_selector('button[data-yo="Mica"]'):
        pg.click('button[data-yo="Mica"]'); pg.wait_for_timeout(300); pg.fill('#pin', '1234'); pg.wait_for_timeout(1500)
    pg.wait_for_function('navigator.serviceWorker.controller !== null', timeout=15000)
def ev(pg, js):
    for _ in range(6):
        try: return pg.evaluate(js)
        except Exception as e:
            if 'destroyed' not in str(e) and 'navigat' not in str(e): raise
            pg.wait_for_timeout(800)
            try: pg.wait_for_load_state('load')
            except Exception: pass
    return pg.evaluate(js)
def version(pg): return ev(pg, "caches.keys().then(k => k.filter(x => /^consultas-/.test(x)).join(','))")
def marcar(pg): ev(pg, 'window.__marca = 1')
def recargo(pg): return ev(pg, 'typeof window.__marca') == 'undefined'
def banner(pg): return bool(ev(pg, "!!document.querySelector('#sw-nueva')"))
def volver(pg): ev(pg, "document.dispatchEvent(new Event('visibilitychange'))")
def esperar(pg, ms=6000):
    for _ in range(ms // 500):
        pg.wait_for_timeout(500)
        try:
            if recargo(pg) or banner(pg): break
        except Exception: pass
    pg.wait_for_timeout(1500)
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx, pg = ctx_nuevo(b)
    pg.clock.install(time='2026-11-05T11:20:00-03:00')
    entrar(pg); pg.reload(); pg.wait_for_timeout(2500)  # segunda apertura: ya con service worker (como el equipo)
    R['inicio_version'] = version(pg)
    # a) ventana abierta, 31 min sin esconderse
    marcar(pg); v = publicar(); pg.clock.run_for(31 * 60 * 1000); esperar(pg, 8000)
    R['a_recargo'] = recargo(pg); R['a_aviso'] = banner(pg); R['a_version'] = version(pg)
    pg.screenshot(path=os.path.join(OUT, 'a_ventana_abierta_31min.png'))
    if banner(pg):
        pg.click('#sw-nueva button'); pg.wait_for_timeout(2500); R['a_tras_actualizar_recargo'] = recargo(pg)
    # b) vuelve a la app con nada a medio hacer
    pg.reload(); pg.wait_for_timeout(2000); marcar(pg); v = publicar(); volver(pg); esperar(pg)
    R['b_recargo'] = recargo(pg); R['b_aviso'] = banner(pg)
    # c) vuelve a la app con la ficha de una consulta abierta
    pg.reload(); pg.wait_for_timeout(2500)
    pg.click('#nav button[data-view="agenda"]'); pg.wait_for_timeout(800)
    card = pg.query_selector('[data-open]')
    if card: card.click(); pg.wait_for_timeout(800)
    R['c_hoja_abierta'] = bool(ev(pg, "!!document.querySelector('#sheet.on')"))
    marcar(pg); v = publicar(); volver(pg); esperar(pg)
    R['c_recargo'] = recargo(pg); R['c_aviso'] = banner(pg); R['c_hoja_sigue'] = bool(ev(pg, "!!document.querySelector('#sheet.on')"))
    pg.screenshot(path=os.path.join(OUT, 'c_hoja_abierta_version_nueva.png'))
    if not recargo(pg):
        pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
        x = pg.query_selector('#sheet.on [data-close], #sheet.on .x, #sheet.on button[aria-label="Cerrar"]')
        if x: x.click(); pg.wait_for_timeout(600)
        R['c_hoja_cerrada'] = not pg.query_selector('#sheet.on')
        volver(pg); esperar(pg); R['c_recargo_al_volver_sin_hoja'] = recargo(pg)
    ctx.close()
    # d) recarga forzada: abre sin service worker aunque ya hay uno instalado
    ctx, pg = ctx_nuevo(b)
    entrar(pg); pg.reload(); pg.wait_for_timeout(2000)
    cdp = ctx.new_cdp_session(pg); cdp.send('Network.enable'); cdp.send('Network.setBypassServiceWorker', {'bypass': True})
    pg.reload(); pg.wait_for_timeout(2500); cdp.send('Network.setBypassServiceWorker', {'bypass': False})
    R['d_sin_controlador_al_abrir'] = ev(pg, 'navigator.serviceWorker.controller === null')
    marcar(pg); v = publicar(); volver(pg); esperar(pg, 8000)
    R['d_recargo'] = recargo(pg); R['d_aviso'] = banner(pg)
    ctx.close(); b.close()
R['errores'] = ERR
print(json.dumps(R, ensure_ascii=False, indent=1))
