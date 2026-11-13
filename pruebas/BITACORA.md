# Bitácora de pruebas nocturnas (app de consultas)

Todo se prueba con DATOS FALSOS (`datos_falsos.py`). El banco bloquea script.google.com, googleusercontent.com y docs.google.com y responde cada fn con datos inventados. Nunca toca el motor ni las planillas reales.

Cómo correrlo: `python3 pruebas/correr.py <carpeta con index.html> <carpeta de capturas> Mica,Fran,Karim`
- Reloj del navegador fijo el jueves 05/11/2026 11:20 (hora de Mendoza), para tener consultas pasadas y por venir.
- Celulares: 390x844 (x3) y 360x640. Service worker bloqueado (así todo pasa por el banco).
- Fuente Archivo servida local (`fuentes/`, licencia OFL) porque Google Fonts no responde desde el entorno.
- Login: PIN falso 1234. Julián figura con PIN bloqueado.
- Las fn sin respuesta falsa se listan en `sin_fake` (hoy: fin2Calentar, que la pantalla ignora).
- Si la persona no tiene PIN (Pri en los datos falsos), el banco pasa por crear PIN y repetirlo.

## Estado de las mejoras
| Rama | Qué | Estado |
|---|---|---|
| mejora/2026-11-05 | Encabezado: subtítulo a todo el ancho en celular y título que no se corta en 360px; zona táctil 44px en flechas de semana, Día/Semana, "Elegir otro nombre" y "Salir" | Aplicada (en main desde el 05/11) |
| mejora/2026-11-06 | Crear PIN: el paso "Repetí el PIN" ya no muestra "Son 4 números." en rojo antes de escribir (el PIN se mandaba dos veces); "Editar" del Resumen del caso con zona táctil de 44px | Aplicada (en main desde el 06/11) |

| mejora/2026-11-06-* (cli-rep, disponibilidad, repetidos, reportes-claros, sc-lista, semana-rama, sin-contactar, tareas-reportes, ver-como) | Ramas armadas en chats con Karim | Aplicadas (en main) |
| mejora/2026-11-07 | En 360px el nombre de la consulta usa hasta 2 renglones (antes se cortaba en todas las tarjetas); Cerrar (X) de las hojas a 44px; "Cambiar" y "Ver como otra persona" del pie con zona táctil de 45px | Aplicada (en main desde el 07/11) |
| mejora/2026-11-07-reportes-sol | Registro de uso y comentarios de Sol (motor v75/v76) | Aplicada (en main desde el 07/11) |
| mejora/2026-11-08-flujo-sin-contactar | Flujo semanal: Sin contactar → primer mensaje → fase sin abrir la ficha (auto "Contacté" al volver de WhatsApp con Deshacer, sección "Falta la fase" con botones A/B/Llamada/C, barra para ir directo). Sin motor. | Aplicada (en main desde el 09/11, dentro de b1f5d7e; la rama vieja choca con main y no hace falta) |
| mejora/2026-11-08 | Pedidos colgados: las lecturas se cortan a los 35 s y se repiten solas; al volver a la app se repiten las que llevan más de 12 s en camino. Escrituras sin cambios. Sin motor. | Aplicada (en main desde el 13/11) |
| mejora/2026-11-09 | Cargar resultado: la hoja ya no esconde la hora y el nombre de la consulta (baja solo lo necesario); Confirmó/No respondió y Cargar resultado a 44 px; Bloquear con zona táctil de 44 px. Sin motor. | Aplicada (en main desde el 13/11) |
| mejora/2026-11-09-whatsapp | WhatsApp oficial, flujo Sin contactar, agenda de Juan rayada, actualización | Aplicada (en main desde el 09/11) |
| mejora/2026-11-10 | 📤 Enviar no traba la pantalla (la ventana se cierra al tocar Enviar, la fila queda "⏳ Enviando…", se puede seguir con el próximo lead) y no deja mandar dos veces al mismo lead; si falla, "📤 Reintentar" y aviso de mirar uChat si se cortó la conexión. Sin motor. | Aplicada (en main desde el 10/11, 230bb3e) |
| mejora/2026-11-10-notas-vs-sol, -zona-sol, -vercomo-sol | Zona propia de comentarios de Sol en la ficha, "Notas sobre el cliente", Ver como Sol | Aplicadas (en main desde el 10/11) |
| mejora/2026-11-11 | Menos pedidos de fondo al motor: reporte en segundo plano como mucho cada 3 min después de guardar; saveVisto solo si cambió algo; fin2Calentar recordado en el celular entre aperturas. Sin motor. | Aplicada (en main desde el 13/11) |
| mejora/2026-11-13-archivos-laboral | Laboral: un solo apartado "Documentación" con "＋ Agregar documentación" en cada consulta (actas notariales, cartas documento, etc.; intakers, Sol y la abogada de la consulta). Necesita motor (rama LABORAL con cat docs). | Aplicada (en main desde el 13/11, ee0463e; motor real v85 con CONFIG.ESTUDIOS LABORAL: [docs], también en el Index.html del motor real) |

