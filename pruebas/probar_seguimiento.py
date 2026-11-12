# -*- coding: utf-8 -*-
"""Seguimiento entre intakers de punta a punta (DATOS FALSOS, nada sale del navegador).
    python3 pruebas/probar_seguimiento.py [carpeta_con_index.html] [carpeta_salida]
"""
import sys, os, json, threading, functools, http.server, socketserver, re
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from datos_falsos import FakeApi

SRC = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
OUT = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else 'pruebas/capturas_seg')
os.makedirs(OUT, exist_ok=True)
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(Q, directory=SRC)); PORT = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = 'http://127.0.0.1:%d/index.html' % PORT
FUENTE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fuentes', 'archivo-latin-wdth-normal.woff2'), 'rb').read()
GOOGLE = re.compile(r'script\.google\.com|googleusercontent\.com|docs\.google\.com')
RES, ERR = [], []
def ok(nombre, cond, extra=''):
    RES.append(('OK ' if cond else 'MAL') + ' ' + nombre + (' · ' + str(extra) if extra != '' else ''))

def abrir(browser, who, vp=(390, 844)):
    api = FakeApi()
    ctx = browser.new_context(viewport={'width': vp[0], 'height': vp[1]}, device_scale_factor=2, is_mobile=True, has_touch=True,
                              locale='es-AR', timezone_id='America/Argentina/Buenos_Aires', service_workers='block')
    page = ctx.new_page(); page.clock.install(time='2026-11-05T11:20:00-03:00')
    def route(r):
        u = r.request.url
        if GOOGLE.search(u):
            try: body = json.loads(r.request.post_data or '{}')
            except Exception: body = {}
            k, data = api.handle(body.get('fn'), body.get('arg'))
            r.fulfill(status=200, content_type='application/json', body=json.dumps({'ok': True, 'data': data} if k else {'ok': False, 'error': data}))
        elif u.startswith('http://127.0.0.1:%d/' % PORT): r.continue_()
        elif 'fonts.googleapis.com/css' in u: r.fulfill(status=200, content_type='text/css', body="@font-face{font-family:'Archivo';src:url(https://fonts.gstatic.com/a.woff2) format('woff2')}")
        elif 'fonts.gstatic.com' in u: r.fulfill(status=200, content_type='font/woff2', body=FUENTE)
        else: r.abort()
    page.route('**/*', route)
    page.on('pageerror', lambda e: ERR.append('%s EXCEPCION: %s' % (who, str(e)[:300])))
    page.on('console', lambda m: m.type == 'error' and 'ERR_FAILED' not in m.text and ERR.append('%s console: %s' % (who, m.text[:200])))
    page.goto(BASE); page.wait_for_timeout(1200)
    page.click('button[data-yo="%s"]' % who); page.wait_for_timeout(300)
    page.fill('#pin', '1234'); page.wait_for_timeout(700)
    if page.query_selector('#sheet.on #pin'): page.fill('#pin', '1234'); page.wait_for_timeout(700)
    page.wait_for_timeout(1300)
    return api, ctx, page

def nav(page): return page.eval_on_selector_all('#nav button[data-view]', 'bs => bs.filter(b=>!b.hidden).map(b=>b.getAttribute("data-view"))')
def shot(page, n): page.wait_for_timeout(300); page.screenshot(path=os.path.join(OUT, n + '.png'))
def toast(page): return page.evaluate("() => { const t=document.querySelector('.toast, #toast'); return t ? t.innerText.trim() : ''; }")
TAM = r"""() => [...document.querySelectorAll('#main button, #main a[href], #main input')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&r.top<innerHeight*4}).filter(e=>{const r=e.getBoundingClientRect();return r.width<44||r.height<44}).map(e=>(e.getAttribute('aria-label')||e.textContent||e.className).trim().replace(/\s+/g,' ').slice(0,30)+' '+Math.round(e.getBoundingClientRect().width)+'x'+Math.round(e.getBoundingClientRect().height))"""

