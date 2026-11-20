# -*- coding: utf-8 -*-
# Producción (Fede): cuánto tarda en ver Guiones la primera vez, con getData lento (motor de hoy) o rápido
# (motor con mejora-2026-11-20.json) y getCreativos de 4 s. DATOS FALSOS; bloquea todo lo externo.
# Uso: python3 pruebas/probar_prod.py <carpeta con index.html> <carpeta capturas> [ms getData,...]
import sys, os, json, time, asyncio, re, threading, functools, http.server, socketserver
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from datos_falsos import FakeApi
from playwright.async_api import async_playwright
SRC=os.path.abspath(sys.argv[1]); OUT=sys.argv[2]; os.makedirs(OUT,exist_ok=True)
DEMORAS=[int(x) for x in (sys.argv[3] if len(sys.argv)>3 else '9000,1500').split(',')]
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
srv=socketserver.TCPServer(('127.0.0.1',0), functools.partial(Q, directory=SRC)); PORT=srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
GOOGLE=re.compile(r'script\.google\.com|googleusercontent\.com|docs\.google\.com')
CRE={"ramas":[{"rama":"ART","videos":[]}],"anio":2026,"mes":11}
async def caso(br, dgd):
    api=FakeApi(); log=[]; t0=[time.time()]
    ctx=await br.new_context(viewport={'width':390,'height':844}, is_mobile=True, has_touch=True, locale='es-AR', timezone_id='America/Argentina/Buenos_Aires', service_workers='block')
    page=await ctx.new_page()
    async def route(r):
        u=r.request.url
        if GOOGLE.search(u):
            b=json.loads(r.request.post_data or '{}'); fn=b.get('fn'); log.append((fn, round(time.time()-t0[0],1)))
            if fn=='getData': await asyncio.sleep(dgd/1000)
            if fn=='getCreativos': await asyncio.sleep(4); ok,data=True,CRE
            else: ok,data=api.handle(fn,b.get('arg'))
            await r.fulfill(status=200, content_type='application/json', body=json.dumps({'ok':True,'data':data} if ok else {'ok':False,'error':data}))
        elif u.startswith('http://127.0.0.1:%d/'%PORT): await r.continue_()
        else: await r.abort()
    await page.route('**/*', route)
    errs=[]; page.on('pageerror', lambda e: errs.append(str(e)[:200]))
    await page.goto('http://127.0.0.1:%d/index.html'%PORT); await page.wait_for_timeout(1000)
    await page.click('button[data-yo="Fede"]'); await page.wait_for_timeout(300)
    t0[0]=time.time(); await page.fill('#pin','1234'); vio=None
    FOTO=float(os.environ.get('FOTO','0')); foto=False
    for i in range(300):
        if FOTO and not foto and time.time()-t0[0]>=FOTO: foto=True; await page.screenshot(path=os.path.join(OUT,'prod_fede_getData%d_a_los_%ss.png'%(dgd,FOTO)))
        await page.wait_for_timeout(100)
        if 'Todavía no hay guiones' in (await page.inner_text('main')):
            vio=round(time.time()-t0[0],1)
            if not FOTO or foto: break
    await ctx.close()
    return {'getData_ms':dgd,'segundos_hasta_ver_guiones':vio,'pedidos':log,'errores':errs}
async def main():
    async with async_playwright() as pw:
        br=await pw.chromium.launch(); out=[]
        for d in DEMORAS: out.append(await caso(br,d))
        await br.close(); print(json.dumps(out,ensure_ascii=False))
asyncio.run(main()); srv.shutdown()
