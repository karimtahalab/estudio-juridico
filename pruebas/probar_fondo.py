# -*- coding: utf-8 -*-
"""Cuenta los pedidos de FONDO (los que la persona no espera) con DATOS FALSOS.
Uso: python3 pruebas/probar_fondo.py <carpeta con index.html> <carpeta capturas>
A) Pri (intaker): entra, clasifica 4 leads en "Falta la fase" (cambiarFase) con 40 s entre cada uno,
   toca Actualizar y abre 3 fichas. Cuenta getReporte, saveVisto y getData.
B) Pri abre la pestaña Reporte después de todo eso: tiene que verse el reporte (aunque sea el guardado) y pedir uno nuevo.
C) Karim (admin con finanzas): abre la app 4 veces seguidas en 10 minutos (mismo celular). Cuenta fin2Calentar.
"""
import sys, os, json, collections
sys.argv = [sys.argv[0], sys.argv[1] if len(sys.argv) > 1 else '.', sys.argv[2] if len(sys.argv) > 2 else 'pruebas/capturas_fondo', 'Pri']
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import explora_base as B
from playwright.sync_api import sync_playwright

OUT = B.OUT; os.makedirs(OUT, exist_ok=True)
VP = {'vp': {'width': 390, 'height': 844}}
res = {}

def contar(api):
    c = collections.Counter(); orig = api.handle
    def h(fn, arg):
        c[fn] += 1
        if fn == 'fin2Calentar': return True, {'ok': True}
        return orig(fn, arg)
    api.handle = h
    return c

with sync_playwright() as pw:
    br = pw.chromium.launch()
    # A y B
    page, ctx, shot, api = B.explora(br, 'Pri', VP, 'fondo', OUT)
    import datos_falsos as DF
    for k in range(4):
        l = DF._lead(81 + k, "Lead Falta Fase %d (prueba)" % (k + 1), "26155501%02d" % (81 + k), ["ART", "LABORAL"][k % 2], "", "", "", fase="", ingreso=DF.D(0))
        l["intaker"] = "Pri"; api.pa.insert(0, l)
    page.click('#btnRefresh'); page.clock.run_for(5000); page.wait_for_timeout(800)
    c = contar(api)
    page.clock.run_for(5000); page.wait_for_timeout(500)
    base = dict(c)
    hechos = 0
    for i in range(4):
        b = page.query_selector('button[data-scfase="A"], button[data-scfase="B"]')
        if not b:
            page.click('nav button[data-view="tareas"]'); page.wait_for_timeout(400)
            b = page.query_selector('button[data-scfase="A"], button[data-scfase="B"]')
        if b:
            b.scroll_into_view_if_needed(); b.click(); hechos += 1
        page.clock.run_for(40000); page.wait_for_timeout(600)
    page.click('#btnRefresh'); page.clock.run_for(5000); page.wait_for_timeout(600)
    for i in range(3):
        o = page.query_selector_all('[data-open]')
        if len(o) > i:
            o[i].scroll_into_view_if_needed(); o[i].click(); page.clock.run_for(2500); page.wait_for_timeout(300)
            page.keyboard.press('Escape'); page.evaluate("()=>{const x=document.querySelector('#sheet.on [data-close], #sheet.on .close'); if(x) x.click();}"); page.wait_for_timeout(300)
    page.clock.run_for(5000); page.wait_for_timeout(500)
    res['A_pri'] = {'clasificados': hechos, 'getReporte': c['getReporte'], 'saveVisto': c['saveVisto'], 'getData': c['getData'], 'cambiarFase': c['cambiarFase'], 'al_entrar': base}
    antes = c['getReporte']
    page.click('nav button[data-view="reporte"]'); page.wait_for_timeout(300)
    t = page.inner_text('main') if page.query_selector('main') else page.inner_text('body')
    res['B_reporte_al_tocar'] = {'muestra_algo': ('Armando el reporte' not in t) or c['getReporte'] > antes, 'pidio_nuevo': c['getReporte'] - antes}
    page.clock.run_for(3000); page.wait_for_timeout(600); shot('reporte')
    t = page.inner_text('body')
    res['B_reporte_al_tocar']['listo_a_los_3s'] = 'Armando el reporte' not in t
    # D) una consulta con novedad (cambió el resumen): al abrirla tiene que guardar el visto (1 saveVisto)
    page.click('nav button[data-view="agenda"]'); page.wait_for_timeout(400)
    o = page.query_selector('[data-open]'); lid = o.get_attribute('data-open') if o else None
    l = api._find(lid) if lid else None
    if l:
        l["resumen"] = "Resumen nuevo (prueba) " + "x" * 20
        page.click('#btnRefresh'); page.clock.run_for(5000); page.wait_for_timeout(800)
        sv0 = c['saveVisto']
        page.query_selector('[data-open="%s"]' % lid).click(); page.clock.run_for(3000); page.wait_for_timeout(500)
        res['D_novedad_guarda_visto'] = c['saveVisto'] - sv0
    ctx.close()
    # C
    page, ctx, shot, api = B.explora(br, 'Karim', VP, 'fondo', OUT)
    c = contar(api)
    page.clock.run_for(5000); page.wait_for_timeout(500)
    for i in range(3):
        page.clock.run_for(150000)
        page.reload(); page.wait_for_timeout(1500); page.clock.run_for(5000); page.wait_for_timeout(500)
    res['C_karim_4_aperturas'] = {'fin2Calentar': c['fin2Calentar'], 'getData': c['getData']}
    ctx.close(); br.close()

print(json.dumps(res, ensure_ascii=False, indent=1))
print(json.dumps({'errores': B.REPORT['errores']}, ensure_ascii=False))
