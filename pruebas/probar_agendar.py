# -*- coding: utf-8 -*-
"""Banco (DATOS FALSOS): casos borde del agendar al instante (rama mejora/2026-11-15-flujo-agendar).
  a) El motor rechaza (alguien tomó ese horario): vuelve a Por agendar, se reabre la hoja y avisa.
  b) Salir de la app antes de los 6 s: el pedido sale enseguida.
  c) Actualizar (getData) mientras espera: no lo pisa (sigue agendada en la pantalla).
  d) Reagendar a quien ya tiene consulta: sigue con el botón de confirmar (no es al instante).
  e) Tránsito: la hoja de Juan se abre en el primer día que tiene libre.
Bloquea script.google.com, googleusercontent.com, docs.google.com, graph.facebook.com y uChat (todo lo externo).
Uso: python3 pruebas/probar_agendar.py <carpeta con index.html> <carpeta de capturas>"""
import sys, os, json
sys.argv = sys.argv[:3] + ['Pri']
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import explora_base as B
from playwright.sync_api import sync_playwright

res = {}
with sync_playwright() as pw:
    br = pw.chromium.launch(); api = B.FakeApi(); pedidos, errs = [], []
    api.disp = {"modos": {"Juan": "disponibilidad"}, "fijo": {"Juan": {"1": "14:00-18:00", "3": "14:00-18:00"}}, "fechas": {}}
    rechazar = {'id': None}
    ctx = br.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, is_mobile=True, has_touch=True, locale='es-AR', timezone_id='America/Argentina/Buenos_Aires', service_workers='block')
    pg = ctx.new_page(); pg.clock.install(time='2026-11-05T11:20:00-03:00')
    pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    def route(r):
        u = r.request.url
        if B.GOOGLE.search(u):
            b = json.loads(r.request.post_data or '{}'); pedidos.append(b.get('fn'))
            if b.get('fn') == 'agendar' and b['arg'].get('id') == rechazar['id']:
                r.fulfill(status=200, content_type='application/json', body=json.dumps({'ok': False, 'error': 'Ese horario ya lo tomó otra persona (prueba).'})); return
            ok, d = api.handle(b.get('fn'), b.get('arg')); r.fulfill(status=200, content_type='application/json', body=json.dumps({'ok': ok, 'data': d} if ok else {'ok': False, 'error': d}))
        elif u.startswith('http://127.0.0.1:%d/' % B.PORT): r.continue_()
        else: r.abort()
    pg.route('**/*', route)
    pg.goto(B.BASE); pg.wait_for_timeout(1000); pg.click('button[data-yo="Pri"]'); pg.wait_for_timeout(300)
    pg.fill('#pin', '1234'); pg.wait_for_timeout(700)
    if pg.query_selector('#sheet.on #pin'): pg.fill('#pin', '1234'); pg.wait_for_timeout(700)
    pg.wait_for_timeout(1200)
    pg.click('#nav button[data-view="agendar"]'); pg.wait_for_timeout(900)
    def abrir(nombre):
        pg.fill('#aq', nombre); pg.wait_for_timeout(500)
        pg.locator('li.pa', has_text=nombre).first.locator('[data-agendar]').click(); pg.wait_for_timeout(400)
    cuenta = lambda: pedidos.count('agendar')

    # a) rechazo del motor
    rechazar['id'] = 'P052'; abrir('Oscar'); n0 = cuenta()
    pg.locator('#sheet.on [data-agprox]').first.click(); pg.wait_for_timeout(300)
    pg.clock.run_for(7000); pg.wait_for_timeout(800)
    res['a_rechazo'] = {'mandado': cuenta() - n0, 'hoja_reabierta': bool(pg.query_selector('#sheet.on [data-agprox]')),
                        'aviso': (pg.text_content('#toast') or '').strip(), 'sigue_por_agendar': any(l['id'] == 'P052' for l in api.pa)}
    pg.screenshot(path=os.path.join(B.OUT, 'borde_a_rechazo.png'))
    pg.click('#sheet.on [data-close]'); pg.wait_for_timeout(300); rechazar['id'] = None
    res['a_rechazo']['vuelve_a_la_lista'] = pg.locator('li.pa', has_text='Oscar').count() > 0

    # b) salir de la app antes de los 6 s
    abrir('Ramiro'); n0 = cuenta()
    pg.locator('#sheet.on [data-agprox]').first.click(); pg.wait_for_timeout(300)
    pg.evaluate("""()=>{Object.defineProperty(document,'visibilityState',{value:'hidden',configurable:true});document.dispatchEvent(new Event('visibilitychange'));}""")
    pg.wait_for_timeout(600)
    res['b_salir_manda_enseguida'] = cuenta() - n0
    pg.evaluate("""()=>{Object.defineProperty(document,'visibilityState',{value:'visible',configurable:true});document.dispatchEvent(new Event('visibilitychange'));}""")
    pg.wait_for_timeout(800)

    # c) actualizar mientras espera
    abrir('Nicolás'); n0 = cuenta()
    pg.locator('#sheet.on [data-agprox]').first.click(); pg.wait_for_timeout(300)
    pg.click('#btnRefresh'); pg.wait_for_timeout(1200)
    res['c_actualizar'] = {'sigue_agendada_en_pantalla': pg.locator('li.pa', has_text='Nicolás').locator('.pa-has, :text("Ya tiene consulta")').count() > 0 or pg.locator('li.pa', has_text='Nicolás').count() == 0,
                           'mandado_antes_de_6s': cuenta() - n0}
    pg.clock.run_for(7000); pg.wait_for_timeout(1500)
    res['c_actualizar']['mandado_despues'] = cuenta() - n0
    res['c_actualizar']['en_planilla_falsa'] = next(((l['fecha'], l['hora']) for l in api.leads if l['id'] == 'P054'), None)

    # d) reagendar a quien ya tiene consulta (desde Agenda > ficha)
    pg.click('#nav button[data-view="agenda"]'); pg.wait_for_timeout(800)
    pg.evaluate("()=>{ const b=document.createElement('button'); b.setAttribute('data-agendar','P010'); b.id='probarReag'; document.body.appendChild(b); }")
    pg.evaluate("()=>document.getElementById('probarReag').click()"); pg.wait_for_timeout(500); n0 = cuenta()
    pg.locator('#sheet.on [data-agprox]').first.click(); pg.wait_for_timeout(300)
    res['d_reagendar'] = {'boton': (pg.text_content('#sheet.on [data-saveag]') or '').strip(), 'mandado_al_tocar_horario': cuenta() - n0}
    pg.screenshot(path=os.path.join(B.OUT, 'borde_d_reagendar.png'))
    pg.click('#sheet.on [data-close]'); pg.wait_for_timeout(300)

    # e) Tránsito: día por defecto
    pg.click('#nav button[data-view="agendar"]'); pg.wait_for_timeout(700)
    abrir('Silvina')
    res['e_juan_dia_por_defecto'] = pg.evaluate("()=>{const e=document.querySelector('#sheet.on [data-agdia].on'); return e? e.textContent.trim():''}")
    res['e_juan_slots_del_dia'] = pg.locator('#sheet.on [data-slot^="Juan|"]').count()
    pg.click('#sheet.on [data-close]')
    res['errores_js'] = errs
    br.close()
B.srv.shutdown()
print(json.dumps(res, ensure_ascii=False, indent=1))
