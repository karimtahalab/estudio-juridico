# -*- coding: utf-8 -*-
"""Casos borde del flujo nuevo de Sin contactar (DATOS FALSOS). Uso: python3 pruebas/probar_sin_contactar.py <carpeta index.html> <capturas>"""
import sys
sys.argv = sys.argv[:3] + ['Fran']
from explora_base import *
from flujo_sc_util import afuera
OK = []
def chk(n, c): OK.append((n, bool(c))); print(('OK  ' if c else 'MAL ') + n)
vp = {'tag': 'c360', 'vp': {'width': 360, 'height': 640}}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    page, ctx, shot, api = explora(b, 'Fran', vp, 'borde', OUT)
    page.click('#nav button[data-view="tareas"]'); page.wait_for_timeout(600)
    n = lambda f: api.calls.count(f)
    # 1) vuelve enseguida (2 s): no marca
    page.click('#main .cl.sc a.wa[href*="2615550175"]'); afuera(page, 2)
    chk('vuelve a los 2 s: no marca', page.query_selector('#main [data-levante="P075"]') and n('levantarLead') == 0)
    # 2) WhatsApp y vuelve a los 6 s, Deshacer: vuelve a Sin contactar y no se manda nada
    page.click('#main .cl.sc a.wa[href*="2615550175"]'); afuera(page, 6)
    chk('al volver: sale de Sin contactar', not page.query_selector('#main [data-levante="P075"]'))
    chk('al volver: aparece en Falta la fase', page.query_selector('#main [data-scid="P075"][data-scfase="A"]'))
    page.click('#toast [data-undo]'); page.wait_for_timeout(400); page.clock.run_for(12000); page.wait_for_timeout(600)
    chk('Deshacer: vuelve a Sin contactar', page.query_selector('#main [data-levante="P075"]'))
    chk('Deshacer: no llamó a levantarLead', n('levantarLead') == 0)
    # 3) ✓ Contacté: sale a los 10 s
    page.click('#main [data-levante="P074"]'); page.wait_for_timeout(500)
    chk('✓: todavía no mandó', n('levantarLead') == 0)
    page.clock.run_for(10500); page.wait_for_timeout(900)
    chk('✓: a los 10 s mandó una vez', n('levantarLead') == 1)
    chk('✓: Hernán con nombre de Fran en el motor falso', api._find('P074').get('intaker') == 'Fran')
    chk('✓: Hernán en Falta la fase', page.query_selector('#main [data-scid="P074"][data-scfase="B"]'))
    # 4) ✓ y sale de la app enseguida: se manda al salir
    page.click('#main [data-levante="P073"]'); page.wait_for_timeout(300)
    page.evaluate("""()=>{Object.defineProperty(document,'visibilityState',{value:'hidden',configurable:true});Object.defineProperty(document,'hidden',{value:true,configurable:true});document.dispatchEvent(new Event('visibilitychange'));}""")
    page.wait_for_timeout(700)
    chk('✓ y sale: mandó al salir', n('levantarLead') == 2)
    page.evaluate("""()=>{Object.defineProperty(document,'visibilityState',{value:'visible',configurable:true});Object.defineProperty(document,'hidden',{value:false,configurable:true});document.dispatchEvent(new Event('visibilitychange'));}""")
    page.wait_for_timeout(900)
    # 5) Fase desde la lista + Deshacer
    page.click('#main [data-scid="P074"][data-scfase="C"]'); page.wait_for_timeout(900)
    chk('C: motor falso en C', api._find('P074')['fase'] == 'C')
    chk('C: muestra "Quedó en"', 'Quedó en' in (page.inner_text('#main') or ''))
    page.click('#toast [data-undo]'); page.wait_for_timeout(1200)
    chk('Deshacer fase: vuelve sin fase', api._find('P074')['fase'] == '' and page.query_selector('#main [data-scid="P074"][data-scfase="A"]'))
    # 6) Otra: abre la ficha con las fases abiertas
    page.click('#main [data-scid="P074"][data-scfase=""]'); page.wait_for_timeout(700)
    chk('Otra: ficha con fases', page.query_selector('#sheet.on [data-fase="BC"]')); shot('otra')
    page.click('#sheet.on [data-close]'); page.wait_for_timeout(400)
    # 7) error del motor en levantarLead: vuelve a Sin contactar con aviso
    orig = api.handle
    def falla(fn, arg):
        if fn == 'levantarLead': return False, 'La planilla está ocupada, probá de nuevo en unos segundos.'
        return orig(fn, arg)
    api.handle = falla
    page.click('#main [data-levante="P075"]'); page.clock.run_for(10500); page.wait_for_timeout(900)
    chk('error: vuelve a Sin contactar', page.query_selector('#main [data-levante="P075"]'))
    chk('error: avisa', 'ocupada' in page.inner_text('#toast'))
    api.handle = orig
    ctx.close()
    # 8) Karim (admin): sin barra nueva ni Falta la fase
    page, ctx, shot, api = explora(b, 'Karim', vp, 'borde', OUT)
    if page.query_selector('#nav button[data-view="tareas"]'):
        page.click('#nav button[data-view="tareas"]'); page.wait_for_timeout(600)
    chk('Karim: sin Falta la fase ni barra', not page.query_selector('#ffSec') and not page.query_selector('[data-scir]'))
    ctx.close(); b.close()
print('RESULTADO %d/%d' % (sum(1 for _, c in OK if c), len(OK)))
print('ERRORES', [e for e in REPORT['errores'] if 'update' not in e])
