# -*- coding: utf-8 -*-
# Reporte del turno: con el reporte en memoria, otra persona que entra en el mismo celular no ve el de la anterior. DATOS FALSOS.
import sys, os, json
SRC, OUT = sys.argv[1], sys.argv[2]; sys.argv=[sys.argv[0], SRC, OUT]
sys.path.insert(0,'pruebas'); import explora_base as B
from playwright.sync_api import sync_playwright
res={}
with sync_playwright() as pw:
    br=pw.chromium.launch()
    page,ctx,shot,api=B.explora(br,'Fran',{'vp':{'width':390,'height':844},'dsf':1},'persona',OUT)
    calls=[]; o=api.handle
    def h(fn,arg): calls.append((fn,(arg or {}).get('who'))); return o(fn,arg)
    api.handle=h
    page.click('#nav button[data-view="reporte"]'); page.wait_for_timeout(1200)
    res['fran']=page.inner_text('main')[:60].replace('\n',' ')
    page.click('#btnYo'); page.wait_for_timeout(500); page.click('[data-salir]'); page.wait_for_timeout(800)
    page.click('button[data-yo="Pri"]'); page.wait_for_timeout(300)
    page.fill('#pin','1234'); page.wait_for_timeout(700)
    if page.query_selector('#sheet.on #pin'): page.fill('#pin','1234'); page.wait_for_timeout(700)
    page.wait_for_timeout(1200)
    n0=len(calls)
    page.click('#nav button[data-view="reporte"]'); page.wait_for_timeout(1500)
    res['pri_pedidos']=[c for c in calls[n0:] if c[0]=='reporteTurno']
    res['pri_ve_yo']=page.evaluate("()=>{const t=document.querySelector('main').innerText; return t.slice(0,80).replace(/\\s+/g,' ')}")
    res['errores']=list(B.REPORT['errores'])
    br.close()
B.srv.shutdown(); print(json.dumps(res,ensure_ascii=False,indent=1))