## 2026-11-05 (primera noche)
- Armé el banco (rama pruebas-nocturnas, carpeta pruebas/).
- Roles probados: Mica (abogada), Fran (intaker), Karim (admin), Estefanía (Laboral), Juan (Tránsito). 390 y 360.
- Flujos: ingreso con PIN, cada sección del menú, abrir ficha, cargar resultado (Vino y no firmó + motivo), guardar y Deshacer, abrir lead en Agendar.
- Roto: nada. Sin errores de JavaScript ni pedidos fallidos.
- Permisos (con datos falsos): Estefanía sin Agendar; Juan sin Finanzas ni Reportes; KPIs y Equipo y PINs solo en Karim. Ojo: si el motor le manda a Juan o a Estefanía la lista completa de abogadas, la pantalla les muestra los botones de las demás personas (la pantalla esconde la fila solo cuando recibe 1 persona). Verificar con el motor.
- Problemas encontrados:
  - 360px: el título "Reportes" queda cortado por el botón de la persona; el subtítulo de Tareas/Agendar ocupa 3-4 renglones al lado de los botones.
  - Zonas táctiles chicas: flechas de semana 34x34, Día/Semana 30 de alto, chips de persona (Todas/Mica/Cele…) 32 de alto, "Elegir otro nombre" 30 de alto, "Cambiar" del pie 25 de alto.
  - Texto chico: etiquetas de la barra de abajo 11.5px, días de la semana 11-12.5px, chips de rama 12px.
- Mejoras propuestas: mejora/2026-11-05 (ver tabla).
- Ideas grandes para más adelante:
  - Chips de persona y de fase a 40-44px de alto (cambia un poco el diseño, por eso no lo hice solo).
  - Barra de abajo con etiquetas de 12.5-13px.
- Pendiente del banco: respuestas falsas más completas para getReporte, getFinanzas/getFin2 y getCreativos (hoy los reportes muestran "No hay planillas"), y flujos de agendar, bloquear y derivar.

## 2026-11-06
- mejora/2026-11-05 ya está en main: marcada como aplicada.
- Banco: ahora sigue el flujo de crear PIN (Pri) y responde getEstudios (lista vacía). Funciones nuevas en main sin respuesta falsa todavía: getRitmo, noRepetido, saveTraslado, trasladoAccion, trasladoRecibo, verRecibo, subirEstudio, verEstudio, borrarEstudio, getFin2, getFin2Panel, saveFin2 (no se llamaron en los flujos de hoy).
- Roles probados: Sol, Pri (intaker, crea PIN), Juan (Tránsito), Estefanía (Laboral). Regresión de la rama con Mica, Fran y Karim. 390 y 360.
- Roto: nada de JavaScript. Permisos OK con datos falsos (Estefanía sin Agendar; Juan solo Tránsito; nadie fuera de Karim con Reportes completos).
- Problema encontrado (confuso): al crear el PIN por primera vez (o después de un reseteo), apenas pasa al paso "Repetí el PIN" aparece "Son 4 números." en rojo, antes de escribir nada. Causa: dos listeners de input mandaban el PIN; el segundo leía el campo vacío del paso 2. Afecta a todos los que entran por primera vez o después de que Karim les resetea el PIN.
- Sigue chico: "Editar" del Resumen del caso 52x32; botones de confirmación 144x42; "Cerrar" de la hoja 40x40; "Cambiar" del pie 59x25; chips de persona 32 de alto.
- Mejoras propuestas: mejora/2026-11-06 (ver tabla).
- Ideas grandes:
  - Sol tiene rol de control (deja comentarios a intakers) y hoy entra con la misma vista que una abogada: un acceso directo a "comentar al intaker" desde la ficha le ahorraría pasos.
    - Karim (06/11): el botón va SOLO para Sol. Necesita un permiso nuevo en el motor (Apps Script) que se mande solo a Sol; la pantalla muestra el botón únicamente si llega ese permiso. Pendiente de pedir en un chat.
    - Cómo lo quiere Karim: le llega al intaker como tarea en Tareas, en un grupo "Comentarios de Sol". El intaker la marca como hecha y el aviso desaparece (y baja el número de Tareas).
    - Le llega a los dos intakers (Fran y Pri), sin importar quién agendó el lead.
    - Si uno toca "Listo", desaparece para los dos.
  - Chips de persona/rama a 40-44px de alto (sigue pendiente de la noche anterior).

## 2026-11-07
- mejora/2026-11-06 y todas las mejora/2026-11-06-* ya están en main: marcadas como aplicadas. No quedaban ramas pendientes.
- Roles probados: Cele (abogada), Fran (intaker), Karim (admin) con el banco completo; Estefanía, Sol y Juan para permisos; Pri (agendar un lead sin día hasta guardar, buscar); Julián (PIN bloqueado); Mica (PIN mal). 390 y 360.
- Banco: nuevos `explora_base.py` (arranque reutilizable), `explora1.py` (agendar hasta guardar, buscar, Juan), `explora2.py` (PIN bloqueado y PIN mal) y `antes_despues.py` (mide nombres cortados, Cerrar y pie). Funciones nuevas en main sin respuesta falsa: getLead, levantarLead, resolverRepFin2 (no se llamaron hoy).
- Roto: nada. Sin errores de JavaScript ni pedidos fallidos. Permisos OK con datos falsos (Estefanía solo Agenda y Falta cargar; Juan sin ART/Laboral ni Reportes; Reportes completos y Equipo y PINs solo admins).
- PIN bloqueado y PIN mal: mensaje claro, el campo se vacía y queda con foco. Bien.
- Agendar un lead sin día: 3 toques (Agendar, horario, guardar) y aviso "📅 Agendada…". Bien.
- Problemas encontrados:
  - 360px: el nombre de TODAS las consultas de la agenda se cortaba ("Rubén Prueba …", "Lucía Demo O…") porque iba en un solo renglón al lado de los botones de llamar y WhatsApp. También en la búsqueda.
  - Cerrar (X) de las hojas 40x40. "Cambiar" del pie 59x25.
  - Menor: al entrar, el aviso "Usás la app como …" tapa 2-3 segundos los botones Llamar/WhatsApp de la próxima consulta en 360px.
  - Menor: en "Cargar a alguien nuevo" (360x640) el botón fijo "Elegir día y horario" tapa el campo de Email mientras se completa.
