# -*- coding: utf-8 -*-
"""Finanzas › Cargar gasto: repartos que cargan en otra rama (DATOS FALSOS). Uso:
    python3 pruebas/probar_reparto.py <carpeta con index.html> <carpeta de capturas> [Juan,Mica]
Uso real 26/11: a Juan el motor le rechazó un gasto ("Ese reparto también carga en ART, y no tenés acceso: lo cargan Karim o Julián").
getFin2 se responde con un formulario de gasto como el de fin2Forms_ (los mismos textos de reparto de CONFIG.FIN2 del motor) y
saveFin2 con la regla del motor (rechaza si el reparto carga en una rama que la persona no maneja completa).
Todo pedido a Google se responde con datos falsos; lo demás se aborta.
"""
import sys, os, json, threading, functools, http.server, socketserver, re
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from datos_falsos import FakeApi

SRC = os.path.abspath(sys.argv[1]); OUT = os.path.abspath(sys.argv[2]); os.makedirs(OUT, exist_ok=True)
ROLES = (sys.argv[3] if len(sys.argv) > 3 else 'Juan,Mica').split(',')
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(Q, directory=SRC)); PORT = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = 'http://127.0.0.1:%d/index.html' % PORT
FUENTE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fuentes', 'archivo-latin-wdth-normal.woff2'), 'rb').read()
GOOGLE = re.compile(r'script\.google\.com|googleusercontent\.com|docs\.google\.com')
REPARTOS = {  # copia de CONFIG.FIN2[rama].repartos del motor real (v96)
    'ART': {'solo': 'ART 100%', 'i40': 'Compartido 3 ramas 40/40/20 (intakers)', 'c33': 'Compartido 3 ramas 33/33/33 (community)', 'artlab': '50/50 con Laboral', 'arttra': '50/50 con Tránsito'},
    'TRANSITO': {'solo': 'Solo Tránsito', 'i40': 'Compartido 3 ramas 40/40/20 (intakers)', 'c33': 'Compartido 3 ramas 33/33/33 (community)', 'arttra': '50/50 con ART', 'labtra': '50/50 con Laboral'},
    'LABORAL': {'solo': 'Laboral 100%', 'i40': 'Compartido 3 ramas 40/40/20 (intakers)', 'c33': 'Compartido 3 ramas 33/33/33 (community)', 'artlab': '50/50 con ART', 'labtra': '50/50 con Tránsito'}}
SPLITS = {'solo': None, 'i40': ['ART', 'TRANSITO', 'LABORAL'], 'c33': ['ART', 'TRANSITO', 'LABORAL'], 'artlab': ['ART', 'LABORAL'], 'arttra': ['ART', 'TRANSITO'], 'labtra': ['LABORAL', 'TRANSITO']}
RES = {'errores': [], 'casos': []}

def fin2(rama):
    return {'resumen': {'cobrado': 0, 'gastado': 0}, 'cobros': [], 'gastos': [], 'forms': {'gasto': [
        {'k': 'fecha', 'label': 'Fecha', 'tipo': 'fecha', 'req': True}, {'k': 'categoria', 'label': 'Categoría', 'tipo': 'opcion', 'req': True, 'ops': ['Publicidad', 'Sueldos', 'Otros']},
        {'k': 'monto', 'label': 'Monto total pagado', 'tipo': 'monto', 'req': True},
        {'k': 'reparto', 'label': 'Reparto', 'tipo': 'opcion', 'req': True, 'ops': list(REPARTOS[rama].values())},
        {'k': 'pago', 'label': 'Pagó', 'tipo': 'opcion', 'req': True, 'quien': True, 'ops': ['Juan', 'Karim', 'Juli']}, {'k': 'detalle', 'label': 'Detalle', 'tipo': 'texto'}]}}

