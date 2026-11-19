# Cargar a alguien nuevo con un email mal escrito (lo que el 18/11 le pasó a Fran: "Revisá el email." 2 veces al final del agendar).
# Uso: python3 pruebas/probar_email.py <carpeta con index.html> <carpeta capturas>. Datos falsos; el motor falso revisa el email igual que el real.
import sys, os, json
sys.argv=[sys.argv[0], sys.argv[1], sys.argv[2]]
sys.path.insert(0,'pruebas'); import explora_base as B
from playwright.sync_api import sync_playwright
OUT=sys.argv[2]; os.makedirs(OUT,exist_ok=True); res={}
with sync_playwright() as pw:
    br=pw.chromium.launch()
    for vp in [{'vp':{'width':390,'height':844},'dsf':3,'t':'390'},{'vp':{'width':360,'height':640},'dsf':1,'t':'360'}]:
        page,ctx,shot,api=B.explora(br,'Fran',vp,'mail'+vp['t'],OUT)
        calls=[]; orig=api.handle
        def h(fn,arg,orig=orig):
            if fn in ('agendarNuevo','agendar'): calls.append(fn)
            return orig(fn,arg)
        api.handle=h
        page.click('#nav button[data-view="agendar"]'); page.wait_for_timeout(500)
        page.click('[data-agnuevo]'); page.wait_for_timeout(500)
        page.fill('#mnNombre','Rosa Prueba Lucero'); page.fill('#mnTel','2615559911')
        page.click('#sheet.on [data-mnrama="ART"]'); page.wait_for_timeout(200)
        page.click('#sheet.on [data-mnorigen]'); page.wait_for_timeout(200)
        page.fill('#mnEmail','rosa.lucero@gmail'); page.wait_for_timeout(300)
        r={'hint':page.inner_text('#mnEmailH') if page.query_selector('#mnEmailH') else None,
           'boton_habilitado':page.is_enabled('#sheet.on [data-mnsig]')}
        page.eval_on_selector('#mnEmail','e=>e.scrollIntoView({block:"center"})'); shot('email_mal')
        toques=0; err=''
        if r['boton_habilitado']:
            # como en main: sigue al horario, elige el primero libre y agenda
            page.click('#sheet.on [data-mnsig]'); toques+=1; page.wait_for_timeout(500)
            slot=page.query_selector('#sheet.on [data-slot]:not([disabled])') or page.query_selector('#sheet.on .slot:not([disabled])')
            if slot: slot.click(); toques+=1; page.wait_for_timeout(300)
            sv=page.query_selector('#sheet.on [data-save]:not([disabled])') or page.query_selector('#sheet.on .save:not([disabled])')
            if sv: sv.click(); toques+=1; page.wait_for_timeout(900)
            err=page.inner_text('#toast') if page.query_selector('#toast.on') else ''
            shot('email_rechazado')
        r.update({'toques_hasta_enterarse':toques,'aviso':err,'pedidos':list(calls)})
        page.fill('#mnEmail','rosa.lucero@gmail.com') if page.query_selector('#sheet.on #mnEmail') else None
        page.wait_for_timeout(300)
        if page.query_selector('#sheet.on [data-mnsig]'):
            r['hint_corregido']=page.inner_text('#mnEmailH') if page.query_selector('#mnEmailH') else None
            r['boton_corregido']=page.is_enabled('#sheet.on [data-mnsig]')
            page.eval_on_selector('#mnEmail','e=>e.scrollIntoView({block:"center"})'); shot('email_bien')
        res[vp['t']]=r; ctx.close()
    br.close()
print(json.dumps({'res':res,'err':B.REPORT['errores']},ensure_ascii=False,indent=1))
