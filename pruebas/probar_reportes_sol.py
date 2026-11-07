# -*- coding: utf-8 -*-
"""Prueba de la rama mejora/2026-11-07-reportes-sol con DATOS FALSOS.
Uso: python3 pruebas/probar_reportes_sol.py <carpeta_con_index.html> <carpeta_salida>
Comentarios de Sol -> Tareas de Fran y Pri -> Hecho; registro de uso (sin botón de reportes).
Bloquea todo pedido a Google y lo responde con datos inventados (como correr.py)."""
import sys, os, json, threading, functools, http.server, socketserver, re, copy
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import datos_falsos as DF
from datos_falsos import FakeApi

SRC = os.path.abspath(sys.argv[1]); OUT = os.path.abspath(sys.argv[2]); os.makedirs(OUT, exist_ok=True)
DF.PERMISOS['Sol'] = dict(DF.PERMISOS['Sol'], comentar=True)

class Api(FakeApi):
    """Igual que el banco, más lo nuevo: comentarios de Sol (consulta interna 'control'), saveFeedback y logUso."""
    compartido = {'feedback': [], 'uso': []}
    def get_data(self, who):
        d = super().get_data(who)
        d['respuestas'] = dict(d.get('respuestas') or {}, control=['Hecho'])
        if who in ('Fran', 'Pri'):
            todos = self.leads + self.pa
            d['paraMi'] = [copy.deepcopy(l) for l in todos if any(x.get('tipo') == 'control' and x.get('abierta') and x.get('a') == 'Intakers' for x in l.get('internas', []))]
        return d
    def handle(self, fn, arg):
        arg = arg or {}; who = self._quien(arg) or arg.get('who')
        if fn == 'pedirInterna' and arg.get('tipo') == 'control':
            if not DF.PERMISOS.get(who, {}).get('comentar'): return False, 'Los comentarios para los intakers los deja Sol.'
            l = self._find(arg.get('id'))
            if not (arg.get('nota') or '').strip(): return False, 'Escribí el comentario.'
            l.setdefault('internas', []).append({'i': len(l['internas']), 'cuando': '05/11/2026 11:25', 'de': who, 'a': 'Intakers', 'tipo': 'control', 'estado': 'Pendiente', 'nota': arg['nota'], 'resp': '', 'abierta': True})
            return True, {'lead': copy.deepcopy(l), 'tel': ''}
        if fn == 'responderInterna':
            l = self._find(arg.get('id'))
            for x in l.get('internas', []):
                if x['i'] == int(arg.get('i')):
                    if x['a'] == 'Intakers' and who not in ('Fran', 'Pri', 'Karim', 'Julián'): return False, 'Esa consulta es para Intakers.'
                    x.update(estado=arg.get('respuesta'), abierta=False, resp='05/11 11:40 (%s)' % who)
            return True, copy.deepcopy(l)
        if fn == 'saveFeedback':
            if len((arg.get('texto') or '').strip()) < 3: return False, 'Contá en una frase qué pasó.'
            self.compartido['feedback'].append({'who': who, **{k: arg.get(k) for k in ('tipo', 'texto', 'pantalla', 'ctx')}}); return True, {'ok': True}
        if fn == 'logUso':
            self.compartido['uso'].append({'who': who, 'items': arg.get('items'), 'v': arg.get('v'), 'disp': arg.get('disp')}); return True, {'ok': True, 'n': len(arg.get('items') or [])}
        return super().handle(fn, arg)

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(Q, directory=SRC)); PORT = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = 'http://127.0.0.1:%d/index.html' % PORT
FUENTE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fuentes', 'archivo-latin-wdth-normal.woff2'), 'rb').read()
GOOGLE = re.compile(r'script\.google\.com|googleusercontent\.com|docs\.google\.com')
R = {'errores': [], 'pasos': []}
API = Api()  # un solo estado falso compartido: lo que deja Sol lo ve Fran

def ok(cond, msg):
    R['pasos'].append(('OK ' if cond else 'FALLA ') + msg)

