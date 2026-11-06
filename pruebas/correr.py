# -*- coding: utf-8 -*-
"""Banco de pruebas nocturno (DATOS FALSOS). Uso:
    python3 pruebas/correr.py [carpeta_con_index.html] [carpeta_salida] [roles separados por coma]
Sirve index.html en un puerto local, bloquea TODO pedido a Google (script.google.com,
googleusercontent.com, docs.google.com) y lo responde con datos inventados (datos_falsos.py).
No hay forma de que toque el motor real: cualquier pedido externo que no sea fuentes se aborta.
"""
import sys, os, json, threading, functools, http.server, socketserver, re
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from datos_falsos import FakeApi

SRC = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
OUT = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else 'pruebas/capturas')
ROLES = (sys.argv[3] if len(sys.argv) > 3 else 'Mica,Fran,Karim').split(',')
os.makedirs(OUT, exist_ok=True)

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(Q, directory=SRC))
PORT = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = 'http://127.0.0.1:%d/index.html' % PORT

FUENTE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fuentes', 'archivo-latin-wdth-normal.woff2'), 'rb').read()  # Archivo (OFL), copia local de la fuente de la app
GOOGLE = re.compile(r'script\.google\.com|googleusercontent\.com|docs\.google\.com')
REPORT = {'errores': [], 'pedidos_fallidos': [], 'auditoria': {}, 'externos_bloqueados': 0}

AUDIT_JS = r"""() => {
  const vis = e => { const r=e.getBoundingClientRect(), s=getComputedStyle(e); return r.width>0 && r.height>0 && s.visibility!=='hidden' && s.display!=='none' && r.bottom>0 && r.top<innerHeight*6; };
  const lab = e => (e.getAttribute('aria-label')||e.textContent||e.value||e.className||e.tagName).trim().replace(/\s+/g,' ').slice(0,40);
  const sh = document.querySelector('#sheet.on'); const root = sh || document;
  const small = [];
  root.querySelectorAll('button, a[href], input, select, textarea, [role=button], [data-open], [data-result]').forEach(e => {
    if (!vis(e)) return; const r=e.getBoundingClientRect();
    if (r.width<44 || r.height<44) small.push(lab(e)+' '+Math.round(r.width)+'x'+Math.round(r.height));
  });
  const tiny = new Set();
  (sh||document.body).querySelectorAll('*').forEach(e => {
    if (!vis(e)) return; const t=[...e.childNodes].filter(n=>n.nodeType===3 && n.textContent.trim()).map(n=>n.textContent.trim()).join(' ');
    if (!t) return; const fs=parseFloat(getComputedStyle(e).fontSize); if (fs<14) tiny.add(Math.round(fs*10)/10+'px: '+t.slice(0,40));
  });
  const ov = document.documentElement.scrollWidth > document.documentElement.clientWidth + 1;
  const noLabel = [...root.querySelectorAll('input, select, textarea')].filter(e => vis(e) && !e.labels?.length && !e.getAttribute('aria-label') && !e.getAttribute('placeholder')).map(lab);
  return {en_hoja: !!sh, chicos: small, texto_chico: [...tiny].slice(0,60), scroll_horizontal: ov, sin_label: noLabel, alto_pagina: document.documentElement.scrollHeight};
}"""

