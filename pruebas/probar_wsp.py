# -*- coding: utf-8 -*-
"""Banco (DATOS FALSOS): 📤 Enviar de Sin contactar con un servidor que tarda como el real (enviarWsp ~7 s, hasta 24 s).
Uso: python3 pruebas/probar_wsp.py <carpeta con index.html> <carpeta de capturas> [Pri|Fran]
No sale ningún WhatsApp: enviarWsp lo responde datos_falsos.py (ok falso) y todo lo externo se aborta.
Mide: cuánto queda trabada la pantalla, si se puede seguir con el próximo lead mientras sale el anterior,
cuántas veces se manda cada uno (doble toque), que el lead se marque una sola vez y qué pasa si el envío falla."""
import sys, os, json, time
sys.argv = [sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else 'Pri']
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import explora_base as B
from playwright.sync_api import sync_playwright

WHO = B.ROLES[0]
RES = {'pasos': [], 'errores': B.REPORT['errores']}
def paso(k, v): RES['pasos'].append([k, v]); print(k, '→', v, flush=True)

def correr(browser, vp, tag, falla=False):
    api = B.FakeApi()
    ctx = browser.new_context(viewport=vp, device_scale_factor=2, is_mobile=True, has_touch=True, locale='es-AR', timezone_id='America/Argentina/Buenos_Aires', service_workers='block')
    page = ctx.new_page(); page.clock.install(time='2026-11-05T11:20:00-03:00')
    retenidos, envios = [], []
    def route(r):
        u = r.request.url
        if B.GOOGLE.search(u):
            try: body = json.loads(r.request.post_data or '{}')
            except Exception: body = {}
            if body.get('fn') == 'enviarWsp':
                envios.append(body.get('arg', {}).get('id')); retenidos.append((r, body)); return   # se contesta más tarde (servidor lento)
            ok, data = api.handle(body.get('fn'), body.get('arg'))
            r.fulfill(status=200, content_type='application/json', body=json.dumps({'ok': True, 'data': data} if ok else {'ok': False, 'error': data}))
        elif u.startswith('http://127.0.0.1:%d/' % B.PORT): r.continue_()
        elif 'fonts.googleapis.com/css' in u: r.fulfill(status=200, content_type='text/css', body="")
        elif 'fonts.gstatic.com' in u: r.fulfill(status=200, content_type='font/woff2', body=B.FUENTE)
        else: r.abort()   # graph.facebook.com, uChat y cualquier otro: abortado
    def soltar():
        while retenidos:
            r, body = retenidos.pop(0)
            if falla: ok, data = False, ['La plantilla no está aprobada (prueba).', 'Sin conexión. Revisá internet y probá de nuevo.'][len(retenidos) % 2]
            else: ok, data = api.handle('enviarWsp', body.get('arg'))
            r.fulfill(status=200, content_type='application/json', body=json.dumps({'ok': True, 'data': data} if ok else {'ok': False, 'error': data}))
    page.route('**/*', route)
    page.on('pageerror', lambda e: B.REPORT['errores'].append('%s EXC: %s' % (tag, str(e)[:300])))
    n = [0]
    def shot(name):
        n[0] += 1; page.wait_for_timeout(350); page.screenshot(path=os.path.join(B.OUT, '%s_%s_%02d_%s.png' % (tag, WHO, n[0], name)))
    page.goto(B.BASE); page.wait_for_timeout(1000)
    page.click('button[data-yo="%s"]' % WHO); page.wait_for_timeout(300)
    page.fill('#pin', '1234'); page.wait_for_timeout(700)
    if page.query_selector('#sheet.on #pin'): page.fill('#pin', '1234'); page.wait_for_timeout(700)
    page.wait_for_timeout(1200)
    page.click('#nav button[data-view="tareas"]'); page.wait_for_timeout(900)
    bs = page.query_selector_all('.sc-env')
    paso(tag + ' botones 📤 Enviar en Sin contactar', len(bs))
    if not bs: shot('sin_botones'); ctx.close(); return
    bs[0].scroll_into_view_if_needed(); page.wait_for_timeout(300)
    nombre1 = page.evaluate("b=>b.closest('li').querySelector('b').textContent", bs[0])
    bs[0].click(); page.wait_for_timeout(500); shot('vista_previa')
    paso(tag + ' vista previa abierta', bool(page.query_selector('#wspDlg.on [data-wspok]')))
    t0 = time.time()
    page.click('#wspDlg.on [data-wspok]')
    try: page.click('#wspDlg.on [data-wspok]', timeout=400)   # doble toque apurado
    except Exception: pass
    page.wait_for_timeout(500); shot('enviando')
    trabado = bool(page.query_selector('#wspDlg.on'))
    paso(tag + ' después de tocar Enviar la ventana sigue tapando la pantalla', trabado)
    # ¿Puede seguir con el próximo lead mientras sale el primero?
    otros = [b for b in page.query_selector_all('.sc-env') if page.evaluate("b=>b.closest('li').querySelector('b').textContent", b) != nombre1]
    pudo2 = False
    if otros and not trabado:
        try:
            otros[0].click(timeout=1500); page.wait_for_timeout(500)
            pudo2 = bool(page.query_selector('#wspDlg.on [data-wspok]'))
            if pudo2: shot('segundo_lead'); page.click('#wspDlg.on [data-wspok]'); page.wait_for_timeout(400)
        except Exception as e: paso(tag + ' segundo lead error', str(e)[:120])
    paso(tag + ' pudo mandar al próximo lead sin esperar', pudo2)
    # Fila del primero mientras sale: ¿se puede volver a tocar 📤?
    fila = page.evaluate("n=>{var li=[...document.querySelectorAll('.cl.sc li')].find(x=>x.textContent.indexOf(n)!==-1); if(!li) return 'no está'; var b=li.querySelector('.sc-env'); return b ? (b.disabled?'deshabilitado: ':'habilitado: ')+b.textContent.trim() : 'sin botón';}", nombre1)
    paso(tag + ' fila del primero mientras se manda', fila)
    try:
        page.evaluate("n=>{var li=[...document.querySelectorAll('.cl.sc li')].find(x=>x.textContent.indexOf(n)!==-1); var b=li&&li.querySelector('.sc-env'); if(b) b.click();}", nombre1); page.wait_for_timeout(500)
        if page.query_selector('#wspDlg.on [data-wspok]'): page.click('#wspDlg.on [data-wspok]'); page.wait_for_timeout(300)
    except Exception: pass
    page.wait_for_timeout(1500)
    soltar(); page.wait_for_timeout(1200); shot('despues')
    paso(tag + ' enviarWsp pedidos (ids)', envios)
    paso(tag + ' toast', page.evaluate("()=>{var t=document.getElementById('toast'); return t.className+' | '+t.textContent}"))
    paso(tag + ' quedan en Sin contactar', page.evaluate("()=>[...document.querySelectorAll('.cl.sc li b')].map(b=>b.textContent)"))
    paso(tag + ' botones de Sin contactar al final', page.evaluate("()=>[...document.querySelectorAll('.cl.sc li')].map(li=>{var b=li.querySelector('.sc-env');return li.querySelector('b').textContent+': '+(b?b.textContent.trim():'-')})"))
    if falla:
        b = page.query_selector('.sc-env')
        if b: b.click(); page.wait_for_timeout(500); shot('reintentar'); paso(tag + ' vista previa al reintentar', page.evaluate("()=>{var d=document.querySelector('#wspDlg.on');return d?d.innerText.replace(/\\s+/g,' ').slice(0,300):'-'}"))
    paso(tag + ' ventana abierta al final', bool(page.query_selector('#wspDlg.on')))
    paso(tag + ' WhatsApp falsos registrados', len(api.wsp_enviados))
    ctx.close()

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    correr(browser, {'width': 390, 'height': 844}, 'ok390')
    correr(browser, {'width': 360, 'height': 640}, 'falla360', falla=True)
    browser.close()
B.srv.shutdown()
json.dump(RES, open(os.path.join(B.OUT, 'wsp.json'), 'w'), ensure_ascii=False, indent=1)
print('ERRORES:', RES['errores'])
