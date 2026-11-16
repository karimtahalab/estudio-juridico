# -*- coding: utf-8 -*-
"""Primera apertura del día (DATOS FALSOS). Uso:
    python3 pruebas/probar_snap.py <carpeta con index.html> <carpeta de capturas> [Cele,Pri]
Entra una vez (queda lo guardado en el celular), le cambia la hora a lo guardado (8 h, 40 h, 5 días) y vuelve a abrir
con getData demorado 9 s (como el motor en frío: 9-17 s en el uso real del 14 y 15/11).
Mide: cuánto tarda en verse la agenda, si aparece el aviso, si deja guardar mientras tanto, y qué pasa si getData falla.
Todo pedido a Google se responde con datos falsos; lo demás se aborta.
"""
import sys, os, json, threading, functools, http.server, socketserver, re, time
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from datos_falsos import FakeApi

SRC = os.path.abspath(sys.argv[1]); OUT = os.path.abspath(sys.argv[2]); os.makedirs(OUT, exist_ok=True)
ROLES = (sys.argv[3] if len(sys.argv) > 3 else 'Cele,Pri').split(',')
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(Q, directory=SRC)); PORT = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = 'http://127.0.0.1:%d/index.html' % PORT
FUENTE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fuentes', 'archivo-latin-wdth-normal.woff2'), 'rb').read()
GOOGLE = re.compile(r'script\.google\.com|googleusercontent\.com|docs\.google\.com')
RES = {'errores': [], 'casos': []}