def run_role(pw, browser, who, vp, tag):
    api = FakeApi()
    ctx = browser.new_context(viewport=vp['vp'], device_scale_factor=vp['dpr'], is_mobile=True, has_touch=True,
                              locale='es-AR', timezone_id='America/Argentina/Buenos_Aires', service_workers='block')
    page = ctx.new_page()
    page.clock.install(time='2026-11-05T11:20:00-03:00')
    def route(r):
        u = r.request.url
        if GOOGLE.search(u):
            REPORT['externos_bloqueados'] += 1
            try: body = json.loads(r.request.post_data or '{}')
            except Exception: body = {}
            ok, data = api.handle(body.get('fn'), body.get('arg'))
            r.fulfill(status=200, content_type='application/json', body=json.dumps({'ok': True, 'data': data} if ok else {'ok': False, 'error': data}))
        elif u.startswith('http://127.0.0.1:%d/' % PORT): r.continue_()
        elif 'fonts.googleapis.com/css' in u:
            r.fulfill(status=200, content_type='text/css', body="@font-face{font-family:'Archivo';font-style:normal;font-display:swap;font-weight:100 900;font-stretch:62% 125%;src:url(https://fonts.gstatic.com/archivo.woff2) format('woff2')}")
        elif 'fonts.gstatic.com' in u:
            r.fulfill(status=200, content_type='font/woff2', body=FUENTE)
        else: REPORT['externos_bloqueados'] += 1; r.abort()
    page.route('**/*', route)
    page.on('console', lambda m: m.type in ('error',) and 'ERR_FAILED' not in m.text and 'TUNNEL' not in m.text and REPORT['errores'].append('%s/%s console: %s' % (tag, who, m.text[:200])))
    page.on('pageerror', lambda e: REPORT['errores'].append('%s/%s EXCEPCION: %s' % (tag, who, str(e)[:300])))
    page.on('requestfailed', lambda q: (not GOOGLE.search(q.url)) and '127.0.0.1' in q.url and REPORT['pedidos_fallidos'].append(q.url))
    n = [0]
    def shot(name, audit=True):
        n[0] += 1; fn = '%s_%s_%02d_%s.png' % (tag, who, n[0], name)
        page.wait_for_timeout(350); page.screenshot(path=os.path.join(OUT, fn))
        if audit: REPORT['auditoria']['%s/%s/%s' % (tag, who, name)] = page.evaluate(AUDIT_JS)
    page.goto(BASE); page.wait_for_timeout(1200)
    shot('ingreso_nombres')
    page.click('button[data-yo="%s"]' % who); page.wait_for_timeout(300)
    shot('ingreso_pin')
    page.fill('#pin', '1234'); page.wait_for_timeout(700)
    if page.query_selector('#sheet.on #pin'):  # primera vez: crear PIN (pide repetirlo)
        shot('ingreso_pin_repetir')
        page.fill('#pin', '1234'); page.wait_for_timeout(700)
    page.wait_for_timeout(1300)
    shot('inicio')
    views = page.eval_on_selector_all('#nav button[data-view]', 'bs => bs.filter(b=>!b.hidden).map(b=>b.getAttribute("data-view"))')
    REPORT.setdefault('nav', {})[who] = views
    for v in views:
        page.click('#nav button[data-view="%s"]' % v); page.wait_for_timeout(900)
        shot('vista_' + v)
    # Agenda: abrir la primera ficha
    if 'agenda' in views:
        page.click('#nav button[data-view="agenda"]'); page.wait_for_timeout(600)
        b = page.query_selector('[data-open]')
        if b:
            b.click(); page.wait_for_timeout(700); shot('ficha')
            page.mouse.wheel(0, 900); page.wait_for_timeout(300); shot('ficha_abajo')
            c = page.query_selector('#sheet [data-close]');
            if c: c.click(); page.wait_for_timeout(400)
        r = page.query_selector('[data-result]')
        if r:
            r.click(); page.wait_for_timeout(600); shot('cargar_resultado')
            page.click('#sheet [data-res="nofirmo"]'); page.wait_for_timeout(300); shot('res_nofirmo')
            m = page.query_selector('#sheet [data-motivo]')
            if m: m.click(); page.wait_for_timeout(200)
            page.click('#sheet [data-save]'); page.wait_for_timeout(500); shot('res_guardado')
            u = page.query_selector('#toast [data-undo]')
            if u: u.click(); page.wait_for_timeout(900); shot('res_deshecho')
            c = page.query_selector('#sheet.on [data-close]')
            if c: c.click(); page.wait_for_timeout(400)
    if 'agendar' in views:
        page.click('#nav button[data-view="agendar"]'); page.wait_for_timeout(600)
        b = page.query_selector('#agList [data-open], #agList [data-pa], #agList button')
        if b:
            b.click(); page.wait_for_timeout(700); shot('agendar_ficha')
    ctx.close()
    return api

with sync_playwright() as pw:
    try: browser = pw.chromium.launch()
    except Exception: browser = pw.chromium.launch(channel='chrome')
    for vp in [{'tag': 'cel390', 'vp': {'width': 390, 'height': 844}, 'dpr': 3}, {'tag': 'cel360', 'vp': {'width': 360, 'height': 640}, 'dpr': 2}]:
        for who in ROLES:
            api = run_role(pw, browser, who, vp, vp['tag'])
            if api.sin_fake: REPORT.setdefault('sin_fake', []).extend(sorted(api.sin_fake))
    browser.close()
srv.shutdown()
json.dump(REPORT, open(os.path.join(OUT, 'reporte.json'), 'w'), ensure_ascii=False, indent=1)
print(json.dumps({'errores': REPORT['errores'][:40], 'nav': REPORT.get('nav'), 'sin_fake': sorted(set(REPORT.get('sin_fake', []))), 'bloqueados': REPORT['externos_bloqueados']}, ensure_ascii=False, indent=1))
