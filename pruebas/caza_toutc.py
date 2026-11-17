# Uso: copiar index.html a una carpeta, cambiar toUTC para que avise (console.error TOUTC + stack) si recibe algo que no es texto, y correr: python3 pruebas/caza_toutc.py <carpeta> <capturas>. Toca casi todos los botones de cada pestaña (Karim 1422x701 y 390, Pri 1280x646, Mica 390).
# Caza del error "s.split is not a function" (toUTC). Datos falsos; todo pedido a Google se responde local.
import sys, os, json, re
sys.argv=[sys.argv[0], sys.argv[1], sys.argv[2]]
sys.path.insert(0, 'pruebas')
import explora_base as B
from playwright.sync_api import sync_playwright
OUT=sys.argv[2]; os.makedirs(OUT, exist_ok=True)
hall=[]
def go(browser, who, vp, mobile):
    api=B.FakeApi()
    ctx=browser.new_context(viewport=vp, device_scale_factor=1, is_mobile=mobile, has_touch=mobile, locale='es-AR', timezone_id='America/Argentina/Buenos_Aires', service_workers='block')
    page=ctx.new_page(); page.clock.install(time='2026-11-05T11:20:00-03:00')
    def route(r):
        u=r.request.url
        if B.GOOGLE.search(u):
            try: body=json.loads(r.request.post_data or '{}')
            except Exception: body={}
            ok,data=api.handle(body.get('fn'), body.get('arg'))
            r.fulfill(status=200, content_type='application/json', body=json.dumps({'ok':True,'data':data} if ok else {'ok':False,'error':data}))
        elif u.startswith('http://127.0.0.1:%d/'%B.PORT): r.continue_()
        else: r.abort()
    page.route('**/*', route)
    page.on('pageerror', lambda e: hall.append('%s EXC %s'%(who,str(e)[:300])))
    page.on('console', lambda m: m.type=='error' and 'TOUTC' in m.text and hall.append('%s %s'%(who,m.text[:600])))
    page.goto(B.BASE); page.wait_for_timeout(1000)
    page.click('button[data-yo="%s"]'%who); page.wait_for_timeout(300)
    page.fill('#pin','1234'); page.wait_for_timeout(700)
    if page.query_selector('#sheet.on #pin'): page.fill('#pin','1234'); page.wait_for_timeout(700)
    page.wait_for_timeout(1200)
    views=page.eval_on_selector_all('#nav button[data-view]','bs=>bs.filter(b=>!b.hidden).map(b=>b.getAttribute("data-view"))')
    SKIP=re.compile(r'data-(salir|yocambiar|vcabrir|wsp|escribir|pastefor|pasteall|decopy|retry)')
    clicks=0
    for v in views:
        for rnd in range(2):
            page.click('#nav button[data-view="%s"]'%v); page.wait_for_timeout(500)
            n=page.evaluate("()=>document.querySelectorAll('#main button, #main [data-open]').length")
            for i in range(min(n,60)):
                try:
                    page.click('#nav button[data-view="%s"]'%v, timeout=1500); page.wait_for_timeout(150)
                    els=page.query_selector_all('#main button, #main [data-open]')
                    if i>=len(els): break
                    e=els[i]; h=e.evaluate('e=>e.outerHTML.slice(0,200)')
                    if SKIP.search(h) or not e.is_visible(): continue
                    e.click(timeout=1500); clicks+=1; page.wait_for_timeout(300)
                    if page.query_selector('#sheet.on'):
                        sb=page.query_selector_all('#sheet.on button')
                        for b in sb[:25]:
                            try:
                                hh=b.evaluate('e=>e.outerHTML.slice(0,200)')
                                if 'data-close' in hh or SKIP.search(hh) or not b.is_visible(): continue
                                b.click(timeout=800); clicks+=1; page.wait_for_timeout(120)
                                if not page.query_selector('#sheet.on'): break
                            except Exception: pass
                        c=page.query_selector('#sheet.on [data-close]')
                        if c:
                            try: c.click(timeout=800)
                            except Exception: pass
                        page.keyboard.press('Escape'); page.wait_for_timeout(200)
                except Exception as ex: pass
    page.wait_for_timeout(7000)
    ctx.close(); return clicks
with sync_playwright() as pw:
    br=pw.chromium.launch()
    for who in sys.argv[3:] or ['Karim','Julián','Pri','Mica']:
        pass
    tot={}
    for who,vp,mob in [('Karim',{'width':1422,'height':701},False),('Karim',{'width':390,'height':844},True),('Pri',{'width':1280,'height':646},False),('Mica',{'width':390,'height':844},True)]:
        tot[who+str(vp['width'])]=go(br,who,vp,mob)
    br.close()
print(json.dumps({'clicks':tot,'hallazgos':hall[:40],'n':len(hall)},ensure_ascii=False,indent=1))
