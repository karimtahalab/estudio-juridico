# Uso: python3 pruebas/probar_pasar_bc.py <carpeta con index.html> <carpeta capturas>. Datos falsos: P001-P003 pasan a No show/Reagenda/Seguimiento para que aparezca el botón.
import sys, os, json
sys.argv=[sys.argv[0], sys.argv[1], sys.argv[2]]
sys.path.insert(0,'pruebas'); import explora_base as B
from playwright.sync_api import sync_playwright
_F=B.FakeApi
class F2(_F):
    def __init__(self):
        super().__init__()
        for l,f in zip([x for x in self.leads if x.get('fecha')<=B_D0], ['No show','Reagenda','Seguimiento']): l['fase']=f
from datos_falsos import D as _D
B_D0=_D(0)
B.FakeApi=F2
OUT=sys.argv[2]; os.makedirs(OUT,exist_ok=True); res={}
with sync_playwright() as pw:
    br=pw.chromium.launch()
    for who in ['Fran','Mica']:
        page,ctx,shot,api=B.explora(br,who,{'vp':{'width':390,'height':844}},'bc',OUT)
        calls=[]
        orig=api.handle
        def h(fn,arg,orig=orig):
            if fn=='cambiarFase': calls.append(arg)
            return orig(fn,arg)
        api.handle=h
        page.click('#nav button[data-view="agenda"]'); page.wait_for_timeout(500)
        ids=page.eval_on_selector_all('[data-open]','es=>es.map(e=>e.getAttribute("data-open"))')
        found=None
        for i in ids:
            page.click('#nav button[data-view="agenda"]'); page.wait_for_timeout(200)
            e=page.query_selector('[data-open="%s"]'%i)
            if not e: continue
            e.click(); page.wait_for_timeout(400)
            if page.query_selector('#sheet.on [data-pasarbc]'): found=i; break
            page.click('#sheet.on [data-close]'); page.wait_for_timeout(300)
        r={'boton':bool(found)}
        if found:
            b=page.query_selector('#sheet.on [data-pasarbc]'); bb=b.bounding_box(); r['tam']=[round(bb['width']),round(bb['height'])]
            b.click(); page.wait_for_timeout(300); r['texto1']=page.inner_text('#sheet.on [data-pasarbc]'); shot('bc_confirmar')
            page.click('#sheet.on [data-pasarbc]'); page.wait_for_timeout(600); shot('bc_hecho')
            r['toast']=page.inner_text('#toast') if page.query_selector('#toast') else ''
            r['sigue_en_agenda']=bool(page.query_selector('[data-open="%s"]'%found))
            u=page.query_selector('#toast [data-undo]')
            if u: u.click(); page.wait_for_timeout(1200)
            r['vuelve']=bool(page.query_selector('[data-open="%s"]'%found)); shot('bc_deshecho')
            r['calls']=calls
        res[who]=r; ctx.close()
    br.close()
print(json.dumps({'res':res,'err':B.REPORT['errores']},ensure_ascii=False,indent=1))
