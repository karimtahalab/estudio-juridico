# -*- coding: utf-8 -*-
"""Flujo semanal 22/11: confirmaciones del día y mensaje previo (intakers). DATOS FALSOS; todo lo externo bloqueado
(script.google.com, googleusercontent.com, docs.google.com, graph.facebook.com, uChat y cualquier otro dominio).
Uso: python3 pruebas/flujo_conf.py <carpeta index.html> <salida> [Fran] [390|360]
Mide: toques para mandar los recordatorios de hoy y de mañana (oficial ART/Laboral y 💬 Tránsito) y cargar lo que respondieron;
scroll hasta la primera fila; pedidos al motor; si se puede deshacer."""
import sys, os, json
WHO = sys.argv[3] if len(sys.argv) > 3 else 'Fran'
W = int(sys.argv[4]) if len(sys.argv) > 4 else 390
sys.argv = sys.argv[:3]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import explora_base as B
from playwright.sync_api import sync_playwright
OUT = B.OUT
vp = {'vp': {'width': W, 'height': 844 if W == 390 else 640}, 'dsf': 2}
res = {'toques': [], 'scroll_px': 0}
def toque(q): res['toques'].append(q)
with sync_playwright() as pw:
    br = pw.chromium.launch()
    page, ctx, shot, api = B.explora(br, WHO, vp, 'cf%d' % W, OUT)
    ctx.on('page', lambda p: p.close())  # 💬 abre wa.me en otra pestaña: se cierra (y está bloqueado)
    page.wait_for_timeout(1500)
    n0 = len(api.calls)
    page.click('#nav button[data-view="tareas"]'); toque('Tareas'); page.wait_for_timeout(900)
    page.evaluate("window.scrollTo(0,0)"); shot('tareas_arriba')
    nuevo = page.locator('[data-cfir]').count() > 0
    res['version'] = 'nueva' if nuevo else 'main'
    # dónde queda la primera fila de recordatorios
    y = page.evaluate("()=>{const e=document.querySelector('li.tk'); return e? Math.round(e.getBoundingClientRect().top):null}")
    res['primera_fila_y'] = y; res['alto_pantalla'] = vp['vp']['height']
    if nuevo:
        res['barra'] = page.locator('.cf-bar').first.inner_text().replace('\n', ' ')
        b = page.locator('[data-cftodos="todo"]').first
        b.click(); toque('📤 Mandar todos'); page.wait_for_timeout(700); shot('lote_vista')
        res['lote_lista'] = page.evaluate("()=>[...document.querySelectorAll('#wspDlg .cf-it')].map(e=>e.innerText.replace(/\\s+/g,' ').slice(0,70))")
        page.locator('#wspDlg [data-cflote]').click(); toque('Enviar (lote)'); page.wait_for_timeout(500)
        shot('lote_mandando'); page.wait_for_timeout(2500)
        page.evaluate("window.scrollTo(0,0)"); shot('lote_enviado')
        res['barra_despues'] = page.locator('.cf-bar').first.inner_text().replace('\n', ' ')
        res['dudas'] = page.evaluate("()=>[...document.querySelectorAll('li.tk')].map(li=>({n:(li.querySelector('.nm')||{}).textContent, boton_gris:!!li.querySelector('.cf-ya'), marca:(li.querySelector('.wsp-ya')||{}).textContent||''}))")
    else:
        page.evaluate("()=>{const e=[...document.querySelectorAll('h2.sec-t')].find(h=>/Mensaje del día/.test(h.textContent)); if(e) e.scrollIntoView()}")
        res['scroll_px'] += page.evaluate("window.scrollY"); shot('seccion')
        ids = page.evaluate("()=>[...document.querySelectorAll('li.tk [data-wsp]')].map(b=>b.getAttribute('data-wsp'))")
        for k, i in enumerate(ids):
            b = page.locator('li.tk [data-wsp="%s"]' % i).first
            b.scroll_into_view_if_needed(); b.click(); toque('📤'); page.wait_for_timeout(500)
            if k == 0: shot('vista_previa')
            page.locator('#wspDlg [data-wspok]').click(); toque('Enviar'); page.wait_for_timeout(1200)
        res['dudas'] = page.evaluate("()=>[...document.querySelectorAll('li.tk')].map(li=>({n:(li.querySelector('.nm')||{}).textContent, boton_sigue:!!li.querySelector('[data-wsp]:not([disabled])'), marca:(li.querySelector('.wsp-ya')||{}).textContent||''}))")
        shot('enviados')
    # Tránsito: 💬 (sin oficial)
    tr = page.evaluate("()=>[...document.querySelectorAll('li.tk')].filter(li=>!li.querySelector('[data-wsp],.wsp-va') && li.querySelector('a.wa')).length")
    for i in range(tr):
        toque('💬 Tránsito')
    res['transito'] = tr
    # Después llegan las respuestas: Confirmó en todas
    page.evaluate("window.scrollTo(0,0)")
    guard = 0; sc0 = None
    while guard < 15:
        guard += 1
        c = page.locator('li.tk .cbtn.ok:not(.on)')
        if not c.count(): break
        if sc0 is None:
            c.first.scroll_into_view_if_needed(); sc0 = page.evaluate("window.scrollY")
        c.first.click(); toque('✅ Confirmó'); page.wait_for_timeout(700)
        if guard == 1: shot('confirmo')
    res['scroll_confirmar_px'] = sc0
    page.wait_for_timeout(1500); shot('al_dia')
    res['enviados'] = [(e['id'], e['tpl']) for e in api.wsp_enviados]
    res['pedidos'] = [c for c in api.calls[n0:] if c not in ('getData', 'getReporte', 'reporteTurno', 'wspDatos', 'logUso', 'getEstudios', 'saveVisto')]
    res['n_toques'] = len(res['toques'])
    res['errores'] = B.REPORT['errores']
    br.close()
print(json.dumps(res, ensure_ascii=False, indent=1))
