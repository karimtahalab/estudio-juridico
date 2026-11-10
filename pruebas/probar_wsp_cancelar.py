# -*- coding: utf-8 -*-
"""Banco (DATOS FALSOS): tocar Cancelar mientras dice "Enviando…" y volver a tocar 📤 Enviar del mismo lead (toques reales).
Uso: python3 pruebas/probar_wsp_cancelar.py <carpeta con index.html> <carpeta de capturas>"""
import sys, os, json
sys.argv = [sys.argv[0], sys.argv[1], sys.argv[2], 'Pri']
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import explora_base as B
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    br = pw.chromium.launch(); api = B.FakeApi(); ret, env = [], []
    ctx = br.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, is_mobile=True, has_touch=True, locale='es-AR', timezone_id='America/Argentina/Buenos_Aires', service_workers='block')
    pg = ctx.new_page(); pg.clock.install(time='2026-11-05T11:20:00-03:00')
    def route(r):
        u = r.request.url
        if B.GOOGLE.search(u):
            b = json.loads(r.request.post_data or '{}')
            if b.get('fn') == 'enviarWsp': env.append(b['arg']['id']); ret.append((r, b)); return
            ok, d = api.handle(b.get('fn'), b.get('arg')); r.fulfill(status=200, content_type='application/json', body=json.dumps({'ok': ok, 'data': d} if ok else {'ok': False, 'error': d}))
        elif u.startswith('http://127.0.0.1:%d/' % B.PORT): r.continue_()
        else: r.abort()
    pg.route('**/*', route)
    pg.goto(B.BASE); pg.wait_for_timeout(1000); pg.click('button[data-yo="Pri"]'); pg.wait_for_timeout(300)
    pg.fill('#pin', '1234'); pg.wait_for_timeout(700)
    if pg.query_selector('#sheet.on #pin'): pg.fill('#pin', '1234'); pg.wait_for_timeout(700)
    pg.wait_for_timeout(1200); pg.click('#nav button[data-view="tareas"]'); pg.wait_for_timeout(900)
    pg.locator('.sc-env').first.click(); pg.wait_for_timeout(500); pg.click('#wspDlg.on [data-wspok]'); pg.wait_for_timeout(500)
    can = pg.query_selector('#wspDlg.on [data-wspx]')
    print('Cancelar disponible mientras sale:', bool(can))
    if can: can.click(); pg.wait_for_timeout(400)
    try:
        pg.locator('.sc-env').first.click(timeout=2000); pg.wait_for_timeout(500)
        if pg.query_selector('#wspDlg.on [data-wspok]'): pg.click('#wspDlg.on [data-wspok]'); pg.wait_for_timeout(400)
    except Exception as e: print('segundo toque no posible:', str(e)[:80])
    for r, b in ret: ok, d = api.handle('enviarWsp', b['arg']); r.fulfill(status=200, content_type='application/json', body=json.dumps({'ok': True, 'data': d}))
    pg.wait_for_timeout(800); pg.screenshot(path=os.path.join(B.OUT, 'cancelar_final.png'))
    print('enviarWsp pedidos:', env)
    br.close()
B.srv.shutdown()
