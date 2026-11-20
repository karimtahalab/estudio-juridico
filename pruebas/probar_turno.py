# -*- coding: utf-8 -*-
# Reporte del turno (intakers, nuevo del 19/11) y apertura de producción (Fede). DATOS FALSOS.
# Uso: python3 pruebas/probar_turno.py <carpeta con index.html> <carpeta capturas>
import sys, os, json, time
sys.argv=[sys.argv[0], sys.argv[1], sys.argv[2]]
sys.path.insert(0,'pruebas'); import explora_base as B
from playwright.sync_api import sync_playwright
OUT=sys.argv[2]; os.makedirs(OUT,exist_ok=True); res={}
def espiar(api, lst):
    orig=api.handle
    def h(fn,arg):
        lst.append(fn); return orig(fn,arg)
    api.handle=h
with sync_playwright() as pw:
    br=pw.chromium.launch()
    # 1) Pri en Reporte: cuántos reporteTurno salen quedándose 6 min en la pantalla y yendo y viniendo
    page,ctx,shot,api=B.explora(br,'Pri',{'vp':{'width':390,'height':844},'dsf':1},'turno',OUT)
    calls=[]; espiar(api,calls)
    page.click('#nav button[data-view="reporte"]'); page.wait_for_timeout(800)
    for m in range(6):
        page.clock.run_for(60000); page.wait_for_timeout(400)
    res['reporteTurno_6min_quieta']=calls.count('reporteTurno'); res['getData_6min']=calls.count('getData')
    c0=len(calls)
    for v in ['tareas','reporte','agenda','reporte']:
        page.click('#nav button[data-view="%s"]'%v); page.wait_for_timeout(500)
    res['reporteTurno_ir_y_volver']=calls[c0:].count('reporteTurno')
    # cerrar turno
    page.click('[data-turconf]'); page.wait_for_timeout(300); shot('confirmar')
    page.click('[data-turcerrar]'); page.wait_for_timeout(1200); shot('cerrado')
    res['cerrado_ok']=bool(page.query_selector('.ok-box'))
    res['errores']=list(B.REPORT['errores'])
    ctx.close()
    # 2) Fede (producción): orden de pedidos al abrir y cuándo ve Guiones
    page,ctx,shot,api=B.explora(br,'Fede',{'vp':{'width':390,'height':844},'dsf':1},'prod',OUT)
    res['fede_main_txt']=page.inner_text('main')[:200]
    ctx.close()
    br.close()
B.srv.shutdown()
print(json.dumps(res,ensure_ascii=False,indent=1))