- Mejoras propuestas: mejora/2026-11-07 (ver tabla).
- Ideas grandes:
  - Agenda en 360x640: la tarjeta de la próxima consulta queda con Llamar/WhatsApp debajo de la barra de abajo. Achicar o plegar "Marcar mi disponibilidad" cuando ya está configurada subiría la tarjeta ~70px.
  - Chips de persona/rama a 40-44px de alto (sigue pendiente).

## 2026-11-07 (chat con Karim) — entorno de prueba, reportes del equipo y comentarios de Sol
- Karim pidió apuntar más alto, con una condición: no romper nada de lo que ya anda; todo con planillas de prueba.
- Entorno de prueba en Drive: carpeta "App Consultas – ENTORNO DE PRUEBA (no usar con el equipo)" (1EzKcc0PPI9AajvuX6_DbknUeQrcQJEqm), con copia del motor (1QmoHClNDfh4JzOfDGzBfu6X59Nm0CDqKLiCs52FyEIyTaQh2O2W_jG20) que apunta solo a copias de las 10 planillas que la app escribe. Los creativos y los KPIs se leen de las reales (solo lectura). PIN de prueba para todos: lo deja PRUEBA_prepararEntorno.
- Cambios del motor pendientes: carpeta 1WZPoPIF_DJN0N8l4L3NXNjrQF5Cqov7E, un JSON por rama con pares buscar/reemplazar.
- Rama mejora/2026-11-07-reportes-sol (pantalla) + mejora-2026-11-07-reportes-sol.json (motor):
  - "Algo no anda o tengo una idea" (pie y ¿Quién sos?) → REPORTES de la planilla de reportes.
  - Registro de uso agrupado cada 10 min y al salir (resumen de pedidos, lentos >4 s, avisos, errores, tiempo de apertura) → USO.
  - Comentarios de Sol: botón solo para Sol en la ficha; les llega a Fran y Pri en Tareas ("Comentarios de Sol"), cualquiera marca ✔ Hecho, baja el número de Tareas.
  - Reporte semanal: repPend_ arma el lead completo solo de las filas de la semana (mismo resultado, menos trabajo).
- Pruebas: pruebas/probar_reportes_sol.py → 22/22 OK, sin errores. correr.py con Mica, Fran, Karim, Sol y Juan: 0 errores en main y en la rama, mismas pestañas, sin scroll horizontal nuevo.
- Nota del banco: con service_workers='block', un visibilitychange con document.hidden=false hace fallar r.update() del service worker (solo en el banco). Para simular salir de la app, poner visibilityState y hidden juntos.
- Tareas programadas: la nocturna ahora lee REPORTES/USO reales y puede proponer cambios del motor como JSON; nueva tarea semanal (domingos 16:47) que rediseña un flujo completo.
- 07/11 23:55: Karim no quiere el botón "Algo no anda o tengo una idea": se sacó de la rama y del motor (queda solo el registro de uso, que no lo ve nadie en la app; planilla "Registro de uso de la app", pestaña USO). Prueba 17/17 OK; correr.py igual que main.
- 07/11 00:22: APLICADO en la app real con el ok de Karim. Antes: PRUEBA_probarNuevas en la copia, todo OK (Sol comenta, a Pri le llega, Mica no puede, Pri marca Hecho, a Fran ya no le aparece, registro de uso guardado). Motor real v75 publicado (mismo ID de implementación); pantalla en main 788c0ad (cache consultas-20261107002234). Registro de uso real: "App Consultas – Registro de uso de la app" (1pEQAQseAj0l0KOLB4JD1qKaJBXKgSRznfmZnFZNOzNI).
- Medición honesta del reporte en la copia: armado de cero tarda ~1,9 s (2,1 s con control de KPIs); casi todo es leer HISTORIAL/CARGA SEMANAL/KPIs (1,9 s). repPend_ bajó la búsqueda de pendientes de 20 ms a 1 ms: mismo resultado, diferencia imperceptible.
- Aviso: otra conversación (envío de WhatsApp, Wsp.gs) también edita la copia del motor. Una vez guardó con una versión vieja abierta y pisó cambios; se volvieron a aplicar sin tocar Wsp.gs. Recargar el editor antes de guardar.
- 07/11 00:55: CONTEO DEL REPORTE SEMANAL CORREGIDO (motor v76, con el ok de Karim: "si arreglalo"). Problema: Laboral 2-8/11 mostraba 7 "vinieron y no firmaron" y la agenda tiene 4. Los 3 de más eran C puestos por intakers a agendados que no vinieron (Brenda Ramirez y Nahuel Paredes el 5/11, Juan Pablo Avendaño el 4/11 antes de su turno); además Celia Crespo (BC, pidió reagendar) contaba como no show.
  - Regla nueva desde el 4/11/2026 (cuando empezaron los resultados desde la app): un C después de un turno cuenta como "vino y no era caso" solo si la abogada lo cargó como resultado en la app; un C o BC que pone un intaker a un agendado no cuenta como que vino ni como no show. Antes del 4/11 sigue la regla vieja (igual que la planilla de KPIs).
  - La app marca cada resultado en la columna M del HISTORIAL ("Resultado cargado en la app": "Resultado app: No era caso (Mica)"); el script de KPIs lee hasta la L. Corrección del mismo día: misma línea, marca nueva. Deshacer: borra la línea.
  - Pruebas: probar_conteo_reporte.js con el HISTORIAL real de Laboral → 2/11: 5 firmaron, 4 vinieron y no firmaron, 0 no show, 1 reagendó (Juan Pablo); 26/10 sin cambios. En la copia del motor, PRUEBA_probarV76: mismo resultado con getReporte; "No es caso" desde la app deja la marca y cuenta; corregir a "No firmó" actualiza la misma línea; Deshacer deja el HISTORIAL como estaba.
  - Real: v76 publicado (mismo ID de implementación), código guardado verificado contra el local, la API responde. Pantalla sin cambios.
  - Pendiente con Karim: Maria Cecilia (ART, turno 5/11 15:30 con Mica, "no era caso" en la agenda) se cargó antes de la marca y ya no cuenta como que vino; se puede marcar a mano su línea del HISTORIAL de ART. La planilla de KPIs sigue con la regla vieja (Laboral 2/11 da 7 ahí).
