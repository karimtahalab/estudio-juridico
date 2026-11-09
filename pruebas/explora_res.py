# -*- coding: utf-8 -*-
"""Cargar resultado desde la agenda: ¿se ve de quién es la consulta? (DATOS FALSOS)
Uso: python3 pruebas/explora_res.py <carpeta index.html> <salida> Karim,Pri,Juan"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from explora_base import *
MED = r"""()=>{const sh=document.getElementById('sheet'); const R=e=>{if(!e)return null;const r=e.getBoundingClientRect();return [Math.round(r.top),Math.round(r.bottom)]};
 const shr=sh.getBoundingClientRect();
 return {hoja_top:Math.round(shr.top), nombre:R(sh.querySelector('.sh-who h2')), contexto:R(sh.querySelector('.res-quien')), res:R(document.getElementById('resBlk')), opciones:R(sh.querySelector('#resBlk .res')), guardar:R(sh.querySelector('[data-save]')), alto:innerHeight, scroll:sh.scrollTop}}"""
out={}
with sync_playwright() as pw:
    b=pw.chromium.launch()
    VPS=[{'tag':'cel390','vp':{'width':390,'height':844}},{'tag':'cel360','vp':{'width':360,'height':640}}]
    if os.environ.get('CHICO'): VPS=[{'tag':'cel320','vp':{'width':320,'height':480}}]
    for vp in VPS:
        for who in ROLES:
            page,ctx,shot,api=explora(b,who,vp,vp['tag'],OUT)
            if 'agenda' not in page.eval_on_selector_all('#nav button[data-view]','bs=>bs.filter(b=>!b.hidden).map(b=>b.dataset.view)'): ctx.close(); continue
            page.click('#nav button[data-view="agenda"]'); page.wait_for_timeout(600)
            r=page.query_selector('[data-result]')
            if not r: ctx.close(); continue
            r.click(); page.wait_for_timeout(900)
            out['%s/%s'%(vp['tag'],who)]=page.evaluate(MED); shot('cargar_resultado')
            page.click('#sheet [data-res="nofirmo"]'); page.wait_for_timeout(400); shot('nofirmo')
            out['%s/%s/nofirmo'%(vp['tag'],who)]=page.evaluate(MED)
            ctx.close()
    b.close()
srv.shutdown()
print(json.dumps({'medidas':out,'errores':REPORT['errores']},ensure_ascii=False,indent=1))
