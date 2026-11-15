# -*- coding: utf-8 -*-
"""Banco (DATOS FALSOS): flujo semanal del 15/11 — intaker agenda un lead desde Agendar.
Escenarios (Pri):
  1) "Lo antes posible": Oscar (ART, fase A) en el primer horario libre que haya.
  2) "El lunes a las 10": Nicolás (Laboral, fase B) el lunes 09/11 a las 10:00 con quien esté libre.
  3) Tránsito: Silvina (fase A) con Juan, en el primer horario libre de Juan (agenda rayada).
Cuenta toques, scroll dentro de la hoja, pedidos al motor y si puede deshacer.
Bloquea script.google.com, googleusercontent.com, docs.google.com, graph.facebook.com y uChat: todo se responde con datos falsos.
Uso: python3 pruebas/flujo_agendar.py <carpeta con index.html> <carpeta de capturas> <etiqueta> [ancho] [alto]"""
import sys, os, json, time
TAG = sys.argv[3] if len(sys.argv) > 3 else 'x'
W = int(sys.argv[4]) if len(sys.argv) > 4 else 390
H = int(sys.argv[5]) if len(sys.argv) > 5 else 844
sys.argv = [sys.argv[0], sys.argv[1], sys.argv[2], 'Pri']
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import explora_base as B
from playwright.sync_api import sync_playwright

