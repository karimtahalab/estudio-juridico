# -*- coding: utf-8 -*-
"""Noche 13->14/11 (DATOS FALSOS). Mide:
 A) título de cada pestaña: ¿se corta una palabra a la mitad? (Seguimiento en 360/390)
 B) agenda: a qué altura arranca la primera consulta (Karim con "Todas", Mica, Juan)
 C) abrir el mismo estudio/archivo dos veces: cuántos verEstudio salen al motor
Uso: python3 pruebas/probar_2026_11_14.py <carpeta index.html> <salida> Pri,Karim,Mica,Juan"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from explora_base import *

TIT = r"""()=>{const h=document.querySelector('#ttl h1'); if(!h) return null; const r=h.getBoundingClientRect();
  const rg=document.createRange(); rg.selectNodeContents(h); const lineas=new Set([...rg.getClientRects()].map(x=>Math.round(x.top))).size;
  const palabras=h.textContent.trim().split(/\s+/).length;
  return {texto:h.textContent, fs:getComputedStyle(h).fontSize, lineas:lineas, palabras:palabras, corta: lineas>palabras, alto:Math.round(r.height)}}"""
AG = r"""()=>{const c=document.querySelector('#main [data-open], #main .next, #main .cs'); const d=document.querySelector('.de-adm, .de-mia');
  const R=e=>e?[Math.round(e.getBoundingClientRect().top),Math.round(e.getBoundingClientRect().bottom)]:null;
  return {primera_consulta:R(c), disp:R(d), alto:innerHeight}}"""
out = {}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for vp in [{'tag': 'cel390', 'vp': {'width': 390, 'height': 844}}, {'tag': 'cel360', 'vp': {'width': 360, 'height': 640}}]:
        for who in ROLES:
            page, ctx, shot, api = explora(b, who, vp, vp['tag'], OUT)
            pedidos = []
            page.on('request', lambda r: r.method == 'POST' and pedidos.append((json.loads(r.post_data or '{}') or {}).get('fn')))
            views = page.eval_on_selector_all('#nav button[data-view]', 'bs=>bs.filter(b=>!b.hidden).map(b=>b.dataset.view)')
            k = '%s/%s' % (vp['tag'], who)
            out[k] = {'titulos': {}}
            for v in views:
                page.click('#nav button[data-view="%s"]' % v); page.wait_for_timeout(500)
                out[k]['titulos'][v] = page.evaluate(TIT)
                if v == 'seguimiento': shot('seguimiento')
                if v == 'agenda':
                    out[k]['agenda'] = page.evaluate(AG); shot('agenda')
            # C) estudio: abrir la ficha de una consulta de ART/Laboral y tocar el mismo archivo dos veces
            if 'agenda' in views:
                page.click('#nav button[data-view="agenda"]'); page.wait_for_timeout(400)
                op = page.query_selector('#main [data-open]')
                if op:
                    op.click(); page.wait_for_timeout(1200)
                    ev = page.query_selector('#sheet [data-estver]')
                    if ev:
                        n0 = pedidos.count('verEstudio')
                        ev.click(); page.wait_for_timeout(900)
                        visor1 = bool(page.query_selector('#estVisor'))
                        if visor1: page.click('#estVisor [data-estcerrar]'); page.wait_for_timeout(300)
                        page.query_selector('#sheet [data-estver]').click(); page.wait_for_timeout(900)
                        visor2 = bool(page.query_selector('#estVisor'))
                        out[k]['estudio'] = {'verEstudio_al_motor': pedidos.count('verEstudio') - n0, 'visor1': visor1, 'visor2': visor2}
                        if visor2: shot('estudio_2da_vez'); page.click('#estVisor [data-estcerrar]')
            ctx.close()
    b.close()
srv.shutdown()
print(json.dumps({'medidas': out, 'errores': REPORT['errores']}, ensure_ascii=False, indent=1))
