# -*- coding: utf-8 -*-
"""Banco (DATOS FALSOS): Fran, Pri y Agus abren o cierran horarios de las abogadas y de Juan (24/11).
  a) Fran en Agenda ve "Abrir o cerrar horarios de…" con todas las personas.
  b) Fran agenda a un lead de Tránsito: Juan no tiene horario ese día; desde la hoja toca "🗓 Juan",
     abre las 18:00, guarda y vuelve a la hoja con las 18:00 libres; lo agenda a esa hora.
  c) El editor de un intaker no muestra el modo ni "Todas las semanas" y manda solo fechas puntuales.
  d) Fran bloquea un horario de Mica desde Agenda (ya andaba: que siga andando).
  e) Mica y Karim siguen viendo el editor completo (modo y todas las semanas).
  f) Con el motor anterior (sin permisos.horarios) los intakers no ven nada nuevo.
Bloquea todo lo externo. Uso: python3 pruebas/probar_horarios_intakers.py <carpeta con index.html> <carpeta de capturas>"""
import sys, os, json
sys.argv = sys.argv[:3] + ['Fran']
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import explora_base as B
from playwright.sync_api import sync_playwright

res = {}

def abrir_app(br, api, who, vp=(390, 844)):
    pedidos, errs = [], []
    ctx = br.new_context(viewport={'width': vp[0], 'height': vp[1]}, device_scale_factor=1, is_mobile=True, has_touch=True, locale='es-AR', timezone_id='America/Argentina/Buenos_Aires', service_workers='block')
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

def shot(pg, n): pg.wait_for_timeout(250); pg.screenshot(path=os.path.join(B.OUT, 'horarios_' + n + '.png'))

