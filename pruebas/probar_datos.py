# Corregir datos y Cambiar fase en la ficha (Pri, 23/11: "Escribí el nombre." llegó del motor después de mandar editarDatos; Pri usa una compu de 1163x587).
# Uso: python3 pruebas/probar_datos.py <carpeta con index.html> <carpeta capturas>. Datos falsos; el motor falso revisa nombre/teléfono/email como el real.
import sys, os, json
OUT=sys.argv[2]; sys.argv=[sys.argv[0], sys.argv[1], OUT]
sys.path.insert(0,'pruebas'); import explora_base as B
from playwright.sync_api import sync_playwright
os.makedirs(OUT,exist_ok=True); res={}
VPS=[('pc',{'width':1163,'height':587},1),('360',{'width':360,'height':640},1),('390',{'width':390,'height':844},3)]
VIS="""(sel)=>{const p=document.querySelector('#sheet.on .fi-panel'); const b=document.querySelector(sel); if(!p||!b) return null; const r=p.getBoundingClientRect(), rb=b.getBoundingClientRect(); return {panel_a_la_vista: r.top>=0 && r.top<innerHeight-60, boton_a_la_vista: rb.top>=0 && rb.bottom<=innerHeight}}"""
def txt(page, sel): e=page.query_selector(sel); return e.inner_text() if e else None
with sync_playwright() as pw:
    br=pw.chromium.launch()
    for tag,vp,d in VPS:
        page,ctx,shot,api=B.explora(br,'Pri',{'vp':vp,'dsf':d},'dat'+tag,OUT)
        calls=[]; orig=api.handle
        def h(fn,arg,orig=orig):
            if fn in ('editarDatos','cambiarFase'): calls.append(fn)
            return orig(fn,arg)
        api.handle=h; r={}
        page.click('#nav button[data-view="agendar"]'); page.wait_for_timeout(500)
        page.click('[data-ficha]'); page.wait_for_timeout(600)
        page.click('#sheet.on [data-fimodo="fase"]'); page.wait_for_timeout(900)
        r['fase']=page.evaluate(VIS, '#sheet.on [data-fase]'); shot('fase')
        page.click('#sheet.on [data-fimodo="fase"]'); page.wait_for_timeout(300)
        page.evaluate("()=>document.querySelectorAll('#sheet.on, #sheet.on *').forEach(e=>{if(e.scrollTop) e.scrollTop=0})"); page.wait_for_timeout(200)
        page.click('#sheet.on [data-fimodo="datos"]'); page.wait_for_timeout(900)
        r['datos']=page.evaluate(VIS, '[data-datosave]'); shot('datos_abierto')
        nombre=page.input_value('#fdNombre')
        # nombre borrado
        page.fill('#fdNombre',''); page.wait_for_timeout(300)
        n={'aviso_campo':txt(page,'#fdNombreH'),'boton_habilitado':page.is_enabled('[data-datosave]')}
        page.eval_on_selector('#fdNombre','e=>e.scrollIntoView({block:"center"})'); shot('nombre_vacio')
        if n['boton_habilitado']:
            page.click('[data-datosave]'); page.wait_for_timeout(1200); n['aviso']=txt(page,'#toast.on'); shot('nombre_rechazado')
        n['pedidos']=list(calls); r['nombre_vacio']=n; calls.clear()
        page.fill('#fdNombre',nombre); page.wait_for_timeout(200)
        # teléfono corto
        page.fill('#fdTel','26155'); page.wait_for_timeout(300)
        t={'aviso_campo':txt(page,'#fdTelH'),'boton_habilitado':page.is_enabled('[data-datosave]')}
        if t['boton_habilitado']:
            page.click('[data-datosave]'); page.wait_for_timeout(1200); t['aviso']=txt(page,'#toast.on')
        t['pedidos']=list(calls); r['tel_corto']=t; calls.clear()
        # teléfono bien → se guarda
        if page.query_selector('#fdTel'):
            page.fill('#fdTel','261 555-7788'); page.wait_for_timeout(300)
            g={'aviso_campo':txt(page,'#fdTelH'),'boton_habilitado':page.is_enabled('[data-datosave]')}
            page.click('[data-datosave]'); page.wait_for_timeout(1200); g['aviso']=txt(page,'#toast.on'); g['pedidos']=list(calls); r['tel_bien']=g
        res[tag]=r; ctx.close()
    br.close()
print(json.dumps({'res':res,'err':B.REPORT['errores']},ensure_ascii=False,indent=1))