def caso(browser, who, vp):
    api = FakeApi(); calls = []
    full = {'Juan': ['TRANSITO'], 'Mica': ['ART', 'LABORAL'], 'Karim': ['ART', 'LABORAL', 'TRANSITO']}.get(who, [])
    ctx = browser.new_context(viewport=vp, device_scale_factor=2, is_mobile=True, has_touch=True, locale='es-AR', timezone_id='America/Argentina/Buenos_Aires', service_workers='block')
    page = ctx.new_page(); page.clock.install(time='2026-11-05T11:20:00-03:00')
    def route(r):
        u = r.request.url
        if GOOGLE.search(u):
            try: b = json.loads(r.request.post_data or '{}')
            except Exception: b = {}
            fn, arg = b.get('fn'), b.get('arg') or {}; calls.append((fn, arg))
            if fn == 'getFin2': ok, data = True, fin2(arg.get('rama'))
            elif fn == 'saveFin2':
                rama = arg.get('rama'); rep = (arg.get('datos') or arg).get('reparto') if isinstance(arg.get('datos') or arg, dict) else ''
                rk = next((k for k, v in REPARTOS.get(rama, {}).items() if v == rep), 'solo'); otras = [x for x in (SPLITS.get(rk) or []) if x != rama]
                sin = [x for x in otras if x not in full]
                ok, data = (False, 'Ese reparto también carga en ' + ' y '.join(sin) + ', y no tenés acceso: lo cargan Karim o Julián.') if sin else (True, {'ok': True})
            elif fn in ('getFin2Panel', 'fin2Calentar'): ok, data = True, {}
            else: ok, data = api.handle(fn, arg)
            r.fulfill(status=200, content_type='application/json', body=json.dumps({'ok': True, 'data': data} if ok else {'ok': False, 'error': data}))
        elif u.startswith('http://127.0.0.1:%d/' % PORT): r.continue_()
        elif 'fonts.googleapis.com/css' in u: r.fulfill(status=200, content_type='text/css', body="@font-face{font-family:'Archivo';src:url(https://fonts.gstatic.com/a.woff2) format('woff2')}")
        elif 'fonts.gstatic.com' in u: r.fulfill(status=200, content_type='font/woff2', body=FUENTE)
        else: r.abort()
    page.route('**/*', route)
    page.on('pageerror', lambda e: RES['errores'].append('%s EXCEPCION: %s' % (who, str(e)[:200])))
    page.goto(BASE); page.wait_for_timeout(1200)
    page.click('button[data-yo="%s"]' % who); page.wait_for_timeout(300); page.keyboard.type('1234'); page.wait_for_timeout(2500)
    page.click('#nav button[data-view="finanzas"]'); page.wait_for_timeout(800)
    if page.get_by_text('Finanzas protegidas').count():
        page.locator('input:visible').first.click(); page.keyboard.type('135792'); page.wait_for_timeout(300)
        if page.get_by_role('button', name='Entrar').count(): page.get_by_role('button', name='Entrar').click()
        page.wait_for_timeout(1500)
    if who == 'Karim' and page.locator('[data-f2per="semana"]').count() == 0 and page.locator('[data-f2rama]').count() == 0:
        pass
    page.wait_for_timeout(800)
    # Tránsito si la persona tiene varias ramas
    if page.locator('[data-f2rama="TRANSITO"]').count(): page.click('[data-f2rama="TRANSITO"]'); page.wait_for_timeout(800)
    try: page.click('[data-f2nuevo="gasto"]', timeout=5000)
    except Exception: page.screenshot(path=os.path.join(OUT, 'sin_gasto_%s.png' % who)); print(page.evaluate('() => document.body.innerText.slice(0,600)')); raise
    page.wait_for_timeout(700)
    pk = page.locator('#sheet [data-f2pick^="reparto|"]')
    ops = [{'txt': pk.nth(i).inner_text(), 'apagado': pk.nth(i).is_disabled()} for i in range(pk.count())]
    hint = page.locator('#sheet .hint', has_text='los cargan Karim o Julián').all_inner_texts()
    tag = '%s_%dx%d' % (who, vp['width'], vp['height'])
    page.locator('#sheet [data-f2pick^="reparto|"]').first.scroll_into_view_if_needed(); page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(OUT, 'reparto_%s.png' % tag))
    # Intentar el compartido de 3 ramas: si está apagado no se puede tocar
    c3 = page.locator('#sheet [data-f2pick="reparto|Compartido 3 ramas 40/40/20 (intakers)"]')
    try: c3.click(timeout=1500); toco = True
    except Exception: toco = False
    page.wait_for_timeout(300)
    elegido = page.locator('#sheet [data-f2pick^="reparto|"].on').all_inner_texts()
    RES['casos'].append({'quien': who, 'vp': tag, 'opciones': ops, 'aviso': hint, 'toco_compartido': toco, 'quedo_elegido': elegido,
                         'saveFin2': sum(1 for c in calls if c[0] == 'saveFin2')})
    ctx.close()

with sync_playwright() as pw:
    br = pw.chromium.launch()
    for w in ROLES:
        for vp in ({'width': 390, 'height': 844}, {'width': 360, 'height': 640}): caso(br, w, vp)
    br.close()
print(json.dumps(RES, ensure_ascii=False, indent=1))
