# -*- coding: utf-8 -*-
"""Casos borde de mejora/2026-11-22-flujo-confirmaciones. DATOS FALSOS; todo lo externo bloqueado.
Uso: python3 pruebas/probar_confirmaciones.py <carpeta index.html> <salida>"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import explora_base as B
from playwright.sync_api import sync_playwright
OUT = B.OUT; vp = {'vp': {'width': 390, 'height': 844}}
R = {}
def ok(k, v): R[k] = v
with sync_playwright() as pw:
    br = pw.chromium.launch()
    # 1) Destildar uno: salen 4
    page, ctx, shot, api = B.explora(br, 'Pri', vp, 'pc', OUT)
    page.click('#nav button[data-view="tareas"]'); page.wait_for_timeout(1200)
    page.click('[data-cftodos="todo"]'); page.wait_for_timeout(500)
    page.locator('#wspDlg [data-cfchk="1"]').click(); page.wait_for_timeout(200)
    ok('1_boton_tras_destildar', page.locator('#wspDlg [data-cflote]').inner_text())
    page.locator('#wspDlg [data-cflote]').click(); page.wait_for_timeout(3000)
    ok('1_enviados', [e['id'] for e in api.wsp_enviados])
    ok('1_barra', page.locator('.cf-bar').first.inner_text().replace('\n', ' '))
    # 2) La sección: botón "a los N que faltan" ya no está si queda 1 (queda el 📤 de la fila)
    ok('2_botones_seccion', page.locator('[data-cftodos="hoy"],[data-cftodos="previa"]').count())
    # 3) Tocar el 📤 gris de alguien ya mandado: avisa "Ya se mandó" y pide Enviar igual
    page.locator('li.tk .cf-ya').first.click(); page.wait_for_timeout(500)
    ok('3_aviso', page.locator('#wspDlg').inner_text().replace('\n', ' ')[:200])
    page.locator('#wspDlg [data-wspx]').first.click(); page.wait_for_timeout(300)
    ctx.close()
    # 4) El motor rechaza uno y se corta otro
    page, ctx, shot, api = B.explora(br, 'Fran', vp, 'pc', OUT)
    h0 = api.handle
    def h(fn, arg):
        if fn == 'enviarWsp' and (arg or {}).get('id') == 'P007': return False, 'La plantilla está en revisión (prueba).'
        return h0(fn, arg)
    api.handle = h
    page.route('**/*', lambda r: r.abort() if ('enviarWsp' in (r.request.post_data or '') and 'P008' in (r.request.post_data or '')) else r.fallback())
    page.click('#nav button[data-view="tareas"]'); page.wait_for_timeout(1200)
    page.click('[data-cftodos="todo"]'); page.wait_for_timeout(500)
    page.locator('#wspDlg [data-cflote]').click(); page.wait_for_timeout(3500)
    ok('4_toast', page.locator('#toast').inner_text().replace('\n', ' '))
    shot('fallas')
    ok('4_enviados', [e['id'] for e in api.wsp_enviados])
    ok('4_barra', page.locator('.cf-bar').first.inner_text().replace('\n', ' '))
    ctx.close()
    # 5) Mica (abogada) no ve nada de esto; Karim (admin) sí
    for who in ('Mica', 'Karim'):
        page, ctx, shot, api = B.explora(br, who, vp, 'pc', OUT)
        b = page.locator('#nav button[data-view="tareas"]:not([hidden])')
        if b.count(): b.click(); page.wait_for_timeout(1200)
        ok('5_' + who, {'tareas': b.count(), 'barra': page.locator('.cf-bar').count(), 'mandar': page.locator('[data-cftodos]').count()})
        ctx.close()
    # 6) WhatsApp oficial apagado: sin botón de mandar, todo "por 💬"
    import datos_falsos as DF
    w0 = DF.wsp_datos
    DF.wsp_datos = lambda who: dict(w0(who), activo=False)
    page, ctx, shot, api = B.explora(br, 'Fran', vp, 'pc', OUT)
    page.click('#nav button[data-view="tareas"]'); page.wait_for_timeout(1500)
    ok('6_apagado', {'barra': page.locator('.cf-bar').first.inner_text().replace('\n', ' ') if page.locator('.cf-bar').count() else '', 'mandar': page.locator('[data-cftodos]').count()})
    DF.wsp_datos = w0
    ctx.close()
    R['errores'] = B.REPORT['errores']
    br.close()
print(json.dumps(R, ensure_ascii=False, indent=1))
