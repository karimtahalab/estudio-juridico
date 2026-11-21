# -*- coding: utf-8 -*-
"""📤 en la tarjeta de la consulta con resultado (main 20/11, 4a25463). DATOS FALSOS; todo lo externo bloqueado.
Uso: python3 pruebas/probar_wsp_tarjeta.py <carpeta index.html> <salida> [Fran|Mica|Karim] [390|360]"""
import sys, os, json
sys.argv = sys.argv[:3] + sys.argv[3:]
WHO = sys.argv[3] if len(sys.argv) > 3 else 'Fran'
W = int(sys.argv[4]) if len(sys.argv) > 4 else 390
sys.argv = sys.argv[:3]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import explora_base as B
from playwright.sync_api import sync_playwright
OUT = B.OUT
if os.environ.get('PREVIO') == '1':  # desde el arranque: ayer Pri ya le mandó a Rubén el de "vino y no firmó"
    _i0 = B.FakeApi.__init__
    def _i(self, *a, **k):
        _i0(self, *a, **k); self.wsp_log['P001'] = {'seguimiento_post_consulta': {'t': 1793826300000, 'quien': 'Pri'}}
    B.FakeApi.__init__ = _i
vp = {'vp': {'width': W, 'height': 844 if W == 390 else 640}, 'dsf': 2}
res = {}
with sync_playwright() as pw:
    br = pw.chromium.launch()
    page, ctx, shot, api = B.explora(br, WHO, vp, 'c%d' % W, OUT)
    page.on('console', lambda m: m.type == 'log' and '[harness]' in m.text and print(m.text))
    for i, f in (('P001', 'Seguimiento'), ('P003', 'No show')):
        l = api._find(i); l['fase'] = f
    l = api._find('P003'); l['hora'] = '08:30'
    # Ayer Pri ya le mandó a Rubén el de "vino y no firmó" (como lo trae la hoja de envíos del motor)
    # enviarWsp lento (como en el uso real, 7-19 s): para ver el estado "Mandando…"
    LENTO = float(os.environ.get('LENTO', '0'))
    if LENTO:  # se demora en la página (el banco responde al instante y la respuesta se entrega LENTO s después)
        page.evaluate("(ms)=>{ const f0=window.fetch; window.fetch=function(u,o){ const p=f0.apply(this,arguments); try{ if(o&&o.body&&JSON.parse(o.body).fn==='enviarWsp') return p.then(r=>new Promise(ok=>setTimeout(()=>ok(r),ms))); }catch(e){} return p; }; }", int(LENTO*1000))
    page.click("#btnRefresh"); page.wait_for_timeout(1800)
    page.click('#nav button[data-view="agenda"]'); page.wait_for_timeout(800)
    shot('agenda')
    for nom in ('Rubén Prueba', 'Marcos Inventado'):
        c = page.locator('[data-open]', has_text=nom).first
        if not c.count(): res[nom] = 'sin tarjeta'; continue
        c.click(); page.wait_for_timeout(900)
        sh = page.locator('#sheet.on')
        b = sh.locator('[data-wspmenu]')
        info = {'boton': b.count()}
        if b.count():
            bb = b.first.bounding_box(); info['caja'] = [round(bb['y']), round(bb['height'])]
            info['alto_hoja'] = page.evaluate("()=>{const s=document.querySelector('#sheet.on .sh-body')||document.querySelector('#sheet.on'); return [s.scrollHeight, innerHeight]}")
        shot('tarjeta_' + nom.split()[0])
        if b.count():
            b.first.scroll_into_view_if_needed(); b.first.click(); page.wait_for_timeout(1200)
            shot('menu_' + nom.split()[0])
            info['menu'] = page.evaluate("()=>[...document.querySelectorAll('#wspDlg .wsp-op')].map(b=>b.textContent.trim().replace(/\\s+/g,' ').slice(0,60)).slice(0,6)")
            op = page.locator('#wspDlg .wsp-op').first
            if op.count():
                op.click(); page.wait_for_timeout(700); shot('vista_' + nom.split()[0])
                n0 = len(api.calls)
                page.locator('#wspDlg [data-wspok]').click(); page.wait_for_timeout(600)
                if LENTO: shot('mandando_' + nom.split()[0]); info['durante'] = page.evaluate("()=>{const b=document.querySelector('#sheet.on .wsp-menu'); return b? b.innerText:''}")
                page.wait_for_timeout(int(LENTO * 1000) + 1900)
                info['pedidos_envio'] = [c for c in api.calls[n0:]]
                shot('tras_enviar_' + nom.split()[0])
                info['tarjeta_tras'] = page.evaluate("()=>{const s=document.querySelector('#sheet.on'); return s? s.innerText.slice(0,500):'(hoja cerrada)'}")
            if page.locator('#wspDlg.on [data-wspx]').count(): page.locator('#wspDlg.on [data-wspx]').first.click()
            page.evaluate("()=>{const d=document.getElementById('wspDlg'); if(d){d.classList.remove('on'); d.innerHTML='';}}")
        res[nom] = info
        page.keyboard.press('Escape'); page.wait_for_timeout(300)
        (page.locator("#sheet.on [data-close]").first.click() if page.locator("#sheet.on [data-close]").count() else None); page.wait_for_timeout(400)
    res['errores'] = B.REPORT['errores']
    br.close()
print(json.dumps(res, ensure_ascii=False, indent=1))