- 07/11 01:11: KPIs CON LA MISMA REGLA QUE LA APP (ok de Karim: "si que app y kpis cuenten con misma regla"). La planilla "KPIs Semanales – Legal (vigente)" (script "Kpis Automaticos") tenía la misma regla vieja: Laboral 2-8/11 daba 7 vinieron y no firmaron, Celia como no show y Juan Pablo como "reagendado que terminó viniendo".
  - Cambio en consultasDeRama_ (6 pares, iguales a los del motor v76) y lectura del HISTORIAL hasta la columna M. "Pases a C de leads viejos" no cambia (antes del 4/11 sigue igual; después, los C de intakers a agendados no suman en ningún lado).
  - Prueba antes de guardar, en el navegador con el código real: la versión vieja reproduce DATA_CONSULTAS tal cual (26/10 y 2/11); la nueva da Laboral 2/11 = 5 firmaron, 4 no firmaron, 1 reagendó, 0 no show; con marca en la columna M cuenta como "no era caso".
  - Guardado (verificado al recargar el editor) y "actualizar" corrido a mano a la 01:11 (es lo que corre el disparador cada hora). Resultado en la planilla: Laboral NOV 02-08 → consultas 10, firmaron 5, vinieron y no firmaron 4, no show 0, pidieron reagendar 1, reagendados que vinieron 0. ART y Tránsito coinciden con la app.
  - Maria Cecilia (ART): marcada a mano en HISTORIAL de ART, fila 408, columna M ("Vino y no era caso (marcado a mano el 07/11 según la agenda...)"), y encabezado M1 "Resultado cargado en la app". Ahora cuenta como "no era caso" en la app y en KPIs.
  - Copia de los pares: Drive, carpeta "Cambios del motor pendientes", "APLICADO KPIs (07-11) - misma-regla-que-la-app.json".

## 2026-11-08 (domingo)
- mejora/2026-11-07 y mejora/2026-11-07-reportes-sol ya están en main: marcadas como aplicadas. No había ramas pendientes.
- Registro de uso real (USO, 06/11 y 07/11; solo usaron la app Karim y Fran, nada el 08/11 hasta la noche):
  - Pedidos colgados: getFin2 de Karim esperó 1.081.694 ms (18 min) y terminó en "Sin conexión" (Finanzas). getData de Fran 2 veces "Sin conexión" tras ~6 s (Tareas). Causa en la pantalla: call1 no tenía tiempo máximo; mientras getData está en camino, load() no vuelve a pedir (state.busy), así que un pedido colgado frenaba todas las actualizaciones y Finanzas quedaba en "cargando" (f2Load no repite si hay uno cargando).
  - getData lento seguido: 4-14 s (Karim 14 s en Agenda, Fran 10-11 s en Tareas/Agendar). Es del motor.
  - fin2Calentar 43-47 s (la pantalla no lo espera). cambiarFase 4-6 s (la pantalla ya lo muestra al instante). getCreativos 8 s una vez.
  - 1 aviso de PIN de finanzas incorrecto (Karim). Sin errores de pantalla.
- Roles probados: Juan, Estefanía, Sol, Pri (crea PIN) en 390 y 360; regresión con Mica, Fran y Karim. Sin errores de JavaScript ni pedidos fallidos en main ni en la rama. Mismas pestañas por rol. Permisos OK con datos falsos.
- Nuevo en el banco: pruebas/probar_colgados.py (A: Actualizar con getData colgado, sale y vuelve a los 15 s; B: se queda mirando 40 s; C: cargar resultado con el servidor que no contesta 65 s). main: A y B quedan girando para siempre. Rama: A y B se recuperan solos (2 pedidos de getData), C manda saveAction una sola vez (las escrituras no se cortan).
- Nota del banco: el audit marca "Cambiar" del pie 59x25 pero tiene zona táctil extendida con ::after (ok). Las diferencias de captura main/rama son de animaciones (fondo de hoja, puntos del PIN).
- Mejora propuesta: mejora/2026-11-08 (ver tabla). Sin cambios de motor.
- Ideas grandes:
  - getData tarda 4-14 s y se pide en cada Actualizar y al volver a la app: que el motor guarde la respuesta armada 30-60 s en CacheService por persona y la invalide al guardar (pares en un JSON de "Cambios del motor pendientes", a medir primero en la copia).
  - Agenda en 360x640: plegar "Marcar mi disponibilidad" a una línea en pantallas bajas (sube la próxima consulta ~35 px). Sigue pendiente lo de los chips a 40-44 px.