def abrir(browser, who, vp=(390, 844)):
    ctx = browser.new_context(viewport={'width': vp[0], 'height': vp[1]}, device_scale_factor=3, is_mobile=True, has_touch=True,
                              locale='es-AR', timezone_id='America/Argentina/Buenos_Aires', service_workers='block')
    page = ctx.new_page(); page.clock.install(time='2026-11-05T11:20:00-03:00')
    def route(r):
        u = r.request.url
        if GOOGLE.search(u):
            try: body = json.loads(r.request.post_data or '{}')
            except Exception: body = {}
            k, data = API.handle(body.get('fn'), body.get('arg'))
            r.fulfill(status=200, content_type='application/json', body=json.dumps({'ok': True, 'data': data} if k else {'ok': False, 'error': data}))
        elif u.startswith('http://127.0.0.1:%d/' % PORT): r.continue_()
        elif 'fonts.googleapis.com/css' in u: r.fulfill(status=200, content_type='text/css', body="@font-face{font-family:'Archivo';src:url(https://fonts.gstatic.com/a.woff2)}")
        elif 'fonts.gstatic.com' in u: r.fulfill(status=200, content_type='font/woff2', body=FUENTE)
        else: r.abort()
    page.route('**/*', route)
    page.on('pageerror', lambda e: R['errores'].append('%s EXCEPCION: %s' % (who, str(e)[:300])))
    page.on('console', lambda m: m.type == 'error' and 'ERR_FAILED' not in m.text and R['errores'].append('%s console: %s' % (who, m.text[:200])))
    page.goto(BASE); page.wait_for_timeout(1200)
    page.click('button[data-yo="%s"]' % who); page.wait_for_timeout(300)
    page.fill('#pin', '1234'); page.wait_for_timeout(700)
    if page.query_selector('#sheet.on #pin'): page.fill('#pin', '1234'); page.wait_for_timeout(700)
    page.wait_for_timeout(1300)
    return ctx, page

def shot(page, name): page.wait_for_timeout(350); page.screenshot(path=os.path.join(OUT, name + '.png'))

