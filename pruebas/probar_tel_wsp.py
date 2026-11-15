# -*- coding: utf-8 -*-
"""Banco (DATOS FALSOS): 📤 Enviar a un lead con el teléfono mal cargado (8 números, como el aviso de Pri del 14/11).
Mide: cuánto tarda en enterarse, si se manda pedido al motor, y si puede corregir el teléfono y mandarlo sin salir de Tareas.
Uso: python3 pruebas/probar_tel_wsp.py <carpeta con index.html> <carpeta de capturas> [etiqueta] [ancho] [alto]"""
import sys, os, json, time
TAG = sys.argv[3] if len(sys.argv) > 3 else 'x'
W = int(sys.argv[4]) if len(sys.argv) > 4 else 390
H = int(sys.argv[5]) if len(sys.argv) > 5 else 844
sys.argv = [sys.argv[0], sys.argv[1], sys.argv[2], 'Pri']
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import explora_base as B
from playwright.sync_api import sync_playwright

LEAD = 'P077'
DEMORA = 3.5  # el motor real tarda 3-5 s en contestar enviarWsp (registro de uso)
res = {'tag': TAG, 'vp': '%dx%d' % (W, H)}
with sync_playwright() as pw:
    br = pw.chromium.launch(); api = B.FakeApi(); env, errs = [], []
    ctx = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=2, is_mobile=True, has_touch=True, locale='es-AR', timezone_id='America/Argentina/Buenos_Aires', service_workers='block')
    pg = ctx.new_page(); pg.clock.install(time='2026-11-05T11:20:00-03:00')
    pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    def route(r):
        u = r.request.url
        if B.GOOGLE.search(u):
            b = json.loads(r.request.post_data or '{}')
            if b.get('fn') == 'enviarWsp': env.append(b['arg']['id']); time.sleep(DEMORA)
            ok, d = api.handle(b.get('fn'), b.get('arg')); r.fulfill(status=200, content_type='application/json', body=json.dumps({'ok': ok, 'data': d} if ok else {'ok': False, 'error': d}))
        elif u.startswith('http://127.0.0.1:%d/' % B.PORT): r.continue_()
        else: r.abort()  # graph.facebook.com, uChat y todo lo externo: bloqueado
    pg.route('**/*', route)
    shot = lambda n: pg.screenshot(path=os.path.join(B.OUT, '%s_%dx%d_%s.png' % (TAG, W, H, n)))
    pg.goto(B.BASE); pg.wait_for_timeout(1000); pg.click('button[data-yo="Pri"]'); pg.wait_for_timeout(300)
    pg.fill('#pin', '1234'); pg.wait_for_timeout(700)
    if pg.query_selector('#sheet.on #pin'): pg.fill('#pin', '1234'); pg.wait_for_timeout(700)
    pg.wait_for_timeout(1200); pg.click('#nav button[data-view="tareas"]'); pg.wait_for_timeout(900)
    fila = pg.locator('li.sc-of', has_text='Adriana')
    fila.scroll_into_view_if_needed(); pg.wait_for_timeout(300)
    res['fila_tel'] = fila.locator('.ct').inner_text()
    shot('1_fila')
    t0 = time.time(); toques = 1
    fila.locator('.sc-env').click(); pg.wait_for_timeout(300)
    if pg.query_selector('#wspDlg.on [data-wspok]'):  # main: muestra la vista previa como si todo estuviera bien
        shot('2_vista_previa'); pg.click('#wspDlg.on [data-wspok]'); toques += 1
        pg.wait_for_function("() => /no tiene 10/.test(document.getElementById('toast').textContent)", timeout=15000)
    res['seg_hasta_enterarse'] = round(time.time() - t0, 1)
    pg.wait_for_timeout(200); shot('3_aviso')
    res['aviso'] = (pg.text_content('#wspDlg.on') or '').strip() if pg.query_selector('#wspDlg.on') else pg.text_content('#toast').strip()
    # Corregir: botón del aviso (rama) o del toast (main)
    b = pg.query_selector('#wspDlg.on [data-wspcorr]') or pg.query_selector('#toast button:not([data-undo])')
    res['boton_corregir'] = (b.inner_text().strip() if b else '')
    if b and 'Corregir' in res['boton_corregir']:
        b.click(); toques += 1
    else:  # sin atajo: abrir la ficha y tocar "Corregir datos"
        pg.click('#wspDlg.on [data-wspx]') if pg.query_selector('#wspDlg.on [data-wspx]') else None
        fila.locator('.cn').click(); pg.wait_for_timeout(500); pg.click('#sheet [data-fimodo="datos"]'); toques += 2
    pg.wait_for_timeout(400)
    res['foco_en_tel'] = pg.evaluate("() => document.activeElement && document.activeElement.id")
    shot('4_corregir')
    if res['foco_en_tel'] != 'fdTel': pg.click('#fdTel'); toques += 1
    pg.fill('#fdTel', '2615550177'); pg.click('#sheet [data-datosave]'); toques += 1
    pg.wait_for_timeout(800); pg.click('#sheet [data-close]'); toques += 1; pg.wait_for_timeout(500)
    fila = pg.locator('li.sc-of', has_text='Adriana'); fila.locator('.sc-env').click(); toques += 1; pg.wait_for_timeout(300)
    pg.click('#wspDlg.on [data-wspok]'); toques += 1
    pg.wait_for_timeout(int(DEMORA * 1000) + 1200); shot('5_enviado')
    res['toques_total'] = toques
    res['enviarWsp'] = env; res['rechazados_motor'] = api.wsp_rechazados; res['mandados_ok'] = [x['id'] for x in api.wsp_enviados]
    # Lead sano: sigue igual (vista previa al instante)
    pg.locator('li.sc-of .sc-env').first.click(); pg.wait_for_timeout(300)
    res['lead_sano_vista_previa'] = bool(pg.query_selector('#wspDlg.on [data-wspok]'))
    res['errores_js'] = errs
    br.close()
B.srv.shutdown()
print(json.dumps(res, ensure_ascii=False, indent=1))