with sync_playwright() as pw:
    br = pw.chromium.launch()
    # Juan solo atiende lunes y miércoles de 14 a 18 (modo "solo lo que marca")
    api = B.FakeApi()
    api.disp = {"modos": {"Juan": "disponibilidad"}, "fijo": {"Juan": {"1": "14:00-18:00", "3": "14:00-18:00"}}, "fechas": {}}
    ctx, pg, pedidos, errs = abrir_app(br, api, 'Fran')

    # a) botón en Agenda
    pg.click('#nav button[data-view="agenda"]'); pg.wait_for_timeout(700)
    t = pg.text_content('#main') or pg.text_content('body')
    res['a_boton'] = 'Abrir o cerrar horarios de' in t
    b = pg.query_selector('[data-deadm]')
    if b: b.click(); pg.wait_for_timeout(300)
    res['a_personas'] = pg.eval_on_selector_all('[data-deon]', 'bs => bs.map(b => b.getAttribute("data-deon"))')
    shot(pg, 'a_agenda_fran')

    # b) desde Agendar: Silvina (Tránsito) → Juan no tiene horario ese día → abrir 18:00
    pg.click('#nav button[data-view="agendar"]'); pg.wait_for_timeout(800)
    pg.fill('#aq', 'Silvina'); pg.wait_for_timeout(500)
    pg.locator('li.pa', has_text='Silvina').first.locator('[data-agendar]').click(); pg.wait_for_timeout(500)
    fecha = pg.input_value('#sheet.on #agFecha')
    res['b_dia_hoja'] = fecha
    res['b_sin_horario'] = 'No marcó disponibilidad ese día' in (pg.text_content('#sheet') or '')
    res['b_chip'] = pg.eval_on_selector_all('#sheet.on [data-agabrir]', 'bs => bs.map(b => b.getAttribute("data-agabrir"))')
    shot(pg, 'b1_hoja_sin_horario')
    pg.click('#sheet.on [data-agabrir="Juan"]'); pg.wait_for_timeout(800)
    res['c_editor'] = bool(pg.query_selector('[data-desave]'))
    res['c_editor_de'] = (pg.text_content('#main') or pg.text_content('body') or '').count('Juan') > 0
    res['c_dia_elegido'] = pg.get_attribute('.de-tab.sel', 'data-dedia')
    res['c_sin_modo'] = not pg.query_selector('[data-demodo]')
    res['c_sin_todas_semanas'] = not pg.query_selector('[data-deque]')
    shot(pg, 'b2_editor_juan')
    s18 = 18 * 2  # media hora 36 = 18:00
    cel = pg.query_selector('.de-col[data-ded="%s"] .de-s[data-s="%d"]' % (fecha, s18))
    res['c_celda_18'] = bool(cel)
    if cel:
        cel.scroll_into_view_if_needed(); cel.tap(); pg.wait_for_timeout(400)
    res['c_marcada'] = 'on' in (pg.get_attribute('.de-col[data-ded="%s"] .de-s[data-s="%d"]' % (fecha, s18), 'class') or '')
    shot(pg, 'b3_editor_18')
    pg.click('[data-desave]'); pg.wait_for_timeout(1200)
    envio = [a for f, a in pedidos if f == 'saveDisponibilidad']
    res['c_envio'] = envio[-1] if envio else None
    res['c_envio_solo_fechas'] = bool(envio) and 'modo' not in envio[-1] and 'fijo' not in envio[-1] and fecha in envio[-1].get('fechas', {})
    res['b_volvio_hoja'] = bool(pg.query_selector('#sheet.on [data-saveag]'))
    res['b_volvio_mismo_dia'] = bool(pg.query_selector('#sheet.on #agFecha')) and pg.input_value('#sheet.on #agFecha') == fecha
    libres = pg.eval_on_selector_all('#sheet.on [data-slot^="Juan|"]', 'bs => bs.map(b => b.textContent)')
    res['b_libres_juan'] = libres
    shot(pg, 'b4_hoja_con_18')
    if '18:00' in libres:
        pg.click('#sheet.on [data-slot="Juan|18:00"]'); pg.wait_for_timeout(300)
        pg.click('#sheet.on [data-saveag]'); pg.wait_for_timeout(7500)
    ag = [a for f, a in pedidos if f == 'agendar']
    res['b_agendado'] = (ag[-1].get('abogada'), ag[-1].get('fecha'), ag[-1].get('hora')) if ag else None
    res['b_vista_final'] = pg.get_attribute('#nav button.on', 'data-view')

    # d) bloquear un horario de Mica desde Agenda (Hoy)
    x = pg.query_selector('#sheet.on [data-close]')
    if x: x.click(); pg.wait_for_timeout(400)
    pg.click('#nav button[data-view="agenda"]'); pg.wait_for_timeout(600)
    m = pg.query_selector('[data-agmode="dia"]')
    if m: m.click(); pg.wait_for_timeout(400)
    nb = pg.query_selector('[data-nuevo]')
    res['d_boton_bloquear'] = bool(nb)
    if nb:
        nb.click(); pg.wait_for_timeout(500)
        pg.click('#sheet.on [data-bqwho="Mica"]'); pg.wait_for_timeout(200)
        pg.fill('#bqNota', 'Audiencia (prueba)')
        pg.click('#sheet.on [data-savebq]'); pg.wait_for_timeout(1000)
    bq = [a for f, a in pedidos if f == 'saveBloqueo']
    res['d_bloqueo'] = (bq[-1].get('abogada'), bq[-1].get('aclaracion')) if bq else None
    res['errores_fran'] = errs
    ctx.close()

    # f) Con el motor anterior (sin permisos.horarios) Fran no ve nada nuevo
    apiv = B.FakeApi(); apiv.motor_horarios = False
    ctx, pg, pedidos, errs = abrir_app(br, apiv, 'Fran')
    pg.click('#nav button[data-view="agenda"]'); pg.wait_for_timeout(600)
    res['f_motor_viejo_sin_boton'] = not pg.query_selector('[data-deadm], [data-deon]')
    pg.click('#nav button[data-view="agendar"]'); pg.wait_for_timeout(800)
    pg.fill('#aq', 'Silvina'); pg.wait_for_timeout(500)
    pg.locator('li.pa', has_text='Silvina').first.locator('[data-agendar]').click(); pg.wait_for_timeout(500)
    res['f_motor_viejo_sin_atajo'] = not pg.query_selector('#sheet.on [data-agabrir]')
    res['errores_motor_viejo'] = errs
    ctx.close()

    # c2) celular chico: el editor de Fran entra en 360x640
    api2 = B.FakeApi(); api2.disp = api.disp
    ctx, pg, pedidos, errs = abrir_app(br, api2, 'Agus', (360, 640))
    pg.click('#nav button[data-view="agenda"]'); pg.wait_for_timeout(600)
    b = pg.query_selector('[data-deadm]')
    if b: b.click(); pg.wait_for_timeout(300)
    pg.click('[data-deon="Mica"]'); pg.wait_for_timeout(700)
    res['c2_scroll_horizontal'] = pg.evaluate('document.documentElement.scrollWidth > document.documentElement.clientWidth + 1')
    shot(pg, 'c2_editor_mica_360')
    pg.click('[data-dequick="nada"]'); pg.wait_for_timeout(200)
    pg.click('[data-desave]'); pg.wait_for_timeout(1000)
    envio = [a for f, a in pedidos if f == 'saveDisponibilidad']
    res['c2_agus_cierra_dia'] = envio[-1] if envio else None
    res['c2_vista'] = pg.get_attribute('#nav button.on', 'data-view'); res['c2_editor_cerrado'] = not pg.query_selector('[data-desave]')
    res['errores_agus'] = errs
    ctx.close()

    # e) Mica y Karim: editor completo
    for who in ('Mica', 'Karim'):
        ctx, pg, pedidos, errs = abrir_app(br, B.FakeApi(), who)
        pg.click('#nav button[data-view="agenda"]'); pg.wait_for_timeout(600)
        m = pg.query_selector('[data-agmode="semana"]')
        if m: m.click(); pg.wait_for_timeout(300)
        b = pg.query_selector('[data-deadm]')
        if b: b.click(); pg.wait_for_timeout(300)
        d = pg.query_selector('[data-deon]')
        res['e_%s_boton' % who] = d.text_content().strip()[:60] if d else None
        if d: d.click(); pg.wait_for_timeout(600)
        res['e_%s_modo' % who] = bool(pg.query_selector('[data-demodo]'))
        res['e_%s_todas_semanas' % who] = bool(pg.query_selector('[data-deque="habitual"]'))
        hs = pg.eval_on_selector_all('#sheet.on [data-agabrir]', 'bs => bs.length')
        res['errores_' + who] = errs
        shot(pg, 'e_editor_' + who)
        ctx.close()
    br.close()

print(json.dumps(res, ensure_ascii=False, indent=1))