## 2026-11-09 (lunes, madrugada)
- Ramas sin mergear: mejora/2026-11-08 y mejora/2026-11-08-flujo-sin-contactar (2, así que hubo lugar para una nueva). Cambios del motor pendientes: ninguno (los 3 archivos de la carpeta dicen APLICADO).
- Registro de uso real: no hay filas nuevas desde el 07/11 (nadie usó la app el 08/11 ni hasta esta corrida). Lo del 06-07/11 ya se analizó el 08/11. Dato que quedó: Fran pide getReporte (3-5 s) en segundo plano después de cada cambio de fase (~25 veces el 07/11), porque cada escritura invalida el reporte y el próximo getData lo vuelve a precargar. No traba la pantalla; es carga extra del motor.
- Roles probados: Cele (abogada), Pri (intaker, crea PIN), Karim (admin), Juan (Tránsito), Estefanía y Sol. 390 y 360 (y 320x480 para el flujo de resultado). Sin errores de JavaScript ni pedidos fallidos en main ni en la rama. Mismas pestañas por rol. Permisos OK con datos falsos (Estefanía solo Agenda y Falta cargar; Juan sin Reportes ni Tareas; Reportes completos solo Karim).
- Problema encontrado (confuso): "Cargar resultado" abre la ficha y la baja 155 px hasta "¿Qué pasó en la consulta?": la hora y el nombre quedan arriba, fuera de la pantalla (en 390 y 360, todos los roles). Se puede cargar Firmó/No vino sin ver de quién es. Las opciones y Guardar entran sin bajar (390, 360 y 320x480).
- Chicos que quedaban: Confirmó/No respondió 42 de alto (tarea de todos los días de intakers), Cargar resultado 42, Bloquear 34.
- Mejora propuesta: mejora/2026-11-09 (ver tabla). Banco: nuevo pruebas/explora_res.py (mide nombre, opciones y Guardar al cargar resultado; CHICO=1 prueba 320x480). main: nombre en -85/-71 px (escondido); rama: nombre visible (70-84 px), opciones y Guardar visibles, sin bajar.
- Ideas grandes:
  - Reporte en segundo plano: después de una escritura, volver a pedir getReporte recién al abrir la pestaña o 1 vez cada 2-3 min, en vez de tras cada getData (le saca al motor ~25 pedidos de 4 s por día de Fran). Ojo: la pestaña Reporte tardaría 3-5 s la primera vez después de cambiar algo.
  - Sigue pendiente lo de getData en CacheService (motor) y plegar "Marcar mi disponibilidad" en pantallas bajas.

## 2026-11-09 (noche, corrida del 10/11 01:40 UTC)
- main al día: b1f5d7e, 6d80fbb, 1953419 y después 2a8119d (cuánto tiempo trabajó), 0c2f104 (recordatorios 1º/2º/3º) y 9af5295 (Viene a firmar: agendar). Copiados al banco (la rama pruebas-nocturnas no comparte historia con main: se copian index.html, sw.js y manifest).
- Ramas pendientes: mejora/2026-11-08 y mejora/2026-11-09 entran limpias sobre main (probado sin pushear, también juntas con la nueva). mejora/2026-11-08-flujo-sin-contactar choca con main pero ya está adentro (b1f5d7e). mejora/2026-11-05 figura con commits de más pero su contenido está en main.
- Registro de uso real (USO, 7-9/11, 846 filas; usaron la app Pri, Fran, Karim, Cele y Mica; nada de Estefanía, Juan ni Julián):
  - Sin filas de error. 8 avisos "Sin conexión" (getData 5, getFin2 2, fin2Calentar 1) después de esperas enormes: getData 201 s (Fran, iPhone) y 100 s (Karim), getFin2 277 s. Es lo que arregla mejora/2026-11-08 (pendiente).
  - enviarWsp: 38 envíos (Pri 33, Fran 5), 0 errores, promedio 7 s, máximo 24 s. wspDatos 42 (3,4 s). wspVista/wspOpciones no se usaron (todo se arma con wspDatos).
  - getData 669 pedidos, promedio 3,9 s (139 de más de 4 s). getReporte 128 (4,1 s) en segundo plano. cambiarFase 75 (4,6 s, la pantalla no espera). fin2Calentar 18 (hasta 45 s; también lo disparan Cele y Mica, que tienen finAcceso; la pantalla no lo espera).
  - Aperturas: con datos guardados <1,2 s; con datos nuevos 3-8 s (Cele iPhone hasta 12,7 s).
  - Permisos: finanzas y reintegros solo los usó Karim. Nada raro.
