from explora_base import *
with sync_playwright() as pw:
    b=pw.chromium.launch(); vp={'tag':'c360','vp':{'width':360,'height':640}}
    api=FakeApi()
    ctx=b.new_context(viewport=vp['vp'], is_mobile=True, has_touch=True, service_workers='block'); page=ctx.new_page()
    def route(r):
        u=r.request.url
        if GOOGLE.search(u):
            body=json.loads(r.request.post_data or '{}'); ok,data=api.handle(body.get('fn'),body.get('arg'))
            r.fulfill(status=200, content_type='application/json', body=json.dumps({'ok':True,'data':data} if ok else {'ok':False,'error':data}))
        elif '127.0.0.1' in u: r.continue_()
        else: r.abort()
    page.route('**/*',route)
    page.on('pageerror', lambda e: print('EXC',e))
    page.goto(BASE); page.wait_for_timeout(1000)
    page.click('button[data-yo="Julián"]'); page.wait_for_timeout(300)
    page.fill('#pin','1234'); page.wait_for_timeout(900)
    page.screenshot(path=OUT+'/julian_bloq.png'); print(page.inner_text('#sheet') if page.query_selector('#sheet.on') else page.inner_text('body')[:400])
    page.click('text=Elegir otro nombre'); page.wait_for_timeout(300)
    page.click('button[data-yo="Mica"]'); page.wait_for_timeout(300)
    page.fill('#pin','9999'); page.wait_for_timeout(900)
    page.screenshot(path=OUT+'/mica_mal.png'); print('---', page.inner_text('#sheet') if page.query_selector('#sheet.on') else page.inner_text('body')[:400])
    print('pin value after error:', repr(page.input_value('#pin')), 'focused:', page.evaluate('document.activeElement&&document.activeElement.id'))
    b.close()