with sync_playwright() as pw:
    try: browser = pw.chromium.launch()
    except Exception: browser = pw.chromium.launch(channel='chrome')
    # 1) Sol deja un comentario desde la ficha de un lead por agendar
    ctx, page = abrir(browser, 'Sol')
    page.click('#nav button[data-view="agendar"]'); page.wait_for_timeout(800)
    fid = page.evaluate("() => { const b=[...document.querySelectorAll('main [data-ficha]')][0]; return b && b.getAttribute('data-ficha'); }")
    lead = API._find(fid); ok(bool(lead), 'Hay un lead en Agendar para abrir (%s)' % fid)
    page.click('main [data-ficha="%s"]' % fid); page.wait_for_timeout(800)
    b = page.query_selector('#sheet [data-comsol]'); ok(bool(b), 'Sol ve "Dejar un comentario a los intakers" en la ficha')
    if b:
        b.scroll_into_view_if_needed(); shot(page, '01_sol_ficha_boton'); b.click(); page.wait_for_timeout(500)
        shot(page, '02_sol_comentario_vacio')
        page.click('#sheet [data-comsolenviar]'); page.wait_for_timeout(500)
        ok('Escribí el comentario' in (page.inner_text('#toast') or ''), 'Sin texto avisa "Escribí el comentario."')
        page.fill('#csNota', '[PRUEBA] Falta el resumen y la fase no es C: llamalo de nuevo.'); page.click('#sheet [data-comsolenviar]'); page.wait_for_timeout(900)
        ok(not page.query_selector('#sheet.on'), 'Al mandar se cierra la hoja'); ok('intakers' in (page.inner_text('#toast') or ''), 'Aviso "Les llegó a los intakers"')
        shot(page, '03_sol_enviado')
    ok(any(x['tipo'] == 'control' and x['abierta'] for x in lead['internas']), 'El comentario quedó en el lead (pendiente, para Intakers)')
    # Una abogada sin permiso no ve el botón
    ctx.close(); ctx, page = abrir(browser, 'Mica')
    page.click('#nav button[data-view="agendar"]'); page.wait_for_timeout(800)
    page.click('main [data-ficha="%s"]' % fid); page.wait_for_timeout(800)
    ok(page.query_selector('#sheet.on') and not page.query_selector('#sheet [data-comsol]'), 'Mica abre la misma ficha y no ve el botón de comentarios (solo Sol)')
    page.click('#sheet [data-close]'); page.wait_for_timeout(500)
    page.click('#nav button[data-view="agenda"]'); page.wait_for_timeout(700)
    # 2) Ya no hay botón de reportes (Karim lo sacó)
    ok(not page.query_selector('[data-fbabrir]'), 'No aparece "Algo no anda o tengo una idea"')
    # 3) Registro de uso: al salir de la app se manda agrupado
    page.evaluate("() => { Object.defineProperty(document, 'visibilityState', {configurable:true, get:()=>'hidden'}); Object.defineProperty(document, 'hidden', {configurable:true, get:()=>true}); document.dispatchEvent(new Event('visibilitychange')); }")
    page.wait_for_timeout(800)
    u = API.compartido['uso'][-1] if API.compartido['uso'] else {}
    tipos = sorted(set(i.get('t') for i in (u.get('items') or [])))
    ok(u.get('who') == 'Mica' and 'resumen' in tipos and 'carga' in tipos, 'Registro de uso enviado al salir (tipos: %s, disp: %s)' % (tipos, u.get('disp')))
    ok(not any('logUso' in json.dumps(i) for i in (u.get('items') or [])), 'El registro no se cuenta a sí mismo')
    ctx.close()
    # 4) Fran ve el comentario en Tareas y lo marca Hecho
    ctx, page = abrir(browser, 'Fran')
    page.click('#nav button[data-view="tareas"]'); page.wait_for_timeout(700)
    html = page.inner_html('main'); ok('Comentarios de Sol' in html, 'Fran ve el grupo "Comentarios de Sol" en Tareas')
    badge = page.inner_text('#badgeT') if page.query_selector('#badgeT:not([hidden])') else ''
    sec = page.query_selector('main h2:has-text("Comentarios de Sol")')
    if sec: sec.scroll_into_view_if_needed()
    shot(page, '07_fran_tareas_comentario')
    ok('consulta para vos' not in page.inner_text('main').split('Tareas')[0], 'No aparece duplicado en el aviso de arriba')
    h = page.query_selector('main [data-intresp$="|Hecho"]'); ok(bool(h), 'Botón ✔ Hecho')
    if h:
        h.click(); page.wait_for_timeout(900)
        ok('Comentarios de Sol' not in page.inner_html('main'), 'Después de Hecho desaparece de Tareas')
        badge2 = page.inner_text('#badgeT') if page.query_selector('#badgeT:not([hidden])') else ''
        ok(badge != badge2, 'Baja el número de Tareas (%s → %s)' % (badge or '0', badge2 or '0'))
        shot(page, '08_fran_hecho')
    ok(any(x['tipo'] == 'control' and not x['abierta'] and 'Fran' in x['resp'] for x in lead['internas']), 'En el lead queda Hecho por Fran')
    ctx.close()
    # 5) Celular chico: Tareas con el comentario sin scroll horizontal
    ctx, page = abrir(browser, 'Pri', (360, 640))
    page.click('#nav button[data-view="tareas"]'); page.wait_for_timeout(600); shot(page, '09_pri_tareas_360')
    ok(not page.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth + 1"), 'Sin scroll horizontal en 360 px')
    ctx.close(); browser.close()
srv.shutdown()
json.dump(R, open(os.path.join(OUT, 'resultado.json'), 'w'), ensure_ascii=False, indent=1)
print('\n'.join(R['pasos'])); print('ERRORES:', R['errores'] or 'ninguno')