- Banco: datos_falsos.py ahora responde wspDatos (catálogo y textos inventados) y enviarWsp (ok falso, registra en consola a quién y qué plantilla; marca el lead como hace el motor). wspVista/wspOpciones devuelven error (la pantalla no los usa si hay wspDatos). Todo lo externo (graph.facebook.com, uChat, etc.) se aborta. Nuevos: probar_wsp.py (servidor lento: retiene enviarWsp y lo contesta después; también con falla) y probar_wsp_cancelar.py (toques reales).
- Roles probados: Mica (abogada), Fran (intaker), Karim (admin), Juan (Tránsito) con correr.py en 390 y 360; Pri (intaker) con el flujo de WhatsApp. Sin errores de JavaScript ni pedidos fallidos. Mismas pestañas por rol. Permisos OK con datos falsos.
- ROTO (riesgo de mandar dos veces): en main, mientras 📤 Enviar dice "Enviando…" (7-24 s), Cancelar sigue activo. Si se toca, la ventana se cierra, el mensaje sale igual y la fila vuelve a "📤 Enviar" hasta que contesta el servidor: con un segundo toque salen 2 enviarWsp al mismo lead (banco: ['P072','P072']). Si el motor no frena el segundo (los dos llegan antes de que se anote el primero), el lead recibe el mensaje dos veces. Además, durante esos segundos no se puede hacer nada más.
- Mejora propuesta: mejora/2026-11-10 (ver tabla). Banco: main → ventana tapando todo, no se puede seguir, 2 envíos al mismo lead; rama → ventana cerrada al instante, segundo lead mandado sin esperar, fila del primero "⏳ Enviando…" deshabilitada, 1 envío por lead; con falla: "📤 Reintentar" en la fila y aviso. correr.py en la rama: igual que main (0 errores, mismas pestañas, sin elementos chicos nuevos ni scroll horizontal).
- Sigue chico (ya anotado): chips de persona/rama 32 px, Editar del resumen 52x32, Día/Semana 30 px y flechas 34 px en la agenda de Juan.
- Ideas grandes:
  - fin2Calentar se dispara para todos los que tienen finAcceso (también Cele y Mica) y tarda 15-45 s en el motor cada 40 min: limitarlo a quien abre Finanzas o a admins le saca carga al motor (es del motor y de la pantalla; a medir).
  - getReporte en segundo plano 128 veces en un día (4 s cada uno): pedirlo al abrir Reporte o cada 2-3 min (sigue pendiente de la noche anterior), junto con getData en CacheService.

## 2026-11-10 (noche, corrida del 11/11)
- main al día: 08566c6 (incluye mejora/2026-11-10 y las tres ramas de Sol del 10/11). Copiados al banco index.html, sw.js y manifest.
- Ramas pendientes: mejora/2026-11-08 y mejora/2026-11-09 entran limpias sobre main (cada una y juntas con la nueva, sin pushear). mejora/2026-11-05, mejora/2026-11-06 y mejora/2026-11-08-flujo-sin-contactar figuran con commits de más pero su contenido ya está en main. Con la nueva quedan 3 pendientes: la próxima noche no se arma rama nueva si no se aprueba alguna.
- Cambios del motor pendientes: ninguno (los 3 archivos dicen APLICADO).
- Registro de uso real (USO, 9-10/11, 772 filas; usaron la app Pri, Fran, Karim y Mica; nada de Cele, Sol, Estefanía, Juan ni Julián):
  - Sin filas de error. 2 avisos (9/11): un "Sin conexión" de getData de Fran y un PIN de finanzas incorrecto de Karim. El 10/11 ningún "Sin conexión".
  - enviarWsp 29 envíos el 10/11, 0 errores, promedio 5,3 s, máximo 10,8 s (Pri).
  - getData 474 (3,5 s promedio, máximo 20 s de Pri). getReporte 70 (4 s) en segundo plano. saveVisto 87 (2,1 s, máximo 9,7 s). cambiarFase 38 (4,9 s, la pantalla no espera). fin2Calentar 17 (24 s promedio, máximo 64 s; 11 de Karim, que abrió la app muchas veces en Windows y iPhone).
  - Aperturas: con lo guardado 0,2-1,8 s; con datos nuevos 1,7-13 s (Pri en Windows 13,2 s una vez).
  - Pri y Fran usan la app instalada en Windows (1280x646), no solo en el celular.
- Roles probados: Cele, Pri, Karim con correr.py; Sol, Estefanía y Juan para permisos. 390 y 360. Sin errores de JavaScript ni pedidos fallidos en main ni en la rama. Mismas pestañas por rol. Permisos OK con datos falsos.
- Comentarios de Sol de punta a punta (nuevo pruebas/probar_sol.py): Sol ve la zona y el botón, manda; a Pri le llega en Tareas, ✔ Hecho y desaparece; Mica no ve el botón. 7/7 OK.
- Banco: datos_falsos.py ahora tiene a Sol en ABOGADAS (como CONFIG.ABOGADAS del motor; sin eso la agenda de Sol salía vacía y sin chip marcado, solo en el banco), permiso comentar para Sol, pedirInterna tipo control que guarda el comentario, responderInterna que lo cierra y devuelve el lead, y paraMi para intakers. Nuevo pruebas/probar_fondo.py (cuenta pedidos de fondo).
- Mejora propuesta: mejora/2026-11-11 (ver tabla). probar_fondo.py: Pri con 4 cambios de fase + Actualizar + 3 fichas → getReporte 2→0 y saveVisto 3→0; al tocar Reporte se ve y pide uno nuevo (1); ficha con novedad guarda el visto (1 en main y en la rama); Karim 4 aperturas en 10 min → fin2Calentar 4→1. correr.py igual que main (0 errores, mismas pestañas; 124→106 pedidos al banco).
- Ideas grandes:
  - getData sigue en 3,5 s de promedio y es lo que más espera la gente: guardarla armada 30-60 s en CacheService por persona e invalidarla al guardar (motor; medir primero en el entorno de prueba). Sigue pendiente.
  - Pri y Fran trabajan en Windows: una vista de escritorio de Tareas/Agendar a dos columnas (lista + ficha al lado) les ahorraría abrir y cerrar la ficha en cada lead.

