# -*- coding: utf-8 -*-
"""Flujo semanal 08/11: intaker Sin contactar -> primer mensaje -> Contacté -> fase.
Uso: python3 pruebas/flujo_sc.py <carpeta index.html> <carpeta capturas> antes|despues
Cuenta toques, hojas abiertas, scroll y pedidos al motor que la persona tiene que esperar. DATOS FALSOS."""
import sys
MODO = sys.argv[3] if len(sys.argv) > 3 else 'antes'
sys.argv = sys.argv[:3] + ['Fran']
from explora_base import *

M = {'toques': 0, 'pantallas': 0, 'scroll_px': 0, 'espera_motor': 0, 'pasos': []}
def tap(page, sel, nombre, t=700, pantalla=False):
    e = page.query_selector(sel)
    if not e: M['pasos'].append('NO ESTÁ: ' + nombre); print('NO ESTÁ', nombre, sel); return None
    y0 = page.evaluate('scrollY'); e.scroll_into_view_if_needed(); dy = abs(page.evaluate('scrollY') - y0)
    if dy > 4: M['scroll_px'] += dy; M['pasos'].append('scroll %dpx' % dy)
    n0 = len(API.calls); e.click(); M['toques'] += 1; M['pasos'].append('toque: ' + nombre)
    if pantalla: M['pantallas'] += 1
    page.wait_for_timeout(t)
    nuevas = [c for c in API.calls[n0:] if c not in ('saveVisto',)]
    if nuevas: M['pasos'].append('  motor: ' + ','.join(nuevas))
    return e
def irse_a_whatsapp(page, seg=6):
    # el wa.me se abre en otra pestaña (bloqueada por el banco); la app queda oculta unos segundos
    for p in page.context.pages[1:]:
        try: p.close()
        except Exception: pass
    page.evaluate("""()=>{Object.defineProperty(document,'visibilityState',{value:'hidden',configurable:true});Object.defineProperty(document,'hidden',{value:true,configurable:true});document.dispatchEvent(new Event('visibilitychange'));window.dispatchEvent(new Event('blur'));}""")
    page.clock.run_for(seg * 1000); page.wait_for_timeout(200)
    page.evaluate("""()=>{Object.defineProperty(document,'visibilityState',{value:'visible',configurable:true});Object.defineProperty(document,'hidden',{value:false,configurable:true});document.dispatchEvent(new Event('visibilitychange'));window.dispatchEvent(new Event('focus'));}""")
    page.wait_for_timeout(700)
    M['pasos'].append('(escribe el mensaje en WhatsApp y vuelve)')

with sync_playwright() as pw:
    b = pw.chromium.launch()
    for vp in [{'tag': 'v390', 'vp': {'width': 390, 'height': 844}}, {'tag': 'c360', 'vp': {'width': 360, 'height': 640}}]:
        M.update({'toques': 0, 'pantallas': 0, 'scroll_px': 0, 'pasos': []})
        page, ctx, shot, API = explora(b, 'Fran', vp, MODO + '_' + vp['tag'], OUT)
        globals()['API'] = API
        tap(page, '#nav button[data-view="tareas"]', 'Tareas'); page.evaluate('scrollTo(0,0)'); shot('tareas')
        L1, L2 = 'P071', 'P072'
        # Lead 1: le escribe y contesta enseguida -> queda clasificado (A)
        # Lead 2: le escribe, no contesta; más tarde contesta -> fase B
        if MODO == 'antes':
            tap(page, '#main .cl.sc a.wa[href*="2615550171"]', 'WhatsApp (Brenda)'); irse_a_whatsapp(page); shot('volvio_wsp')
            tap(page, '#main [data-ficha="%s"]' % L1, 'abre la ficha (Brenda)', pantalla=True); shot('ficha')
            tap(page, '#sheet.on [data-fimodo="fase"]', 'Cambiar fase'); shot('ficha_fases')
            tap(page, '#sheet.on [data-fase="A"]', 'A'); shot('ficha_A')
            tap(page, '#sheet.on [data-close]', 'cerrar la ficha')
            tap(page, '#main .cl.sc a.wa[href*="2615550172"]', 'WhatsApp (Gustavo)'); irse_a_whatsapp(page)
            tap(page, '#main [data-levante="%s"]' % L2, '✓ Contacté (Gustavo)', t=1200); shot('contacte')
            M['pasos'].append('— más tarde Gustavo contesta: ya no está en Tareas, hay que buscarlo en Agendar —')
            tap(page, '#nav button[data-view="agendar"]', 'Agendar'); page.evaluate('scrollTo(0,0)')
            tap(page, '#main [data-agfase="sin"]', 'chip Sin clasificar'); shot('agendar_sin')
            tap(page, '#main [data-ficha="%s"]' % L2, 'abre la ficha (Gustavo)', pantalla=True)
            tap(page, '#sheet.on [data-fimodo="fase"]', 'Cambiar fase')
            tap(page, '#sheet.on [data-fase="B"]', 'B')
            tap(page, '#sheet.on [data-close]', 'cerrar la ficha'); shot('fin')
        else:
            tap(page, '#main [data-scir]', 'Ver › (barra de arriba)'); shot('ir_sin_contactar')
            tap(page, '#main .cl.sc a.wa[href*="2615550171"]', 'WhatsApp (Brenda)'); irse_a_whatsapp(page); shot('volvio_wsp')
            tap(page, '#main [data-scid="%s"][data-scfase="A"]' % L1, 'A (Brenda, en la lista)'); shot('brenda_A')
            tap(page, '#main .cl.sc a.wa[href*="2615550172"]', 'WhatsApp (Gustavo)'); irse_a_whatsapp(page); shot('gustavo_volvio')
            page.clock.run_for(9000); page.wait_for_timeout(900)
            M['pasos'].append('— más tarde Gustavo contesta: sigue en Tareas, en "Falta la fase" —')
            page.evaluate('scrollTo(0,0)')
            tap(page, '#nav button[data-view="tareas"]', 'Tareas')
            tap(page, '#main [data-scir]', 'Ver › (barra de arriba)'); shot('falta_fase')
            tap(page, '#main [data-scid="%s"][data-scfase="B"]' % L2, 'B (Gustavo, en la lista)'); shot('fin')
        page.clock.run_for(12000); page.wait_for_timeout(800)
        print('==', MODO, vp['tag'], 'toques', M['toques'], 'hojas', M['pantallas'], 'scroll', M['scroll_px'])
        for p in M['pasos']: print('   ', p)
        f = {l['id']: (l['fase'], l.get('intaker')) for l in API.leads + API.pa + API.sc}
        print('   estado motor falso:', f.get(L1), f.get(L2), '| llamadas:', [c for c in API.calls if c not in ('saveVisto',)][-8:])
        ctx.close()
    b.close()
print('ERRORES', REPORT['errores'])