with sync_playwright() as pw:
    b = pw.chromium.launch()
    for vp in ((390, 844), (360, 640)):
        tag = '%dx%d' % vp
        api, ctx, page = abrir(b, 'Fran', vp)
        v = nav(page); ok(tag + ' Fran tiene la pestaña Seguimiento', 'seguimiento' in v, v)
        page.click('#nav button[data-view="tareas"]'); page.wait_for_timeout(600)
        barra = page.query_selector('.next-bar[data-view="seguimiento"]')
        ok(tag + ' aviso de Seguimiento arriba de Tareas', bool(barra), barra.inner_text().replace('\n', ' ') if barra else '')
        shot(page, tag + '_01_tareas')
        page.click('#nav button[data-view="seguimiento"]'); page.wait_for_timeout(700)
        shot(page, tag + '_02_seguimiento')
        txt = page.inner_text('#main')
        ok(tag + ' secciones Para hoy / Próximos / Sin fecha', all(x in txt for x in ('Para hoy', 'Próximos días', 'Sin fecha')))
        ok(tag + ' atrasada marcada', 'Atrasada' in txt)
        ok(tag + ' sin nombre muestra el teléfono', '261' in txt and 'Sin nombre' not in txt)
        chicos = page.evaluate(TAM); RES.append('   chicos en Seguimiento: ' + '; '.join(chicos[:12]))
        sw = page.evaluate('document.documentElement.scrollWidth > document.documentElement.clientWidth+1'); ok(tag + ' sin scroll horizontal', not sw)
        # ✔ Hecho + Deshacer
        page.click('[data-seghecho="SG1"]'); page.wait_for_timeout(900)
        ok(tag + ' ✔ Hecho saca la nota de pendientes', page.query_selector('#main [data-seghecho="SG1"]') is None, toast(page))
        shot(page, tag + '_03_hecho')
        und = page.query_selector('.toast button, #toast button, [data-undo]')
        if und:
            und.click(); page.wait_for_timeout(900)
            ok(tag + ' Deshacer la devuelve', page.query_selector('#main [data-seghecho="SG1"]') is not None, toast(page))
        else: ok(tag + ' hay botón Deshacer en el aviso', False)
        # Comentario en la nota sin nombre
        page.click('[data-segver="SG2"]'); page.wait_for_timeout(700)
        shot(page, tag + '_04_nota_ver')
        page.fill('#sgCom', 'La llamé, no atendió (prueba)'); page.click('[data-segcomsave]'); page.wait_for_timeout(900)
        ok(tag + ' comentario guardado', any('La llamé' in h for h in next(s for s in api.seg if s['id'] == 'SG2')['historial']), toast(page))
        page.click('#sheet [data-close]'); page.wait_for_timeout(500)
        ok(tag + ' último comentario visible en la lista', 'La llamé' in page.inner_text('#main'))
        # Nota nueva para mañana
        page.click('[data-segnueva]'); page.wait_for_timeout(600)
        tipos = page.evaluate("() => ({tel: document.getElementById('sgTel').getAttribute('inputmode'), fecha: document.getElementById('sgPara').type})")
        ok(tag + ' teclado de teléfono y fecha nativa', tipos == {'tel': 'tel', 'fecha': 'date'}, tipos)
        page.fill('#sgNom', 'Nueva Prueba'); page.fill('#sgTel', '2615559999'); page.fill('#sgNota', 'Confirmar si viene el jueves (prueba)')
        page.click('[data-segpara]:has-text("Mañana")'); page.wait_for_timeout(300)
        shot(page, tag + '_05_nueva')
        page.click('[data-segsave]'); page.wait_for_timeout(900)
        ok(tag + ' nota nueva guardada y en Próximos', 'Nueva Prueba' in page.inner_text('#main'), toast(page))
        # Repetir cada semana: Hecho corre 7 días
        antes = next(s for s in api.seg if s['id'] == 'SG3')['para']
        page.click('[data-seghecho="SG3"]'); page.wait_for_timeout(900)
        despues = next(s for s in api.seg if s['id'] == 'SG3')
        ok(tag + ' repetir: Hecho la pasa a la semana siguiente', despues['estado'] == 'Pendiente' and despues['para'] != antes, '%s → %s · %s' % (antes, despues['para'], toast(page)))
        # Buscar
        page.fill('#segQ', 'rosa'); page.wait_for_timeout(500)
        t2 = page.inner_text('#main'); ok(tag + ' buscar filtra', 'Rosa' in t2 and 'Damián' not in t2)
        page.keyboard.type('x'); page.wait_for_timeout(300)
        ok(tag + ' el buscador no pierde el foco al escribir', page.evaluate("document.activeElement && document.activeElement.id") == 'segQ')
        page.fill('#segQ', ''); page.wait_for_timeout(300)
        # Desde la ficha de un lead
        page.click('#nav button[data-view="agendar"]'); page.wait_for_timeout(700)
        bt = page.query_selector('[data-open]')
        if bt:
            bt.click(); page.wait_for_timeout(800)
            sn = page.query_selector('#sheet [data-segnueva]')
            ok(tag + ' ficha: botón "nota de seguimiento"', bool(sn))
            if sn:
                sn.scroll_into_view_if_needed(); sn.click(); page.wait_for_timeout(600)
                ok(tag + ' ficha: la nota trae nombre y queda unida al lead', bool(page.input_value('#sgNom')) and 'Queda unida' in page.inner_text('#sheet'))
                shot(page, tag + '_06_desde_ficha')
        ctx.close()
    for who, debe in (('Sol', True), ('Pri', True), ('Karim', True), ('Mica', False), ('Estefanía', False), ('Juan', False)):
        api, ctx, page = abrir(b, who)
        ok('%s %s Seguimiento' % (who, 've' if debe else 'no ve'), ('seguimiento' in nav(page) or (who == 'Karim' and page.query_selector('[data-view="seguimiento"]') is not None)) == debe, nav(page))
        ctx.close()
    b.close()
print('\n'.join(RES)); print('ERRORES:', ERR[:20])
