# -*- coding: utf-8 -*-
"""Banco (DATOS FALSOS): "👤 Turno con cliente" (publicado el 27/11, d797eee).
  a) Juan en Agenda (día) ve "👤 Turno con cliente"; la hoja abre con él elegido.
  b) Sin nombre: no sale ningún pedido.
  c) Nombre + teléfono + a qué viene, cambia la hora de inicio (el fin se corre) → 1 saveBloqueo con la aclaración "👤 Cliente: …".
  d) El turno se ve en la agenda; al abrirlo muestra lo cargado; "Sacar" pide 2 toques → 1 deleteBloqueo.
  e) Fran (intaker) en la agenda de Juan: ve el turno; no deja agendar en ese horario.
En 390x844 y 360x640. Uso: python3 pruebas/probar_turno_cliente.py <carpeta con index.html> <carpeta de capturas>"""
import sys, os, json
sys.argv = sys.argv[:3] + ['Juan']
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import explora_base as B
from playwright.sync_api import sync_playwright

res = {}

def abrir_app(br, api, who, vp):
    pedidos, errs = [], []
    ctx = br.new_context(viewport={'width': vp[0], 'height': vp[1]}, device_scale_factor=2, is_mobile=True, has_touch=True, locale='es-AR', timezone_id='America/Argentina/Buenos_Aires', service_workers='block')
    pg = ctx.new_page(); pg.clock.install(time='2026-11-05T11:20:00-03:00')
    pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    pg.on('console', lambda m: m.type == 'error' and 'ERR_FAILED' not in m.text and errs.append('console: ' + m.text[:200]))
    def route(r):
        u = r.request.url
        if B.GOOGLE.search(u):
            b = json.loads(r.request.post_data or '{}'); pedidos.append((b.get('fn'), b.get('arg')))
            ok, d = api.handle(b.get('fn'), b.get('arg')); r.fulfill(status=200, content_type='application/json', body=json.dumps({'ok': ok, 'data': d} if ok else {'ok': False, 'error': d}))
        elif u.startswith('http://127.0.0.1:%d/' % B.PORT): r.continue_()
        else: r.abort()
    pg.route('**/*', route)
    pg.goto(B.BASE); pg.wait_for_timeout(1000); pg.click('button[data-yo="%s"]' % who); pg.wait_for_timeout(300)
    pg.fill('#pin', '1234'); pg.wait_for_timeout(700)
    if pg.query_selector('#sheet.on #pin'): pg.fill('#pin', '1234'); pg.wait_for_timeout(700)
    pg.wait_for_timeout(1200)
    return ctx, pg, pedidos, errs

def fns(p, nombre): return [a for f, a in p if f == nombre]

