def afuera(page, seg):
    """Simula salir de la app (a WhatsApp) unos segundos y volver."""
    for p in page.context.pages[1:]:
        try: p.close()
        except Exception: pass
    page.evaluate("""()=>{Object.defineProperty(document,'visibilityState',{value:'hidden',configurable:true});Object.defineProperty(document,'hidden',{value:true,configurable:true});document.dispatchEvent(new Event('visibilitychange'));window.dispatchEvent(new Event('blur'));}""")
    page.clock.run_for(seg * 1000); page.wait_for_timeout(200)
    page.evaluate("""()=>{Object.defineProperty(document,'visibilityState',{value:'visible',configurable:true});Object.defineProperty(document,'hidden',{value:false,configurable:true});document.dispatchEvent(new Event('visibilitychange'));window.dispatchEvent(new Event('focus'));}""")
    page.wait_for_timeout(800)