def caso(browser, who, edad_h, vp, demora=9.0, falla=False, otro=False):
    api = FakeApi(); calls = []; held = []; estado = {'retener': False}
    ctx = browser.new_context(viewport=vp, device_scale_factor=1, is_mobile=True, has_touch=True, locale='es-AR',
                              timezone_id='America/Argentina/Buenos_Aires', service_workers='block')
    page = ctx.new_page(); page.clock.install(time='2026-11-05T11:20:00-03:00')
    def responder(r, fn, arg, fallar=False):
        if fallar: r.fulfill(status=200, content_type='application/json', body=json.dumps({'ok': False, 'error': 'Sin conexión con el servidor.'})); return
        try: ok, data = api.handle(fn, arg)
        except Exception as e: print('fake falló', fn, repr(e)[:200]); ok, data = False, 'fake: ' + str(e)[:80]
        r.fulfill(status=200, content_type='application/json', body=json.dumps({'ok': True, 'data': data} if ok else {'ok': False, 'error': data}))
    def route(r):
        u = r.request.url
        if GOOGLE.search(u):
            try: b = json.loads(r.request.post_data or '{}')
            except Exception: b = {}
            fn = b.get('fn'); calls.append(fn)
            if fn == 'getData' and estado.get('fallar_ya'): responder(r, fn, b.get('arg'), True); return
            if fn == 'getData' and estado['retener']: held.append((r, fn, b.get('arg'), time.time())); return
            responder(r, fn, b.get('arg'))
        elif u.startswith('http://127.0.0.1:%d/' % PORT): r.continue_()
        elif 'fonts.googleapis.com/css' in u: r.fulfill(status=200, content_type='text/css', body="@font-face{font-family:'Archivo';src:url(https://fonts.gstatic.com/a.woff2) format('woff2')}")
        elif 'fonts.gstatic.com' in u: r.fulfill(status=200, content_type='font/woff2', body=FUENTE)
        else: r.abort()
    page.route('**/*', route)
    page.on('pageerror', lambda e: RES['errores'].append('%s EXCEPCION: %s' % (who, str(e)[:200])))
    # 1) entrar normal: queda lo guardado
    page.goto(BASE); page.wait_for_timeout(1000)
    page.click('button[data-yo="%s"]' % who); page.wait_for_timeout(300)
    page.fill('#pin', '1234'); page.wait_for_timeout(700)
    if page.query_selector('#sheet.on #pin'): page.fill('#pin', '1234'); page.wait_for_timeout(700)
    for _ in range(40):
        if page.evaluate("() => !!localStorage.getItem('snap')"): break
        page.wait_for_timeout(250)
    else: print('sin snap', who, calls)
    # 2) lo guardado pasa a ser de hace edad_h horas (y, si otro, de otra persona)
    page.evaluate("""([h, otro]) => { const k='snap'; const s=JSON.parse(localStorage.getItem(k)); s.t=Date.now()-h*3600e3; if (otro) s.d.user.name='Otra Persona'; localStorage.setItem(k, JSON.stringify(s)); }""", [edad_h, otro])
    estado['retener'] = True; n0 = len(calls)
    t0 = time.time(); page.reload(); visto = None; cap_antes = None
    while time.time() - t0 < demora:
        if visto is None and page.query_selector('#main .foot'): visto = round(time.time() - t0, 1)
        page.wait_for_timeout(150)
    tag = '%s_%dh%s%s_%d' % (who, edad_h, '_falla' if falla else '', '_otro' if otro else '', vp['width'])
    page.screenshot(path=os.path.join(OUT, tag + '_a_esperando.png'))
    aviso = page.eval_on_selector('#main', 'm => { const b=m.querySelector(".snap-ban"); return b ? b.innerText.trim() : ""; }')
    # mientras espera: intentar cargar un resultado (si hay agenda)
    intento = None
    nb = page.query_selector('#nav button[data-view="agenda"]')
    if nb and nb.is_visible(): nb.click(); page.wait_for_timeout(500)
    r = page.query_selector('[data-result]')
    if r and not falla:
        n_w = calls.count('saveAction'); r.click(); page.wait_for_timeout(500)
        nf = page.query_selector('#sheet [data-res="nofirmo"]')
        if nf:
            nf.click(); page.wait_for_timeout(200); m = page.query_selector('#sheet [data-motivo]')
            if m: m.click()
            page.click('#sheet [data-save]'); page.wait_for_timeout(1200)
            intento = {'saveAction_salio': calls.count('saveAction') - n_w, 'mensaje': page.eval_on_selector('body', 'b => (document.querySelector("#toast")||{}).innerText || ""').strip()[:160]}
            page.screenshot(path=os.path.join(OUT, tag + '_b_intento.png'))
            c = page.query_selector('#sheet.on [data-close]')
            if c: c.click(); page.wait_for_timeout(300)
    # 3) llega getData
    for (rr, fn, arg, _) in held: responder(rr, fn, arg, falla)
    held.clear(); estado['retener'] = False; estado['fallar_ya'] = falla
    page.wait_for_timeout(9000 if falla else 1500)
    fin = page.eval_on_selector('#main', 'm => ({aviso: (m.querySelector(".snap-ban")||{}).innerText||"", foot: (m.querySelector(".foot")||{}).innerText||""})')
    page.screenshot(path=os.path.join(OUT, tag + '_c_llego.png'))
    despues = None
    if True:
        r = page.query_selector('[data-result]')
        if r:
            n_w = calls.count('saveAction') + calls.count('deshacerResultado'); r.click(); page.wait_for_timeout(500)
            nf = page.query_selector('#sheet [data-res="nofirmo"]')
            if nf:
                nf.click(); m = page.query_selector('#sheet [data-motivo]')
                if m: m.click()
                page.click('#sheet [data-save]'); page.wait_for_timeout(1500)
                despues = calls.count('saveAction') + calls.count('deshacerResultado') - n_w
    RES['casos'].append({'quien': who, 'edad_h': edad_h, 'ancho': vp['width'], 'falla': falla, 'otro': otro,
                         'se_ve_a_los_s': visto, 'aviso_esperando': aviso, 'intento_guardar': intento,
                         'al_llegar': {k: v.strip()[:120] for k, v in fin.items()}, 'guardar_despues': despues,
                         'getData_al_abrir': calls[n0:].count('getData')})
    ctx.close()

with sync_playwright() as pw:
    try: browser = pw.chromium.launch()
    except Exception: browser = pw.chromium.launch(channel='chrome')
    for who in ROLES:
        for vp in [{'width': 390, 'height': 844}, {'width': 360, 'height': 640}]:
            caso(browser, who, 40, vp)
        vp = {'width': 390, 'height': 844}
        caso(browser, who, 8, vp)
        caso(browser, who, 120, vp)
        caso(browser, who, 40, vp, otro=True)
        caso(browser, who, 40, vp, falla=True)
    browser.close()
srv.shutdown()
json.dump(RES, open(os.path.join(OUT, 'snap.json'), 'w'), ensure_ascii=False, indent=1)
for c in RES['casos']:
    print(json.dumps(c, ensure_ascii=False))
print('errores:', RES['errores'][:10])