## 2026-11-11 (noche, corrida de las 22:40)
- main al día: b3914ad (Seguimiento entre intakers 18967c0/e8ad86b/1f1d9e5, Traslados b3914ad, rechazo Laboral 08566c6). Copiados al banco index.html, sw.js y manifest.
- Ramas pendientes sin mergear: mejora/2026-11-08, mejora/2026-11-09 y mejora/2026-11-11 (3). Las tres entran limpias sobre main (cada una y juntas, sin pushear). mejora/2026-11-08-flujo-sin-contactar choca en index.html pero su contenido ya está en main (b1f5d7e); mejora/2026-11-06-repetidos tampoco mergea limpio (2 commits del 06/11, ya superados). Con 3 pendientes, esta noche NO se armó rama nueva.
- Cambios del motor pendientes: ninguno (los 3 archivos dicen APLICADO).
- Registro de uso real (USO, 10/11 noche y 11/11, ~810 filas; usaron la app Pri, Fran, Karim, Cele, Mica y Juan; nada de Sol, Estefanía ni Julián):
  - Sin filas de error. Pedidos colgados otra vez, peores que antes: getData de Cele esperó 5.662.553 ms (94 min) y 2.990.384 ms (50 min) y terminó en "Sin conexión" (iPhone, agenda); otro de 171 s. fin2Calentar de Karim 1.227.609, 1.078.021 y 1.049.574 ms (17-20 min, 3 veces). Pri getData 47 s y getReporte 41 s. Juan 2 "Sin conexión" de getData tras 20-23 s. Es exactamente lo que arregla mejora/2026-11-08 (tiempo máximo por pedido): probar_colgados.py sobre main + las 3 ramas → A y B se recuperan solos (2 getData); main sigue girando para siempre.
  - verEstudio (abrir un estudio del lead, nuevo) lento y repetido: Juan 9-13 s cada vez (6 aperturas), Karim hasta 15,7 s, Cele 4-6 s (11 aperturas en 2 tandas, "agenda > lead"). La pantalla no guarda el archivo: cada vez que se abre el mismo estudio lo vuelve a bajar entero en base64.
  - enviarWsp ~40 envíos (Pri y Fran), 0 errores; 1 aviso "Este lead no tiene nombre cargado." (Pri, Windows): la pantalla deja tocar 📤 Enviar y el motor lo frena.
  - Seguimiento ya se usa: segGuardar, segComentar (5-7,5 s), segHecho; subirEstudio hasta 16,6 s (Pri).
  - getData sigue en 2-9 s (promedio ~3,5 s). Aperturas con datos nuevos 2-9,5 s; Juan 18,9 s una vez.
  - Juan (iPhone) dispara fin2Calentar y getCreativos: el motor le da finAcceso. A confirmar que finRamas sea solo Tránsito (no se bajó el motor; con datos falsos no se puede ver).
- Banco: datos_falsos.py ahora tiene Seguimiento (permiso seguimiento para Fran, Pri, Sol, Karim y Julián; 5 notas: para hoy, atrasada sin nombre, repetir cada semana, sin fecha, hecha) y responde segGuardar/segHecho/segComentar como el motor (repetir: Hecho corre 7 días), getEstudios con un estudio y verEstudio con un PDF falso. Nuevo pruebas/probar_seguimiento.py.
  - Nota del banco: "Cannot read properties of undefined (reading 'update')" en probar_colgados.py sale porque el banco bloquea service workers (register devuelve undefined); en el celular no pasa.
- Roles probados: Juan, Estefanía, Sol y Fran con correr.py (390 y 360): 0 errores de JavaScript, 0 fn sin respuesta falsa, mismas pestañas por rol. Permisos OK con datos falsos (Estefanía solo Agenda y Falta cargar; Juan sin Reportes, Tareas ni Seguimiento).
- Seguimiento de punta a punta (probar_seguimiento.py, Fran 390 y 360): aviso en Tareas, ✔ Hecho + Deshacer, comentario, nota nueva con teclado de teléfono y fecha nativa, repetir cada semana, buscador sin perder el foco: todo OK. Lo ven Fran, Pri, Sol (pestaña) y Karim (desde el aviso de Tareas); no lo ven Mica, Estefanía ni Juan.
- Problemas encontrados (sin rama, por el tope de 3 pendientes):
  - El título "Seguimiento" se corta a mitad de palabra en el celular ("Seguimient/o" en 390, "Seguimie/nto" en 360).
  - En Seguimiento, una nota sin nombre muestra el teléfono pegado (2615550102) en vez de con formato; "✔ Hecho" mide 84x40.
  - Abrir el mismo estudio dos veces lo baja dos veces (9-15 s cada vez para Juan y Karim).
- Para la próxima rama (cuando se apruebe alguna): guardar en memoria el estudio ya abierto (por fid) para que la segunda vez abra al instante; título de Seguimiento que entre en una línea; formato del teléfono en notas sin nombre.
- Ideas grandes:
  - verEstudio: que el motor devuelva un link de vista de Drive (o un PDF ya achicado) en vez del archivo entero en base64; en iPhone además el PDF dentro de la app puede mostrar solo la primera página.
  - Sigue pendiente getData en CacheService (motor) y limitar fin2Calentar a quien abre Finanzas.