with sync_playwright() as pw:
    br = pw.chromium.launch()
    for vp in [(390, 844), (360, 640)]:
        tag = '%d' % vp[0]; R = res.setdefault(tag, {})
        def shot(pg, n): pg.wait_for_timeout(250); pg.screenshot(path=os.path.join(B.OUT, 'cliente_%s_%s.png' % (tag, n)))
        api = B.FakeApi()
        ctx, pg, ped, errs = abrir_app(br, api, 'Juan', vp)
        pg.click('#nav button[data-view="agenda"]'); pg.wait_for_timeout(700)
        bt = pg.query_selector('[data-nuevocli]')
        R['a_boton'] = bool(bt)
        if bt:
            bb = bt.bounding_box(); R['a_boton_tam'] = [round(bb['width']), round(bb['height'])]
            bt.scroll_into_view_if_needed(); shot(pg, 'a_agenda'); bt.click(); pg.wait_for_timeout(500)
        R['a_hoja'] = 'Turno con un cliente' in (pg.text_content('#sheet') or '')
        R['a_elegido'] = pg.eval_on_selector_all('#sheet.on [data-bqwho].on', 'bs=>bs.map(b=>b.textContent)')
        R['a_tel_inputmode'] = pg.get_attribute('#cliTel', 'inputmode')
        sv = pg.query_selector('#sheet.on [data-savebq]')
        R['a_guardar_visible'] = bool(sv) and sv.bounding_box()['y'] + sv.bounding_box()['height'] <= vp[1]
        R['a_guardar_texto'] = sv.text_content() if sv else None
        shot(pg, 'b_hoja')
        n0 = len(fns(ped, 'saveBloqueo'))
        sv.click(); pg.wait_for_timeout(400)
        R['b_sin_nombre_pedidos'] = len(fns(ped, 'saveBloqueo')) - n0
        R['b_toast'] = (pg.text_content('#toast') or '').strip()[:80]
        shot(pg, 'b_sin_nombre')
        pg.fill('#cliNom', 'Ramiro Prueba'); pg.fill('#cliTel', '261 555 9090'); pg.fill('#cliNota', 'Firma el poder (prueba)')
        pg.select_option('#bqDesde', '16:00'); pg.wait_for_timeout(400)
        R['c_hasta'] = pg.input_value('#bqHasta'); R['c_nombre_sigue'] = pg.input_value('#cliNom')
        R['c_nota_sigue'] = pg.input_value('#cliNota')
        shot(pg, 'c_completa')
        pg.click('#sheet.on [data-savebq]'); pg.wait_for_timeout(900)
        sb = fns(ped, 'saveBloqueo'); R['c_pedidos'] = len(sb); R['c_arg'] = {k: sb[-1].get(k) for k in ('fecha', 'desde', 'hasta', 'abogada', 'aclaracion', 'todoDia')} if sb else None
        R['c_toast'] = (pg.text_content('#toast') or '').strip()[:80]
        R['c_hoja_cerrada'] = not pg.query_selector('#sheet.on')
        main = pg.text_content('#main') or pg.text_content('body')
        R['d_en_agenda'] = 'Ramiro Prueba' in main
        shot(pg, 'd_agenda_con_turno')
        it = pg.query_selector('[aria-label="Ver turno con Ramiro Prueba"]')
        R['d_tarjeta'] = bool(it)
        if it:
            it.scroll_into_view_if_needed(); it.click(); pg.wait_for_timeout(500)
            t = pg.text_content('#sheet') or ''
            R['d_detalle'] = all(x in t for x in ('Ramiro Prueba', 'Firma el poder', '261 555 9090'))
            shot(pg, 'd_detalle')
            pg.click('#sheet.on [data-delbq]'); pg.wait_for_timeout(300)
            R['d_1er_toque_pedidos'] = len(fns(ped, 'deleteBloqueo'))
            pg.click('#sheet.on [data-delbq]'); pg.wait_for_timeout(800)
            R['d_2do_toque_pedidos'] = len(fns(ped, 'deleteBloqueo'))
            R['d_toast'] = (pg.text_content('#toast') or '').strip()[:80]
            R['d_sale_agenda'] = 'Ramiro Prueba' not in (pg.text_content('#main') or pg.text_content('body'))
        R['errores'] = errs; ctx.close()
        # e) Fran con un turno de Juan ya anotado hoy 12:00-12:30
        api2 = B.FakeApi()
        api2.handle('saveBloqueo', {'who': 'Juan', 'fecha': '2026-11-05', 'desde': '12:00', 'hasta': '12:30', 'todoDia': False, 'abogada': 'Juan', 'aclaracion': '👤 Cliente: Elsa Prueba · tel 2615550000'})
        ctx, pg, ped, errs = abrir_app(br, api2, 'Fran', vp)
        pg.click('#nav button[data-view="agenda"]'); pg.wait_for_timeout(700)
        j = pg.query_selector('[data-abog="Juan"]')
        if j: j.click(); pg.wait_for_timeout(500)
        R['e_ve_turno'] = 'Elsa Prueba' in (pg.text_content('#main') or pg.text_content('body'))
        R['e_boton'] = bool(pg.query_selector('[data-nuevocli]'))
        shot(pg, 'e_fran_agenda_juan')
        R['e_errores'] = errs; ctx.close()
    br.close()
B.srv.shutdown()
print(json.dumps(res, ensure_ascii=False, indent=1))
