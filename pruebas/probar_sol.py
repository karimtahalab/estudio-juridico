# -*- coding: utf-8 -*-
"""Comentarios de Sol a los intakers, de punta a punta, con DATOS FALSOS.
Uso: python3 pruebas/probar_sol.py <carpeta con index.html> <carpeta capturas>
Sol abre una consulta de la agenda → ve la zona → deja un comentario. Pri entra → lo ve en Tareas → ✔ Hecho → desaparece.
Mica (abogada sin permiso) no ve el botón."""
import sys, os, json
sys.argv = [sys.argv[0], sys.argv[1] if len(sys.argv) > 1 else '.', sys.argv[2] if len(sys.argv) > 2 else 'pruebas/capturas_sol', 'Sol']
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import explora_base as B
from playwright.sync_api import sync_playwright
OUT = B.OUT; os.makedirs(OUT, exist_ok=True)
VP = {'vp': {'width': 390, 'height': 844}}
ok = {}
with sync_playwright() as pw:
    br = pw.chromium.launch()
    page, ctx, shot, api = B.explora(br, 'Sol', VP, 'sol', OUT)
    page.click('nav button[data-view="agenda"]'); page.wait_for_timeout(500)
    shot('agenda_al_entrar')
    page.click('button[data-abog="Todas"]'); page.wait_for_timeout(500)
    o = page.query_selector('[data-open]'); o.click(); page.wait_for_timeout(800)
    z = page.query_selector('#sheet.on .ctl-zona'); ok['sol_ve_zona'] = bool(z)
    b = page.query_selector('#sheet.on [data-comsol]'); ok['sol_ve_boton'] = bool(b)
    if b:
        b.scroll_into_view_if_needed(); shot('zona'); b.click(); page.wait_for_timeout(600)
        page.fill('#csNota', 'Falta el resumen del caso (prueba)'); shot('escribe')
        page.click('[data-comsolenviar]'); page.wait_for_timeout(1200)
        ok['sol_toast'] = page.inner_text('body').count('Les llegó a los intakers') > 0
        shot('mandado')
    estado = (api.leads, api.pa, api.sc); ctx.close()
    page, ctx, shot, api2 = B.explora(br, 'Pri', VP, 'sol', OUT)
    api2.leads, api2.pa, api2.sc = estado
    page.click('#btnRefresh'); page.wait_for_timeout(1500)
    page.click('nav button[data-view="tareas"]'); page.wait_for_timeout(600)
    t = page.inner_text('body'); ok['pri_ve_en_tareas'] = 'Falta el resumen del caso (prueba)' in t
    h = page.query_selector('[data-intresp$="|Hecho"]'); ok['pri_boton_hecho'] = bool(h)
    if h:
        h.scroll_into_view_if_needed(); shot('pri_tareas'); h.click(); page.wait_for_timeout(1500)
        ok['pri_desaparece'] = 'Falta el resumen del caso (prueba)' not in page.inner_text('body'); shot('pri_hecho')
    ctx.close()
    page, ctx, shot, api3 = B.explora(br, 'Mica', VP, 'sol', OUT)
    page.click('nav button[data-view="agenda"]'); page.wait_for_timeout(500)
    page.query_selector('[data-open]').click(); page.wait_for_timeout(800)
    ok['mica_sin_boton'] = not page.query_selector('#sheet.on [data-comsol]')
    ctx.close(); br.close()
print(json.dumps(ok, ensure_ascii=False, indent=1)); print(json.dumps({'errores': B.REPORT['errores']}, ensure_ascii=False))