## 2026-11-12 (noche, corrida del 13/11)
- main sin cambios desde b3914ad (11/11 23:02 UTC). El banco ya tenía index.html, sw.js y manifest iguales a main.
- Ramas pendientes: mejora/2026-11-08, mejora/2026-11-09 y mejora/2026-11-11 siguen sin mergear; las tres entran limpias sobre main (cada una y juntas, sin pushear). Con 3 pendientes, esta noche NO se armó rama nueva.
- Cambios del motor pendientes: ninguno (los 3 archivos dicen APLICADO).
- Registro de uso real (USO, 12/11, filas ~2444-2880; usaron la app Pri, Fran, Karim, Cele y Juan; nada de Mica, Sol, Estefanía ni Julián):
  - Sin filas de error y, por primera vez en varios días, ningún "Sin conexión" ni pedido colgado de minutos. 1 aviso: PIN de finanzas incorrecto (Karim).
  - getData sigue lento: la mayoría 2-5 s, picos de 18,8 y 18,1 s (Pri), 15,5 s (Pri), 13,2 s (Fran y Karim), 9,9 s (Cele). Es del motor (idea de CacheService, pendiente).
  - enviarWsp ~35 envíos (Pri y Fran), 0 errores, 4-11,7 s. wspDatos hasta 12 s (Pri).
  - Karim: fin2Calentar 37 s, 24 s y 19 s; getFin2Panel 16 s; getFin2 4,5-11 s. Lo de fin2Calentar lo baja mejora/2026-11-11 (pendiente).
  - Aperturas con datos nuevos: Cele 11,4 s y 5,8 s (iPhone), Karim 2,5-4,6 s, Pri 4 s. Con lo guardado 0,3-1,5 s.
  - Juan dispara fin2Calentar: revisado en el Código.gs del motor real (solo lectura): Juan tiene fin ['TRANSITO'], así que solo abre Finanzas de Tránsito. Permisos OK; queda cerrada la duda del 11/11.
- Banco: PERMISOS de datos_falsos.py ahora copia CONFIG.EQUIPO del motor real v77: Mica, Cele y Juan sin leads (no ven Agendar; antes el banco se lo mostraba), Sol con leads de las 3 ramas y Finanzas solo para cargar clientes de ART, Mica/Cele/Juan con Finanzas y Guiones de sus ramas. Así el banco muestra las mismas pestañas que ve cada uno de verdad.
- Roles probados con correr.py (390 y 360): Mica, Cele, Juan, Sol, Estefanía, Pri (crea PIN) y Karim. 0 errores de JavaScript, 0 pedidos fallidos, sin scroll horizontal. Pestañas: abogadas de Reclamá → Agenda, Falta cargar, Finanzas, Guiones; Juan → lo mismo con su agenda de Tránsito; Estefanía → Agenda y Falta cargar; Sol → Agenda, Seguimiento, Agendar, Falta cargar y Finanzas; Pri → Reporte, Agenda, Tareas, Seguimiento, Agendar; Karim → todo.
- Sin problemas nuevos. Siguen chicos (ya anotados): Bloquear 34 de alto, chips de persona 32, Día/Semana 30, flechas 34, Editar 52x32, Confirmó/No respondió 42 (los arregla en parte mejora/2026-11-09).
- Para la próxima rama (cuando se apruebe alguna): sigue lo del 11/11 (estudio ya abierto en memoria, título de Seguimiento, teléfono con formato en notas sin nombre).
- Pendiente del banco: respuestas falsas para Traslados (saveTraslado, trasladoAccion, trasladoRecibo, verRecibo) para probar el bloque nuevo de b3914ad.

## Flujos rediseñados (tarea semanal de los domingos)
| Fecha | Flujo | Para quién | Toques antes → después | Rama | Motor |
|---|---|---|---|---|---|
| 2026-11-08 | Sin contactar → primer mensaje → Contacté → fase | Intakers (Fran, Pri) | 13 → 8 (2 leads, con navegación); por lead: 5 → 2 si contesta enseguida, 7 → 1-3 si contesta después. Hojas 2 → 0, scroll ~2.000 px → 0-360 px | mejora/2026-11-08-flujo-sin-contactar | Solo pantalla |

### 2026-11-08 — Sin contactar (intakers)
- Por qué este: en USO (06-07/11) lo que más se repite de Fran es cambiarFase y editarDatos desde "tareas > ficha" y "agendar > ficha" (12 cambiarFase, 4-6 s cada uno, la pantalla ya lo muestra al instante) y levantarLead 5 veces. Es la primera semana de la tarea: no hay flujos repetidos.
- Antes (banco, Fran, 390 y 360): "Sin contactar" está al fondo de Tareas (~1.400-1.500 px de scroll). Para clasificar: ficha → Cambiar fase → fase → cerrar. Si toca "✓ Contacté" (sin Deshacer) el lead desaparece de Tareas y cuando contesta hay que buscarlo en Agendar. 13 toques, 2 hojas, ~2.000 px de scroll, 6 pedidos.
- Después: barra "📨 N leads sin contactar · M sin fase · Ver ›" arriba de Tareas; al volver de WhatsApp (4 s o más afuera) queda marcado solo con Deshacer (el pedido sale a los 10 s o al salir de la app); sección nueva "Falta la fase" (sin fase, ya con nombre de intaker, últimos 7 días) con A/B/Llamada/C/Otra en la fila; después de elegir queda "✓ Quedó en X" con Agendar. Si elige fase con el Contacté pendiente, no manda levantarLead (cambiarFase ya deja el nombre). 8 toques, 0 hojas, 0-360 px, 4 pedidos.
- Banco: datos_falsos.py ahora tiene sinContactar (6 leads) y levantarLead; cambiarFase de un intaker deja su nombre (como anotarIntaker_). Nuevos flujo_sc.py (antes/después), flujo_sc_util.py y probar_sin_contactar.py (17/17: vuelve a los 2 s no marca, Deshacer no manda, ✓ sale a los 10 s o al salir, fase + Deshacer, Otra abre la ficha, error del motor vuelve a Sin contactar, Karim sin cambios).
- Regresión correr.py (Mica, Fran, Karim, Sol, Juan, Estefanía; 390 y 360): sin errores en main ni en la rama, mismas pestañas por rol, sin scroll horizontal nuevo.
- Para más adelante: el envío de plantillas por la API de WhatsApp (Wsp.gs, en otra conversación) encaja acá: el "Primer mensaje" se mandaría desde la misma fila y levantarLead ya se llama solo.
