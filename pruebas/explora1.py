import sys; sys.argv=[sys.argv[0]]+sys.argv[1:]
from explora_base import *
OUTX=OUT
def T(page, sel, t=700):
    e=page.query_selector(sel)
    if not e: print('NO HAY', sel); return None
    e.click(); page.wait_for_timeout(t); return e
with sync_playwright() as pw:
    b=pw.chromium.launch()
    vp={'tag':'c360','vp':{'width':360,'height':640}}
    page,ctx,shot,api=explora(b,'Pri',vp,'c360',OUTX)
    T(page,'#nav button[data-view="agendar"]'); shot('agendar')
    T(page,'#main [data-agendar]'); shot('ag_sheet')
    page.mouse.wheel(0,400); shot('ag_sheet2')
    s=page.query_selector('#sheet [data-slot]'); print('slot', s and s.inner_text())
    if s: s.click(); page.wait_for_timeout(400); shot('ag_slot')
    sv=page.query_selector('#sheet [data-saveag]'); print('save', sv and sv.inner_text())
    if sv: sv.click(); page.wait_for_timeout(1200); shot('ag_guardado')
    print('toast', page.eval_on_selector('#toast','e=>e.innerText') if page.query_selector('#toast') else None)
    c=page.query_selector('#sheet.on [data-close]'); 
    if c: c.click(); page.wait_for_timeout(400)
    # buscar
    T(page,'button[aria-label="Buscar por nombre o teléfono"]'); shot('buscar')
    if page.query_selector('#q'): page.fill('#q','Rubén'); page.wait_for_timeout(900); shot('buscar_res')
    print('calls', api.calls)
    ctx.close()
    # Juan bloqueo
    page,ctx,shot,api=explora(b,'Juan',vp,'c360',OUTX)
    shot('juan_inicio')
    print('nav juan', page.eval_on_selector_all('#nav button[data-view]','bs=>bs.filter(b=>!b.hidden).map(b=>b.dataset.view)'))
    print('texto juan tiene ART?', 'ART' in page.inner_text('#main'), 'Mica' in page.inner_text('#main'))
    e=page.query_selector('#main [data-open]')
    if e: e.click(); page.wait_for_timeout(700); shot('juan_ficha'); page.mouse.wheel(0,1500); shot('juan_ficha_abajo')
    ctx.close(); b.close()
print(REPORT['errores'])
