# -*- coding: utf-8 -*-
"""Pedidos colgados (DATOS FALSOS). Uso: python3 pruebas/probar_colgados.py <carpeta con index.html> <salida>
Simula lo que mostró el registro de uso real (07/11: getFin2 esperó 18 minutos): el servidor no contesta un pedido de lectura.
A) se toca Actualizar, el pedido se cuelga, la persona sale y vuelve a la app a los 15 s.
B) se toca Actualizar, el pedido se cuelga y la persona se queda mirando 40 s.
C) se carga un resultado (saveAction) y el servidor tarda: las escrituras NO se cortan nunca.
Cada caso dice si la pantalla se recupera sola (sin girar para siempre) y con datos nuevos."""
from explora_base import *
COLGAR = {'fn': None, 'n': 0}
colgados = []
def caso(b, nombre, accion):
    api = FakeApi()
    ctx = b.new_context(viewport={'width':390,'height':844}, is_mobile=True, has_touch=True, locale='es-AR', timezone_id='America/Argentina/Buenos_Aires', service_workers='block')
    page = ctx.new_page(); page.clock.install(time='2026-11-05T11:20:00-03:00')
    pedidos = []
    def route(r):
        u = r.request.url
        if GOOGLE.search(u):
            body = json.loads(r.request.post_data or '{}'); fn = body.get('fn'); pedidos.append(fn)
            if COLGAR['fn'] == fn and COLGAR['n'] > 0:
                COLGAR['n'] -= 1; colgados.append(r); return   # no contesta nunca
            ok, data = api.handle(fn, body.get('arg'))
            r.fulfill(status=200, content_type='application/json', body=json.dumps({'ok': True, 'data': data} if ok else {'ok': False, 'error': data}))
        elif '127.0.0.1' in u: r.continue_()
        elif 'fonts.gstatic.com' in u: r.fulfill(status=200, content_type='font/woff2', body=FUENTE)
        else: r.abort()
    page.route('**/*', route)
    errs = []
    page.on('pageerror', lambda e: errs.append(str(e)[:200]))
    page.goto(BASE); page.wait_for_timeout(1000)
    page.click('button[data-yo="Mica"]'); page.wait_for_timeout(300); page.fill('#pin', '1234'); page.wait_for_timeout(1500)
    res = accion(page, pedidos)
    res['errores_js'] = errs
    page.screenshot(path=os.path.join(OUT, 'colgado_%s.png' % nombre))
    ctx.close(); print(nombre, json.dumps(res, ensure_ascii=False)); return res

def gira(page): return page.evaluate("document.getElementById('btnRefresh').classList.contains('spin')")
def vis(page, oculto):
    page.evaluate("""h=>{Object.defineProperty(document,'visibilityState',{configurable:true,get:()=>h?'hidden':'visible'});Object.defineProperty(document,'hidden',{configurable:true,get:()=>h});document.dispatchEvent(new Event('visibilitychange'));}""", oculto)

def A(page, pedidos):
    COLGAR.update(fn='getData', n=1); n0 = pedidos.count('getData')
    page.click('#btnRefresh'); page.wait_for_timeout(300)
    antes = gira(page)
    vis(page, True); page.clock.run_for(15000); vis(page, False)
    page.clock.run_for(2500); page.wait_for_timeout(800); page.clock.run_for(1000); page.wait_for_timeout(500)
    return {'girando_al_tocar': antes, 'girando_despues': gira(page), 'getData_pedidos': pedidos.count('getData') - n0}
def B(page, pedidos):
    COLGAR.update(fn='getData', n=1); n0 = pedidos.count('getData')
    page.click('#btnRefresh'); page.wait_for_timeout(300)
    page.clock.run_for(36000); page.wait_for_timeout(300); page.clock.run_for(2000); page.wait_for_timeout(800)
    return {'girando_despues_40s': gira(page), 'getData_pedidos': pedidos.count('getData') - n0, 'pantalla_ok': page.query_selector('#main .err-box') is None}
def C(page, pedidos):
    # cargar resultado (saveAction) colgado 65 s, saliendo y volviendo a la app: es escritura, no se corta ni se repite
    COLGAR.update(fn='saveAction', n=1); n0 = pedidos.count('saveAction')
    r = page.query_selector('[data-result]')
    if not r: return {'sin_boton': True}
    r.click(); page.wait_for_timeout(600); page.click('#sheet [data-res="nofirmo"]'); page.wait_for_timeout(300)
    m = page.query_selector('#sheet [data-motivo]')
    if m: m.click(); page.wait_for_timeout(200)
    page.click('#sheet [data-save]'); page.wait_for_timeout(500)
    vis(page, True); page.clock.run_for(20000); vis(page, False); page.clock.run_for(45000); page.wait_for_timeout(500)
    return {'saveAction_pedidos': pedidos.count('saveAction') - n0}

with sync_playwright() as pw:
    b = pw.chromium.launch()
    ra = caso(b, 'A_sale_y_vuelve', A); rb = caso(b, 'B_espera', B); rc = caso(b, 'C_escritura', C)
    b.close()
