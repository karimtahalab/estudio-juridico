# -*- coding: utf-8 -*-
# Reporte del turno: ir y venir entre turnos ya cerrados y el de ahora (25/11). DATOS FALSOS.
# En USO del 25/11 Fran hizo 11 reporteTurno seguidos en "reporte" (5-9,8 s cada uno) mirando turnos.
# Uso: python3 pruebas/probar_turno_cache.py <carpeta con index.html> <carpeta capturas> [etiqueta]
# El banco demora 3 s cada reporteTurno (como el motor real, 5-6 s) para ver qué muestra mientras espera.
import sys, os, json
SRC, OUT = sys.argv[1], sys.argv[2]; TAG = sys.argv[3] if len(sys.argv) > 3 else 'x'
sys.argv = [sys.argv[0], SRC, OUT]
sys.path.insert(0, 'pruebas'); import explora_base as B
from playwright.sync_api import sync_playwright
os.makedirs(OUT, exist_ok=True); res = {'pasos': []}
DEMORA = r"""(() => { const f = window.fetch; window.fetch = function(u, o){
  if (o && typeof o.body === 'string' && o.body.indexOf('"fn":"reporteTurno"') >= 0) return new Promise(r => setTimeout(() => r(f.apply(this, [u, o])), 3000));
  return f.apply(this, arguments); }; })();"""
CLICK = """(sel) => { const b = document.querySelector(sel); if (!b) return 'NO HAY ' + sel; b.click();
  const t = document.querySelector('main').innerText; return t.indexOf('Armando el reporte') >= 0 ? 'ESPERA (skeleton)' : 'AL INSTANTE: ' + t.replace(/\\s+/g, ' ').slice(0, 70); }"""
with sync_playwright() as pw:
    br = pw.chromium.launch()
    for vp in [{'vp': {'width': 390, 'height': 844}, 'dsf': 3, 'n': '390'}, {'vp': {'width': 360, 'height': 640}, 'dsf': 1, 'n': '360'}]:
        page, ctx, shot, api = B.explora(br, 'Fran', vp, TAG + vp['n'], OUT)
        H = 1793888400000
        api.cierres_turno = [{'quien': 'Pri', 'desde': H - 51 * 3600000, 'cuando': H - 27 * 3600000}, {'quien': 'Fran', 'desde': H - 27 * 3600000, 'cuando': H - 3 * 3600000}]
        page.add_init_script(DEMORA); page.evaluate(DEMORA)
        calls = []; orig = api.handle
        def h(fn, arg, orig=orig): calls.append(fn); return orig(fn, arg)
        api.handle = h
        page.click('#nav button[data-view="reporte"]'); page.wait_for_timeout(3800)
        def paso(nombre, sel, foto=None):
            r = page.evaluate(CLICK, sel); page.wait_for_timeout(500)
            if foto and vp['n'] == '390': shot(foto)
            page.wait_for_timeout(3300); res['pasos'].append('%s %s: %s' % (vp['n'], nombre, r))
        page.click('[data-turcambiar]'); page.wait_for_timeout(300)
        paso('turno de Pri (1ª vez)', '[data-turver]', 'pri_1a_vez')
        paso('volver al de ahora (1ª vez)', '.tu-acts [data-turactual]', 'ahora_1a_vez')
        page.click('[data-turcambiar]'); page.wait_for_timeout(300)
        paso('turno de Pri (2ª vez)', '[data-turver]', 'pri_2a_vez')
        paso('volver al de ahora (2ª vez)', '.tu-acts [data-turactual]', 'ahora_2a_vez')
        page.click('[data-turcambiar]'); page.wait_for_timeout(300)
        paso('turno de Fran (1ª vez)', '[data-turver]:nth-of-type(2)')
        paso('volver al de ahora (3ª vez)', '.tu-acts [data-turactual]')
        page.click('[data-turcambiar]'); page.wait_for_timeout(300)
        paso('turno de Fran (2ª vez)', '[data-turver]:nth-of-type(2)')
        paso('volver (4ª vez)', '.tu-acts [data-turactual]')
        res[vp['n'] + '_reporteTurno_ida_y_vuelta'] = calls.count('reporteTurno')
        # pasa más de 1 minuto: el de ahora se renueva (mostrando lo anterior mientras tanto)
        c0 = len(calls); page.clock.run_for(70000); page.wait_for_timeout(200)
        page.click('#nav button[data-view="tareas"]'); page.wait_for_timeout(300)
        page.click('#nav button[data-view="reporte"]')
        t = page.evaluate("() => document.querySelector('main').innerText.indexOf('Armando el reporte')>=0 ? 'ESPERA (skeleton)' : 'muestra lo anterior'")
        page.wait_for_timeout(3600)
        res[vp['n'] + '_pasado_1min'] = '%s; pedidos nuevos: %d' % (t, calls[c0:].count('reporteTurno'))
        # cerrar turno: se pide de nuevo el de ahora (siempre)
        c0 = len(calls)
        page.click('[data-turconf]'); page.wait_for_timeout(300); page.click('[data-turcerrar]'); page.wait_for_timeout(4200)
        res[vp['n'] + '_cerrar'] = 'ok-box %s; cerrarTurno %d, reporteTurno %d' % (bool(page.query_selector('.ok-box')), calls[c0:].count('cerrarTurno'), calls[c0:].count('reporteTurno'))
        ctx.close()
    br.close()
res['errores'] = list(B.REPORT['errores'])
B.srv.shutdown()
print(json.dumps(res, ensure_ascii=False, indent=1))
