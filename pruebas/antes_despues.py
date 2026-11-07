from explora_base import *
with sync_playwright() as pw:
    b=pw.chromium.launch(); vp={'tag':'c360','vp':{'width':360,'height':640}}
    for who in ['Fran','Mica']:
        page,ctx,shot,api=explora(b,who,vp,'c360',OUT)
        if who=='Fran':
            page.click('#nav button[data-view="agenda"]'); page.wait_for_timeout(800)
        page.evaluate("window.scrollTo(0, document.querySelector('#main .it .nm').getBoundingClientRect().top+scrollY-120)")
        cut=page.eval_on_selector_all('#main .nm','es=>es.filter(e=>e.scrollHeight>e.clientHeight+1||e.scrollWidth>e.clientWidth+1).map(e=>e.textContent)')
        print(who,'nombres cortados:',cut)
        shot('agenda_lista')
        page.click('button[aria-label="Buscar por nombre o teléfono"]'); page.wait_for_timeout(500)
        page.fill('#q','Prueba'); page.wait_for_timeout(900); shot('buscar')
        page.click('#sheet.on [data-close], button[aria-label="Cerrar"]') if page.query_selector('#sheet.on [data-close]') else page.keyboard.press('Escape')
        page.wait_for_timeout(400)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)"); page.wait_for_timeout(400)
        hit=page.evaluate("""()=>{const bt=document.querySelector('.foot [data-yocambiar]'); if(!bt) return 'sin boton'; const r=bt.getBoundingClientRect(); const e=document.elementFromPoint(r.left+r.width/2, r.top-8); return e===bt||bt.contains(e)}""")
        print(who,'toque 8px arriba de Cambiar llega al botón:',hit)
        # cerrar de hoja
        o=page.query_selector('#main [data-open]')
        if o:
            o.click(); page.wait_for_timeout(700)
            print(who,'Cerrar:', page.eval_on_selector('#sheet.on [data-close]','e=>{const r=e.getBoundingClientRect();return [r.width,r.height]}'))
            page.screenshot(path=OUT+'/c360_%s_ficha_cerrar.png'%who, clip={'x':0,'y':0,'width':360,'height':220})
        ctx.close()
    b.close()
print(REPORT['errores'])
