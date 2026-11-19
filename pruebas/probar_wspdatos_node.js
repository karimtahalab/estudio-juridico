// Prueba chica en node: saca wspDatos() tal cual del index.html y simula la renovación de fondo que falla (USO 18/11: "pantalla (promesa)").
// Uso: node pruebas/probar_wspdatos_node.js <index.html>
const s=require('fs').readFileSync(process.argv[2],'utf8');
const i=s.indexOf('  var wspD=null, wspDT=0, wspDP=null;'), j=s.indexOf('  var WSP_DIAS=', i);
const code=s.slice(i,j);
let sinAtender=[]; process.on('unhandledRejection', e=>sinAtender.push(e.message));
let falla=false; const call=()=> falla ? Promise.reject(new Error('Sin conexión. Revisá internet y probá de nuevo.')) : Promise.resolve({activo:true});
const f=new Function('call', code+'; return {wspDatos, set:(t)=>{wspDT=t;}};')(call);
(async()=>{
  await f.wspDatos();            // primera carga OK
  f.set(Date.now()-6*60000);     // pasaron 6 minutos
  falla=true;
  await f.wspDatos().catch(()=>{}); // como la línea del menú 💬: devuelve lo que había y renueva atrás
  setTimeout(()=>console.log(JSON.stringify({promesas_sin_atender:sinAtender})),50);
})();