DEMORA = 0.3
res = {'tag': TAG, 'vp': '%dx%d' % (W, H), 'esc': {}}
with sync_playwright() as pw:
    br = pw.chromium.launch(); api = B.FakeApi(); pedidos, errs = [], []
    # Juan marcó disponible solo lunes y miércoles de 14 a 18 (el resto de su agenda sale rayado)
    api.disp = {"modos": {"Juan": "disponibilidad"}, "fijo": {"Juan": {"1": "14:00-18:00", "3": "14:00-18:00"}}, "fechas": {}}
    ctx = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=2, is_mobile=True, has_touch=True, locale='es-AR', timezone_id='America/Argentina/Buenos_Aires', service_workers='block')
    pg = ctx.new_page(); pg.clock.install(time='2026-11-05T11:20:00-03:00')
    pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    def route(r):
        u = r.request.url
        if B.GOOGLE.search(u):
            b = json.loads(r.request.post_data or '{}'); pedidos.append(b.get('fn'))
            if b.get('fn') in ('agendar',): time.sleep(DEMORA)
            ok, d = api.handle(b.get('fn'), b.get('arg')); r.fulfill(status=200, content_type='application/json', body=json.dumps({'ok': ok, 'data': d} if ok else {'ok': False, 'error': d}))
        elif u.startswith('http://127.0.0.1:%d/' % B.PORT): r.continue_()
        else: r.abort()  # graph.facebook.com, uChat, Google Fonts y todo lo externo: bloqueado
    pg.route('**/*', route)
    k = [0]
    def shot(n):
        k[0] += 1; pg.wait_for_timeout(250); pg.screenshot(path=os.path.join(B.OUT, '%s_%dx%d_%02d_%s.png' % (TAG, W, H, k[0], n)))
    pg.goto(B.BASE); pg.wait_for_timeout(1000); pg.click('button[data-yo="Pri"]'); pg.wait_for_timeout(300)
    pg.fill('#pin', '1234'); pg.wait_for_timeout(700)
    if pg.query_selector('#sheet.on #pin'): pg.fill('#pin', '1234'); pg.wait_for_timeout(700)
    pg.wait_for_timeout(1200)
    js_scroll = "() => { const s=document.querySelector('#sheet.on .sh-body')||document.querySelector('#sheet.on'); return s? s.scrollTop:0 }"

    def visible_en_hoja(sel):
        return pg.evaluate("""(sel) => { const e=document.querySelector(sel); if(!e) return null; const r=e.getBoundingClientRect(); return {top:Math.round(r.top), bottom:Math.round(r.bottom), vis: r.top>=0 && r.bottom<=innerHeight}; }""", sel)

    def tocar(loc, cuenta):
        loc.scroll_into_view_if_needed(); loc.click(); cuenta[0] += 1; pg.wait_for_timeout(350)

    def scroll_hoja():
        return pg.evaluate("""() => { let m=0; document.querySelectorAll('#sheet.on, #sheet.on *').forEach(e=>{ if(e.scrollTop>m) m=e.scrollTop; }); return m; }""")

    def escenario(nombre, quien_busca, elegir, cap):
        nonlocal_t = [0]; p0 = len(pedidos)
        pg.click('#nav button[data-view="agendar"]'); nonlocal_t[0] += 1; pg.wait_for_timeout(900)
        pg.fill('#aq', ''); pg.click('#aq'); nonlocal_t[0] += 1; pg.keyboard.type(quien_busca); pg.wait_for_timeout(600)
        if cap: shot(nombre + '_lista')
        fila = pg.locator('li.pa', has_text=quien_busca).first
        b = fila.locator('[data-agendar], [data-agahora]').first
        tocar(b, nonlocal_t)
        if cap: shot(nombre + '_hoja')
        info = elegir(nonlocal_t, cap)
        pg.wait_for_timeout(600)
        # Para seguir con el próximo lead hay que volver a la lista: si quedó una hoja abierta (la ficha), se cierra (1 toque más)
        abierta = bool(pg.query_selector('#sheet.on'))
        if abierta: pg.click('#sheet.on [data-close]'); nonlocal_t[0] += 1; pg.wait_for_timeout(300)
        info['hoja_abierta_despues'] = abierta
        pg.clock.run_for(15000); pg.wait_for_timeout(800)
        res['esc'][nombre] = dict(info, toques=nonlocal_t[0], toques_desde_la_lista=nonlocal_t[0]-2, pedidos=pedidos[p0:], errores=list(errs))

    def guardar(t, cap, nombre):
        if not pg.query_selector('#sheet.on [data-saveag]'):  # agendó al tocar el horario
            pg.wait_for_timeout(200); toast = (pg.text_content('#toast') or '').strip()
            if cap: shot(nombre + '_guardado')
            return {'al_instante': True, 'toast': toast, 'deshacer': bool(pg.query_selector('#toast.on [data-undo]')) and 'Deshacer' in toast}
        btn = pg.locator('#sheet.on [data-saveag]')
        pos = visible_en_hoja('#sheet.on [data-saveag]')
        tocar(btn, t)
        pg.wait_for_timeout(200)
        toast = (pg.text_content('#toast') or '').strip()
        if cap: shot(nombre + '_guardado')
        return {'boton_guardar_visible_sin_scroll': bool(pos and pos['vis']), 'toast': toast,
                'deshacer': bool(pg.query_selector('#toast.on [data-undo]')) and 'Deshacer' in toast}

    # 1) Lo antes posible: recorre días hasta encontrar el primer horario libre de alguien
    def primero(t, cap, nombre='1_antes_posible'):
        out = {}
        rapido = pg.query_selector('#sheet.on [data-agprox]')
        if rapido:
            tocar(pg.locator('#sheet.on [data-agprox]').first, t); out['via'] = 'próximos libres'
        else:
            # En la hoja vieja se abre en "Mañana": para lo antes posible hay que tocar "Hoy" y buscar el horario más temprano
            tocar(pg.locator('#sheet.on [data-agdia="2026-11-05"]'), t)
            slot = pg.locator('#sheet.on [data-slot]').first
            out['scroll_hasta_slot'] = pg.evaluate("(e)=>Math.max(0,Math.round(e.getBoundingClientRect().top-innerHeight+60))", slot.element_handle())
            tocar(slot, t); out['via'] = 'grilla del día'
        out['elegido'] = pg.evaluate("()=>{const e=document.querySelector('#sheet.on [data-saveag]'); return e? e.textContent.trim():(document.getElementById('toast').textContent||'').trim()}")
        if cap and pg.query_selector('#sheet.on'): shot(nombre + '_elegido')
        out.update(guardar(t, cap, nombre)); return out
    escenario('1_antes_posible', 'Oscar', primero, True)

    # 2) El lunes a las 10 con quien esté libre
    def lunes10(t, cap, nombre='2_lunes_10'):
        out = {}
        dia = pg.locator('#sheet.on [data-agdia="2026-11-09"]')
        tocar(dia, t)
        slot = pg.locator('#sheet.on [data-slot$="|10:00"]').first
        out['scroll_hasta_slot'] = pg.evaluate("(e)=>Math.max(0,Math.round(e.getBoundingClientRect().top-innerHeight+60))", slot.element_handle())
        tocar(slot, t)
        out['elegido'] = pg.evaluate("()=>{const e=document.querySelector('#sheet.on [data-saveag]'); return e? e.textContent.trim():(document.getElementById('toast').textContent||'').trim()}")
        if cap and pg.query_selector('#sheet.on'): shot(nombre + '_elegido')
        out.update(guardar(t, cap, nombre)); return out
    escenario('2_lunes_10', 'Nicolás', lunes10, True)

    # 3) Tránsito con Juan: primer horario libre de Juan
    def juan(t, cap, nombre='3_juan'):
        out = {}
        rapido = pg.query_selector('#sheet.on [data-agprox]')
        if rapido:
            tocar(pg.locator('#sheet.on [data-agprox]').first, t); out['via'] = 'próximos libres'
        else:
            out['dias_probados'] = 1
            slot = pg.locator('#sheet.on [data-slot^="Juan|"]').first
            if not slot.count():
                # día por defecto sin horarios: ir probando días
                for d in pg.locator('#sheet.on [data-agdia]').all()[1:]:
                    tocar(d, t); out['dias_probados'] += 1
                    if pg.locator('#sheet.on [data-slot^="Juan|"]').count(): break
                slot = pg.locator('#sheet.on [data-slot^="Juan|"]').first
            out['scroll_hasta_slot'] = pg.evaluate("(e)=>Math.max(0,Math.round(e.getBoundingClientRect().top-innerHeight+60))", slot.element_handle())
            tocar(slot, t); out['via'] = 'grilla del día'
        out['elegido'] = pg.evaluate("()=>{const e=document.querySelector('#sheet.on [data-saveag]'); return e? e.textContent.trim():(document.getElementById('toast').textContent||'').trim()}")
        if cap and pg.query_selector('#sheet.on'): shot(nombre + '_elegido')
        out.update(guardar(t, cap, nombre)); return out
    escenario('3_juan', 'Silvina', juan, True)

    # 4) Deshacer: agendar a Patricia y arrepentirse
    def deshacer(t, cap, nombre='4_deshacer'):
        out = {}
        rapido = pg.query_selector('#sheet.on [data-agprox]')
        loc = pg.locator('#sheet.on [data-agprox]').first if rapido else pg.locator('#sheet.on [data-slot]').first
        n0 = pedidos.count('agendar')
        tocar(loc, t); out.update(guardar(t, False, nombre))
        b = pg.query_selector('#toast.on [data-undo]')
        if b and 'Deshacer' in (pg.text_content('#toast') or ''):
            b.click(); t[0] += 1; pg.wait_for_timeout(500)
            out['tras_deshacer'] = (pg.text_content('#toast') or '').strip()
            out['vuelve_a_la_lista'] = pg.locator('li.pa', has_text='Ramiro').count() > 0
            if cap: shot(nombre + '_deshecho')
            pg.clock.run_for(10000); pg.wait_for_timeout(500)
            out['agendar_mandados_tras_deshacer'] = pedidos.count('agendar') - n0
        return out
    escenario('4_deshacer', 'Ramiro', deshacer, True)
    res['agendar_al_motor'] = [x for x in pedidos if x == 'agendar']
    res['en_planilla_falsa'] = {l['nombre'].split()[0]: (l['fecha'], l['hora'], l['abogada'], l['fase']) for l in api.leads + api.pa if l['nombre'].split()[0] in ('Oscar', 'Nicolás', 'Silvina', 'Ramiro')}
    res['errores_js'] = errs
    br.close()
B.srv.shutdown()
print(json.dumps(res, ensure_ascii=False, indent=1))
