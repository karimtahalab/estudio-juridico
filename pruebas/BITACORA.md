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
| mejora/2026-11-13-disp-admin | Administración (Karim, Julián): con "Todas" en la Agenda, "Cargar disponibilidad de…" con un botón por persona que abre su editor. Sin motor (saveDisponibilidad ya acepta admin). | Aplicada (en main desde el 13/11, 166e684) |
| mejora/2026-11-14 | Título de arriba que se achica en vez de cortarse ("Seguimient/o"); estudio/documento ya abierto queda en memoria (la 2ª vez abre al instante, sin otro verEstudio); "Cargar disponibilidad de…" de administración plegado a una línea; ✕ de sacar estudio a 44 px. Sin motor. | Aplicada (en main desde el 14/11, 346dc74) |
| mejora/2026-11-15 | 📤 Enviar revisa en el celular lo mismo que Wsp.gs (teléfono de 10 números y nombre cargado): si falta, avisa al instante con "✏️ Corregir teléfono/nombre" (abre Corregir datos con el cursor en el campo); en Sin contactar el teléfono mal se ve en rojo con ⚠; si igual lo frena el motor, el aviso dice "Corregir" en vez de "Reintentar". Sin motor. | Aplicada (en main desde el 18/11, 9286141) |
| mejora/2026-11-15-flujo-agendar | Flujo semanal: agendar un lead. "Lo antes posible" arriba de la hoja (3 primeros libres de cada persona en los próximos días hábiles); si el lead no tiene turno, tocar un horario lo agenda al instante con Deshacer (el pedido sale a los 6 s o al salir de la app); chips de día con cuántos libres quedan; la hoja abre en el primer día con lugar; ya no abre la ficha después. Reagendar/corregir/firmar siguen con confirmar. Sin motor. | RECHAZADA por Karim (18/11): "Lo antes posible" no lo quiere. Se mergeó y se revirtió en main (772f719). No volver a proponer agendar con un toque ni la caja "Lo antes posible" |
| mejora/2026-11-16-contexto-visual, mejora/2026-11-16-pasar-bc | Guiones con contexto visual; botón "🚫 No responde más: pasar a BC" en la tarjeta (ramas armadas en chats con Karim) | Aplicadas (en main desde el 16/11, c03e341) |
| mejora/2026-11-16 | Primera apertura del día al instante: lo guardado en el celular (misma persona, hasta 4 días; antes 12 horas) se ve enseguida con aviso arriba "Mostrando lo guardado de ayer a las 19:20. Trayendo lo de hoy…"; mientras tanto lo que cambia algo no sale (avisa que espere, la hoja queda como estaba); si no llega lo de hoy, aviso con Reintentar y se puede guardar. Hasta 12 h igual que antes. Sin motor. | Aplicada (en main desde el 18/11, 80cbdd9) |
| mejora/2026-11-19 | Deshacer de "pasar a BC" y de cambiar fase en la ficha: manda deshacer:1 y desde; con el motor nuevo vuelve a No show/Reagenda (hoy el motor lo frena y el lead queda en BC); sin el motor, aviso claro de en qué fase quedó. Cargar a alguien nuevo: email revisado en el celular con la regla del motor (aviso rojo debajo del campo y botón apagado) y Corregir datos lo revisa antes de mandar. Confirmar de pasar a BC en rojo. wspDatos de fondo sin promesa sin atender. toUTC que acepta cualquier cosa y lo anota en el registro. Motor: mejora-2026-11-19.json (cambiarFase). | Aplicada 23/11 |
| mejora/2026-11-20 | Producción (Fede, Iván): Guiones se pide junto con getData (antes esperaba a que terminara getData); registro de uso con versión "lm"+fecha de la pantalla cuando no hay app instalada. Motor: mejora-2026-11-20.json (getData no lee las planillas de leads para quien no ve agenda, leads ni internas). | Aplicada 23/11 |
| mejora/2026-11-20-mensaje-no-firmo, -20-reporte-sol, -20-sol-carga-a-mano | 📤 en la tarjeta de la consulta con resultado y "Preguntar si ya decidió"; reporte de Sol sin pisar apellido ni lesión; Sol (modo carga) carga clientes a mano (ramas armadas en chats con Karim; motor v89-v91) | Aplicadas (en main desde el 20/11, dfb4445) |
| mejora/2026-11-21 | 📤 de la ficha y de la tarjeta de la consulta: abajo dice el último mensaje oficial ("Último: Vino a consulta y no firmó · ayer 18:05 por Pri") y mientras sale "⏳ Mandando…"; wspDatos se renueva si tiene más de 5 min al pintar el botón (como mucho 1 vez por minuto). Sin motor. | Aplicada 23/11 |
| mejora/2026-11-22-flujo-confirmaciones | Flujo semanal: confirmaciones del día y mensaje previo. Barra arriba de Tareas "✅ Confirmaciones: N por mandar · M esperan respuesta" con 📤 Mandar N; "Mandar … a los N que faltan" en Mensaje del día y Recordatorios; lista con cada mensaje completo y casillas para destildar; salen de a 2 con el mismo enviarWsp (momento); fila mandada con 📤 gris y "espera respuesta"; corte → "a revisar en uChat" y no entra en el próximo lote. Sin motor. | Aplicada 23/11 |
| mejora/2026-11-23 | Ficha: Corregir datos revisa nombre (2 letras o más), teléfono (8 números o más) y email en el celular con la regla de editarDatos, solo en lo que cambió (aviso rojo debajo del campo y Guardar apagado); Cambiar fase y Corregir datos bajan la hoja para quedar a la vista (360x640 y compu de 1163x587). Sin motor. | Pendiente |

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

## 2026-11-13 (noche, corrida del 14/11)
- main al día: 166e684 (entraron mejora/2026-11-08, -09, -11, -13-archivos-laboral y -13-disp-admin; motor v85). Copiados al banco index.html, sw.js y manifest. Tabla actualizada: todas aplicadas.
- Ramas pendientes: ninguna sin mergear (mejora/2026-11-05 y -08-flujo-sin-contactar figuran con commits de más pero su contenido ya está en main). Hubo lugar para una nueva.
- Cambios del motor pendientes: ninguno (los 3 archivos dicen APLICADO).
- Registro de uso real (USO, 12/11 noche y 13/11, filas ~2870-3416; usaron la app Fran, Pri, Karim, Mica, Cele y Juan; nada de Sol, Estefanía ni Julián):
  - Sin filas de error. 1 aviso "Sin conexión" de getData (Mica, Android, versión del 11/11, antes del arreglo de colgados).
  - getData sigue siendo lo más lento: casi todo 2-6 s, picos de 24,8 s, 19,1 s, 15,6 s y 14,9 s (Fran, Windows) y 11,7 s (Pri). getReporte 24 s una vez (Fran). Es del motor (idea de CacheService, pendiente).
  - enviarWsp ~45 envíos (Fran y Pri), 0 errores, 4-10,6 s.
  - fin2Calentar de Karim marcó 11.637.299 ms (3,2 h) en la versión del 13/11: no pasa por el corte de 35 s porque es un aviso de fondo que la pantalla no espera; el número es el tiempo con el iPhone dormido. No traba nada; queda solo como ruido en el registro. Mica 35 s (tiene finAcceso).
  - Aperturas con datos nuevos: Fran 15,9 s una vez, Pri 12,5 s, Mica 8,4 s, Juan 7,7 s. Con lo guardado 0,1-2,3 s.
  - Ya se usa Documentación de Laboral: subirEstudio 5-10 s (Fran, Pri).
- Banco: getEstudios falso ahora devuelve un estudio (cat estudios) y un documento (cat docs) para que se vea en ART/Tránsito y en Laboral (antes cat "Estudios" no coincidía y la ficha salía vacía); verEstudio devuelve el nombre según fid. Nuevo pruebas/probar_2026_11_14.py (títulos cortados, altura de la primera consulta en Agenda, verEstudio al abrir el mismo archivo 2 veces).
- Roles probados con correr.py (390 y 360): Cele, Pri (crea PIN), Karim, Estefanía. probar_2026_11_14.py: Pri, Karim, Mica, Juan. 0 errores de JavaScript, 0 pedidos fallidos, sin scroll horizontal. Pestañas iguales a la noche anterior. Permisos OK con datos falsos. "Cargar disponibilidad de…" (admin) abre el editor de la persona elegida: OK.
- Problemas encontrados:
  - Título "Seguimiento" cortado a mitad de palabra (sigue desde el 11/11).
  - Abrir el mismo estudio/documento dos veces lo baja dos veces (2 verEstudio; en el uso real 9-15 s cada vez).
  - Karim con "Todas" en 360x640: la caja nueva "Cargar disponibilidad de…" (~190 px) deja la primera consulta en 599 px de 640.
  - ✕ de sacar estudio 31x30 (tiene confirmación "¿Sacar?", no es grave).
- Descartado: formato del teléfono en notas sin nombre de Seguimiento (la app muestra los teléfonos tal cual en todos lados; cambiarlo solo ahí sería inconsistente).
- Mejora propuesta: mejora/2026-11-14 (ver tabla). Resultado en el banco: Seguimiento en 1 renglón (30 px en 390, 24 px en 360); verEstudio 2 → 1 en todos los roles; primera consulta de Karim 599 → 468 px; ✕ 44x44. correr.py en la rama igual que main (0 errores, mismas pestañas, sin elementos chicos nuevos).
- Ideas grandes:
  - getData en CacheService del motor (sigue pendiente; es lo único que el uso real muestra lento todos los días, picos de 15-25 s en Windows de Fran).
  - Pri y Fran en Windows: vista de escritorio a dos columnas en Tareas/Agendar (lista + ficha al lado).

## 2026-11-14 (noche, corrida de las 22:40)
- main al día: 2308dbc (entró mejora/2026-11-14 y 48c7afe: ✕ para sacar el cuadro "consultas para vos"). Copiados al banco index.html, sw.js y manifest.
- Ramas pendientes: ninguna sin mergear antes de esta noche (mejora/2026-11-05 y -08-flujo-sin-contactar figuran con commits de más pero su contenido ya está en main). Hubo lugar para una nueva.
- Cambios del motor pendientes: ninguno nuevo (no se armó archivo esta noche).
- Registro de uso real (USO, 14/11, filas 3417-3687; usaron la app Pri (Windows instalada) y Karim (iPhone y Windows); sábado, nadie más):
  - 1 aviso de enviarWsp: "El teléfono de Adrian no tiene 10 números. Revisalo antes de mandar." (Pri). Junto con "Este lead no tiene nombre cargado." del 11/11: la pantalla deja tocar 📤 y muestra la vista previa; el motor lo frena 3-5 s después y el aviso ofrece "Reintentar", que vuelve a fallar. → mejora/2026-11-15.
  - 1 "Sin conexión" de getData (Pri, Windows); se recuperó solo.
  - getData sigue siendo lo lento: 271 pedidos, promedio 3,0 s, picos 13,8 s, 12,3 s, 11,8 s, 10,8 s (Pri). Del motor (idea de CacheService, pendiente).
  - enviarWsp 15 envíos, promedio 5,6 s, máximo 9,7 s; 1 rechazado (el del teléfono). cambiarFase 4,5 s promedio, máximo 8,9 s.
  - fin2Calentar de Karim 50 s y 43 s (de fondo, no traba nada).
  - Aperturas con datos nuevos: Pri 14,2 s una vez (Windows), Karim 3-6,9 s. Con lo guardado 0,06-1,5 s.
  - Registro duplicado: el lote de Karim (iPhone, filas 3590-3596) llegó dos veces igual (3597-3603). Parece que el envío de logUso le llegó al motor pero el celular lo dio por fallado (se fue a segundo plano) y lo volvió a juntar. Solo ensucia los números del registro; anotado como idea.
- Banco: datos_falsos.py ahora tiene un lead de ART en Sin contactar con teléfono de 8 números (P077, Adriana) y enviarWsp falso frena teléfono y nombre igual que wspCtx_ de Wsp.gs. Nuevo pruebas/probar_tel_wsp.py (tiempo hasta enterarse, toques hasta mandarlo corregido, pedidos al motor).
  - probar_sin_contactar.py quedó viejo (busca el botón 💬 en ART, que desde el 09/11 es 📤 Enviar): falla igual en main y en la rama. Para rehacer.
- Roles probados con correr.py (390 y 360): Fran, Sol, Juan, Karim. 0 errores de JavaScript, 0 pedidos fallidos, sin scroll horizontal. Pestañas: Fran → Reporte, Agenda, Tareas, Seguimiento, Agendar; Sol → Finanzas, Agenda, Seguimiento, Agendar, Falta cargar; Juan → Finanzas, Agenda, Guiones, Falta cargar; Karim → Reportes, Agenda, Tareas, Agendar, Falta cargar. Permisos OK con datos falsos. probar_wsp.py igual en main y en la rama.
- Los "chicos" que marca la auditoría (Bloquear 34, chips de persona 32, flechas 34, Día/Semana 30) ya tienen zona táctil agrandada con ::after (la auditoría mide la caja visible). No es problema.
- Mejora propuesta: mejora/2026-11-15 (ver tabla). probar_tel_wsp.py (Pri, 390x844 y 360x640): enterarse 4,0 s → 0,3 s; toques hasta mandarlo con el teléfono corregido 9 → 6; enviarWsp 2 → 1 (0 rechazados); foco directo en Teléfono. correr.py en la rama igual que main (solo cambia el texto del botón del teléfono mal: "⚠ 26155501").
- Ideas grandes:
  - getData en CacheService del motor (sigue pendiente; Pri en Windows 10-14 s varias veces el sábado).
  - Registro de uso sin duplicados: que cada lote lleve un id y el motor ignore uno repetido (motor + pantalla).

## 2026-11-15 (noche, corrida de las 22:40)
- main sin cambios desde 2308dbc (14/11). El banco ya tenía index.html, sw.js y manifest iguales a main.
- Ramas pendientes: mejora/2026-11-15 y mejora/2026-11-15-flujo-agendar (2). Entran limpias sobre main, cada una y juntas (y junto con la nueva). Ninguna choca. Hubo lugar para una más.
- Cambios del motor pendientes: ninguno (los 3 archivos dicen APLICADO). No se bajó el Código.gs: la mejora de hoy es solo pantalla.
- Registro de uso real (USO, 14/11 y 15/11, filas ~3417-3704; usaron la app Pri y Karim el sábado; Fran, Cele y Mica el domingo):
  - Sin filas de error. 1 aviso de enviarWsp (el teléfono de 8 números del 14/11, ya cubierto por mejora/2026-11-15) y 1 aviso de getData de Pri.
  - La primera apertura del día espera todo getData con la pantalla vacía: Cele 17,3 s, Fran 16,2 s, Pri 14,2 s, Mica 9,8 s, Karim 3-5 s, todas como "abrir app (datos nuevos)" sin "abrir app (lo guardado)" antes. Causa: lo guardado en el celular solo se usa hasta 12 horas, y de un día al otro pasan más. El motor en frío tarda más en la primera (getData 8,7-17,1 s). → mejora/2026-11-16.
  - Con lo guardado (segunda apertura del día) 0,06-1,5 s.
  - getData sigue lento en Windows de Pri (271 pedidos el 14/11, picos 10-14 s). Del motor (idea de CacheService, pendiente).
  - fin2Calentar de fondo: Mica 36 s, Cele 16 s, Karim 43-50 s (no traba nada).
- Banco: nuevo pruebas/probar_snap.py (entra, envejece lo guardado a 8 h, 40 h y 5 días, abre con getData retenido 9 s; mide cuándo se ve, el aviso, si deja guardar, y getData que falla; también lo guardado de otra persona).
- Roles probados con correr.py (390 y 360): Mica, Pri (crea PIN), Estefanía, Karim. probar_snap.py: Cele, Pri, Mica, Karim. 0 errores de JavaScript, 0 pedidos fallidos, sin scroll horizontal. Pestañas: Mica → Finanzas, Agenda, Guiones, Falta cargar; Pri → Reporte, Agenda, Tareas, Seguimiento, Agendar; Estefanía → Agenda, Falta cargar; Karim → Reportes, Agenda, Tareas, Agendar, Falta cargar. Permisos OK con datos falsos.
- Mejora propuesta: mejora/2026-11-16 (ver tabla). probar_snap.py: lo guardado de 40 h → main: pantalla vacía los 9 s; rama: agenda a los 0,1-0,2 s con aviso. Cargar resultado mientras espera → no sale saveAction, aviso "⏳ Un momento…", la hoja queda con lo elegido; al llegar lo de hoy el aviso se va y se guarda (1 saveAction). getData que falla → aviso "No se pudo traer lo de hoy" + Reintentar y se puede guardar. 8 h → igual que main. 5 días o de otra persona → igual que main (no se muestra). correr.py en la rama igual que main (mismas 110 pantallas auditadas, sin diferencias).
- Ideas grandes:
  - getData en CacheService del motor (sigue pendiente; es lo que alarga la primera apertura y los picos de Pri).
  - Registro de uso sin duplicados (sigue pendiente).

## 2026-11-16 (noche, corrida del 17/11 01:40 UTC)
- main al día: c03e341 (entraron mejora/2026-11-16-contexto-visual y -16-pasar-bc, armadas con Karim). Copiados al banco index.html, sw.js y manifest. Tabla actualizada.
- Ramas pendientes: mejora/2026-11-15, -15-flujo-agendar y -16 (3). Merge local contra main (sin pushear): -15 y -16 entran limpias; -15-flujo-agendar CHOCA en una sola línea de index.html (la lista de selectores del click: main sumó [data-pasarbc] y la rama [data-agprox]; se arregla dejando los dos). Con 3 pendientes, esta noche NO se armó rama nueva.
- Cambios del motor pendientes: ninguno (los 3 archivos dicen APLICADO). Bajé el Código.gs del motor real (solo lectura) para revisar de dónde salen las fechas.
- Registro de uso real (USO, filas 3705-4595, 15/11 noche y lunes 16/11; usaron la app Pri, Fran, Karim, Julián, Mica y Cele):
  - 1 ERROR de pantalla: Karim, Windows navegador 1422x701, versión del 16/11 15:29 (c082f12): "Uncaught TypeError: s.split is not a function" en la línea 1168 (toUTC), 2 veces, en el mismo lote que un saveAction desde agenda. toUTC recibe algo que no es texto (número u objeto) desde addDays/diffDays/dow/longDate/shortDate/mondayOf. Revisé el motor: las fechas de leads, bloqueos, feriados y finanzas salen como texto. No lo pude reproducir en el banco (caza_toutc.py, ~700 toques en Karim 1422 y 390, Pri 1280 y Mica 390, con toUTC avisando). Para la próxima rama: que toUTC acepte cualquier cosa (String(s)) y avise en logUso de dónde vino, así no corta la pantalla.
  - enviarWsp: ~100 envíos (Pri y Fran), 4-10,9 s, y 5 avisos de Pri; los vistos: "Este lead no tiene nombre cargado." y "El teléfono de Patricia no tiene 10 números". Es justo lo que arregla mejora/2026-11-15 (pendiente).
  - getData: Fran (Windows instalada) 6 avisos "El servidor no respondió a tiempo" / "Sin conexión", picos 35,3 s, 24,7 s, 22,9 s, 21,4 s; Pri 35,2 s, 34,9 s, 32,5 s, 18,7 s; Mica 19,1 s. El corte de 35 s y el reintento funcionan; lo lento es del motor (idea de CacheService, pendiente).
  - Primera apertura del día con la pantalla vacía: Karim 25,3 s, Mica 19,4 s, Pri 19,1 s, Cele 16 s, Karim 11,4 s. Es lo que arregla mejora/2026-11-16 (pendiente).
  - getReporte hasta 20,3 s (Karim) y 20 s (Fran, con aviso). getFin2 hasta 14,9 s (Karim, 1 aviso).
  - Julián volvió a usar la app (Windows): 1 "Sin conexión" en saveVisto; saveBloqueo OK.
  - fin2Calentar de fondo: Mica 4.464.333 ms (celular dormido), Julián 57 s, Karim 42 s. Ruido, no traba nada.
- Banco: nuevos pruebas/probar_pasar_bc.py (botón nuevo "pasar a BC": aparece para intakers en No show/Reagenda/Seguimiento, pide tocar dos veces, saca de la agenda, Deshacer vuelve a la fase anterior con un segundo cambiarFase) y pruebas/caza_toutc.py (toca casi todo buscando el error de toUTC).
- Roles probados con correr.py (390 y 360): Juan, Fran, Sol, Karim. 0 errores de JavaScript, 0 pedidos fallidos, sin scroll horizontal. Pestañas: Juan → Finanzas, Agenda, Guiones, Falta cargar; Fran → Reporte, Agenda, Tareas, Seguimiento, Agendar; Sol → Finanzas, Agenda, Seguimiento, Agendar, Falta cargar; Karim → Reportes, Agenda, Tareas, Agendar, Falta cargar. Permisos OK con datos falsos.
- Pasar a BC (Fran): OK. 358x46, confirma con segundo toque, toast con Deshacer, vuelve a No show. Mica (abogada) no lo ve: OK. Detalle: el paso "Tocá de nuevo para confirmar" se ve casi igual que el botón normal (mismo color); para una acción que saca el lead de la agenda convendría que se note (rojo). Anotado para la próxima rama.
- Ideas grandes:
  - getData en CacheService del motor (sigue pendiente; hoy hubo pedidos de 32-35 s en Pri y Fran).
  - Registro de uso con el stack del error (archivo y función), para encontrar errores como el de toUTC sin tener que adivinar.

## 2026-11-17 (noche, corrida de las 22:37)
- main sin cambios desde c03e341 (16/11). El banco ya tenía index.html, sw.js y manifest iguales a main.
- Ramas pendientes: mejora/2026-11-15, -15-flujo-agendar y -16 (3). Merge local contra main (sin pushear): -15 y -16 entran limpias (también juntas); -15-flujo-agendar sigue chocando en la misma línea de index.html (selectores del click: [data-pasarbc] de main y [data-agprox] de la rama; se arregla dejando los dos). mejora/2026-11-05, -06 y -08-flujo-sin-contactar siguen figurando sin mergear pero su contenido ya está en main. Con 3 pendientes, esta noche NO se armó rama nueva.
- Las 3 pendientes juntas sobre main (choque resuelto a mano, solo local): correr.py con Cele, Pri, Estefanía y Mica igual que main (0 errores, mismas pestañas); probar_tel_wsp.py, probar_snap.py, probar_agendar.py y probar_pasar_bc.py OK (solo los 2 "reading 'update'" de siempre del banco).
- Cambios del motor pendientes: ninguno (los 3 archivos dicen APLICADO). No se bajó el Código.gs (sin rama nueva).
- Registro de uso real (USO, filas 4596-5102, martes 17/11; usaron la app Pri (casi todo, Windows instalada), Karim, Julián, Mica, Cele y Fran (poco); nada de Sol, Estefanía ni Juan):
  - Sin filas de error. El error de toUTC del 16/11 no volvió a aparecer.
  - 3 avisos "Sin conexión" de getData de Mica (Android instalada, agenda, versión actual), uno después de 21,5 s. El corte y el reintento funcionan; parece conexión del celular o motor lento.
  - getData de Pri: picos 29,8 s, 19,7 s, 17 s, 15,9 s, 13,4 s; promedio ~3,5 s. Julián 11,9 s. Del motor (idea de CacheService, pendiente).
  - enviarWsp ~40 envíos (Pri), 4-9,2 s, 0 errores y 0 avisos de teléfono/nombre hoy.
  - agendar hasta 16,2 s (Pri); subirEstudio 16,6 s; segComentar 10,7 s; saveAction de Pri 5-8,8 s en racha (11 en un lote).
  - Primera apertura con datos nuevos: Mica 8,6 s, Pri 7 s, Julián 5,6 s, Karim 5,5 s (lo arregla mejora/2026-11-16, pendiente).
  - fin2Calentar de fondo: Karim 30,6 s, Mica 14,3 s (no traba nada).
- Roles probados con correr.py (390 y 360): Cele, Pri (crea PIN), Estefanía, Mica. 0 errores de JavaScript, 0 pedidos fallidos, sin scroll horizontal. Pestañas: Cele y Mica → Finanzas, Agenda, Guiones, Falta cargar; Pri → Reporte, Agenda, Tareas, Seguimiento, Agendar; Estefanía → Agenda, Falta cargar. Permisos OK con datos falsos.
- Sin problemas nuevos. Lo chico que marca la auditoría es lo de siempre (con zona táctil agrandada).
- Para la próxima rama (cuando se apruebe alguna): toUTC que acepte cualquier cosa y avise de dónde vino; "Tocá de nuevo para confirmar" de pasar a BC en rojo.
- Ideas grandes:
  - getData en CacheService del motor (sigue pendiente; hoy picos de 20-30 s en Pri).
  - Registro de uso con el stack del error (sigue pendiente).

## 2026-11-18 (chat con Karim)
- Karim avisó que ya están implementadas todas las mejoras salvo "Lo antes posible" al agendar, que no la quiere.
- Verificado en main (fd83fc7/772f719, cache consultas-20261118200407): entraron mejora/2026-11-15 (📤 Enviar con "Corregir teléfono/nombre") y mejora/2026-11-16 (lo guardado al abrir); mejora/2026-11-15-flujo-agendar se mergeó y se revirtió (772f719, sin "Lo antes posible" ni data-agprox). También entró 381c842 (Traslados: recibos del Uber cuando la consulta ya pasó).
- Ramas pendientes ahora: ninguna. La próxima noche hay lugar para rama nueva.
- Banco: copiados index.html, sw.js y manifest de main al 18/11. probar_agendar.py y flujo_agendar.py prueban la rama rechazada: ya no aplican a main (no usar como regresión).

## 2026-11-18 (noche, corrida de las 22:37)
- main sin cambios desde 772f719 (18/11). El banco ya tenía index.html, sw.js y manifest iguales a main.
- Ramas pendientes antes de esta noche: ninguna (-05, -06 y -08-flujo-sin-contactar figuran sin mergear pero su contenido está en main). Hubo lugar para una nueva.
- Cambios del motor pendientes: ninguno antes de esta noche. Bajé el Código.gs del motor real y del entorno de prueba (solo lectura).
- Registro de uso real (USO, filas 5095-5986, 17/11 noche y miércoles 18/11; usaron la app Pri (481 filas), Fran, Karim, Cele, Julián y Mica; nada de Sol, Estefanía ni Juan):
  - 1 ERROR "pantalla (promesa)": Pri, "Sin conexión", en el mismo lote que wspDatos, enviarWsp, cambiarFase y getData fallados desde tareas > ficha. Causa: wspDatos() renueva atrás cuando lo guardado tiene más de 5 min y devuelve lo viejo; si esa renovación falla nadie la atiende. Solo ensucia el registro (no traba nada). Reproducido en node (pruebas/probar_wspdatos_node.js). → mejora/2026-11-19.
  - 1 aviso de cambiarFase de Pri desde agenda: "Esa fase no se cambia desde acá". Es el Deshacer de "pasar a BC": vuelve a la fase anterior (No show o Reagenda) y el motor real solo acepta fases manuales. El lead queda en BC sin que se note bien. El banco no lo mostraba porque el motor falso aceptaba cualquier fase. → mejora/2026-11-19 + mejora-2026-11-19.json.
  - 1 aviso de agendarNuevo de Fran: "Revisá el email." (2 rechazos en el lote, desde agendar > manual). La pantalla no revisa el email y el motor lo frena recién al final, después de elegir día y horario. → mejora/2026-11-19.
  - ~20 avisos "Sin conexión" / "El servidor no respondió a tiempo" (Pri en Windows, Cele en iPhone, Mica, Karim): getData, getReporte, getCreativos, agendarNuevo, saveAction, equipoLogin. El corte y el reintento funcionan.
  - getData: 206 lentos; picos 49,1 s (Cele), 35,6 y 35,3 s (Pri), 28,1 s (Pri), 25,8 s (Fran). getReporte hasta 33,3 s (Pri). Del motor (idea de CacheService, pendiente).
  - enviarWsp 32 lentos, hasta 12,9 s; 1 "Sin conexión" (Pri). subirEstudio 31 s (Pri, 2 veces). agendarNuevo 35,2 s una vez (Pri).
  - Aperturas con datos nuevos: Julián 38,3 s (Windows), Fran 28 s, Cele 16,7 s y 12,6 s, Pri 16,3 s, Karim 13,1 s; con lo guardado 0,4-1,7 s (mejora/2026-11-16 funcionando: casi todas las aperturas lentas tienen antes "lo guardado").
  - Ruido de celular dormido: cambiarFase 370 s (Pri), saveAction 8.501.118 ms (Mica), Karim abrir app 384 s, fin2Calentar 104 s (Cele).
- Banco:
  - datos_falsos.py: cambiarFase frena como el motor real (solo FASES_MANUALES; con MOTOR_DESHACER=1 simula el cambio de mejora-2026-11-19.json); agendarNuevo y editarDatos revisan el email como el motor.
  - explora_base.py acepta 'dsf' en el viewport (capturas x3).
  - probar_pasar_bc.py ahora mide el Deshacer (aviso y fase final). Nuevos probar_email.py y probar_wspdatos_node.js.
- Roles probados con correr.py (390 y 360): Juan, Sol, Fran, Karim. 0 errores de JavaScript, 0 pedidos fallidos, sin scroll horizontal. Pestañas: Juan → Finanzas, Agenda, Guiones, Falta cargar; Sol → Finanzas, Agenda, Seguimiento, Agendar, Falta cargar; Fran → Reporte, Agenda, Tareas, Seguimiento, Agendar; Karim → Reportes, Agenda, Tareas, Agendar, Falta cargar. Permisos OK con datos falsos.
- Resultados de la rama:
  - probar_pasar_bc.py (Fran, lead en No show): main → Deshacer falla, "Esa fase no se cambia desde acá", queda en BC. Rama sin motor nuevo → igual, con aviso "No se pudo deshacer: quedó en BC. La app todavía no deja volver a NO SHOW." Rama + motor nuevo → "Volvió a NO SHOW." y vuelve a la agenda. Confirmar en rojo. Mica no ve el botón.
  - probar_email.py (Fran, 390 y 360, "rosa.lucero@gmail"): main → se entera a los 3 toques, después de elegir horario, con 1 agendarNuevo rechazado; rama → aviso rojo debajo del campo al escribir, botón apagado, 0 pedidos; con ".com" se prende.
  - probar_wspdatos_node.js: main 1 promesa sin atender, rama 0.
  - correr.py en la rama igual que main (mismo resultado JSON). probar_wsp.py y probar_tel_wsp.py OK en la rama.
- Ideas grandes:
  - getData en CacheService del motor (sigue pendiente; hoy picos de 35-49 s y aperturas de 28-38 s en Windows).
  - Registro de uso con el stack del error (sigue pendiente).

## 2026-11-19 (noche, corrida de las 22:40)
- main al día: dda09cf (entraron en chats con Karim: Seguimiento con formato de planilla y orden por fecha, resumen del caso en la ficha del lead, textos sin nombres fijos de intakers (se suma Agus) y "Reporte del turno" para intakers (Mi turno | Semana, reporteTurno y cerrarTurno)). Copiados al banco index.html, sw.js y manifest. Las ramas -19-ficha-resumen, -19-reporte-turno, -19-seguimiento-orden y -19-seguimiento-planilla están en main.
- Ramas pendientes: solo mejora/2026-11-19 (entra limpia sobre main, sin pushear). Hubo lugar para una nueva. mejora-2026-11-19.json sigue sin aplicar (cambiarFase del motor real todavía no tiene deshacer).
- Equipo nuevo en el motor real: Agus (intaker, igual que Fran y Pri) y Fede e Iván (producción: solo Guiones).
- Registro de uso real (USO, filas 5986-6682, 18/11 noche y 19/11; Pri 281 filas, Fran 202, Karim 76, Agus 62, Iván 42, Fede 17, Mica 9, Cele 8; nada de Sol, Estefanía, Juan ni Julián):
  - Sin filas de error.
  - 4 avisos "El servidor no respondió a tiempo": getData de Pri (agendar, 35 s), Agus (seguimiento, 18 s) y Fede (guiones, 2 veces, una con el celular dormido 2 h); getReporte de Pri (13 s).
  - Producción espera getData para nada: Fede getData 35,5 s cortado y apertura 23,7 s; Iván aperturas 29,6 s y 17,6 s. getData les lee las 3 planillas aunque no ven leads ni agenda, y Guiones (getCreativos) recién se pedía al terminar getData. → mejora/2026-11-20 + mejora-2026-11-20.json.
  - getData: 144 lentos, casi todo 4-12 s (Pri, Fran, Agus). getReporte hasta 21,5 s (Karim). cambiarFase hasta 18,9 s y enviarWsp hasta 13,2 s (Fran, agendar > ficha). reporteTurno (nuevo) 10 lentos hasta 9 s (Fran).
  - 124 filas sin versión (Agus, Fede, Iván y parte de Karim, en navegador sin la app instalada): la versión salía solo del cache del service worker. → mejora/2026-11-20 (fallback "lm"+fecha de la pantalla).
  - Karim en navegador: "abrir app (lo guardado)" hasta 5,2 s (mide desde que empieza a bajar la página de 480 KB; sin service worker no hay copia local).
  - fin2Calentar de Karim 52,6 s (de fondo, no traba nada).
- Banco:
  - datos_falsos.py: Agus (intaker) y Fede (producción) con los permisos de CONFIG.EQUIPO del motor real; respuestas falsas para reporteTurno y cerrarTurno (forma de viewTurno).
  - Nuevos pruebas/probar_turno.py (Reporte del turno: pedidos quedándose en la pantalla, cerrar turno) y pruebas/probar_prod.py (async: Fede con getData lento o rápido y getCreativos de 4 s; FOTO=9.5 saca captura a esa altura).
- Roles probados con correr.py (390 y 360): Cele, Pri (crea PIN), Estefanía, Karim, Agus, Fede. 0 errores de JavaScript, 0 pedidos fallidos, sin scroll horizontal. Pestañas: Cele → Finanzas, Agenda, Guiones, Falta cargar; Pri y Agus → Reporte, Agenda, Tareas, Seguimiento, Agendar; Estefanía → Agenda, Falta cargar; Karim → Reportes, Agenda, Tareas, Agendar, Falta cargar; Fede → solo Guiones. Permisos OK con datos falsos.
- Reporte del turno (Pri): cerrar turno en 2 toques con confirmación, queda el cuadro "Cerraste tu turno" y el reporte copiado. Quedándose 6 min en la pantalla salen 4 reporteTurno (se renueva en cada render después de 60 s). No es grave; anotado.
- Resultado de la rama (probar_prod.py, Fede, 390x844): getData 9 s → main ve Guiones a los 13,3 s, rama 9,2 s; getData 1,5 s (motor con el cambio) → main 5,8 s, rama 4,2 s. correr.py en la rama igual que main (mismas 140 pantallas auditadas, 0 errores, mismas pestañas).
- Motor: mejora-2026-11-20.json aplica sobre el Código.gs del motor real y pasa new Function; sobre el entorno de prueba NO aplica (le falta swr) → "Sincronizar primero el entorno de prueba".
- Ideas grandes:
  - getData en CacheService del motor (sigue pendiente; hoy picos de 26-35 s en Pri).
  - Reporte del turno: renovar solo al entrar a la pantalla o al tocar "Copiar/cerrar", no en cada render (menos pedidos al motor).


## 2026-11-20 (noche, corrida de las 22:36)
- main al día: dfb4445 (entraron en chats con Karim mejora/2026-11-20-mensaje-no-firmo, -20-reporte-sol y -20-sol-carga-a-mano; motor real v91). Copiados al banco index.html, sw.js y manifest. Tabla actualizada.
- Ramas pendientes antes de esta noche: mejora/2026-11-19 y mejora/2026-11-20 (2). Merge local contra main (sin pushear): las dos entran limpias, también junto con la nueva -21. -05, -06, -06-repetidos/-reportes-claros/-semana-rama/-tareas-reportes y -08-flujo-sin-contactar figuran sin mergear pero su contenido está en main. Hubo lugar para una nueva.
- Cambios del motor pendientes: mejora-2026-11-19.json y mejora-2026-11-20.json (sin cambios). Bajé el Código.gs y Wsp.gs del motor real (solo lectura) para copiar el catálogo de mensajes.
- Registro de uso real (USO, filas 6676-7327, 19/11 noche y 20/11; Pri 321 filas, Fran 109, Agus 95, Mica 45, Cele 28, Sol 23, Karim 21, Julián 10; nada de Estefanía, Juan, Fede ni Iván):
  - Sin filas de error.
  - Avisos: 6 "Sin conexión" de fin2Calentar (Mica, Cele, Karim; de fondo, con el celular dormido: 13 h, 57 min), 3 de getData (Mica 2 "no respondió a tiempo", Cele 1) y 1 de getCreativos (Cele, celular dormido 23 min). 1 PIN de finanzas mal (Sol). Nada para arreglar en la pantalla: el corte y el reintento funcionan.
  - getData: 123 lentos, casi todo 4-8 s; picos 20,9 s (Mica), 19,8 s (Pri). getReporte hasta 10,3 s (Julián). Mejor que el 18-19/11.
  - Sol usó Finanzas (modo carga) por primera vez: getFin2 5-8,5 s y saveFin2 5-8,6 s; cada guardado pide después la planilla de nuevo (getFin2 fresco). Lo guardado ya se ve al instante; no lo toqué.
  - enviarWsp 28 lentos hasta 19 s (Pri, tareas > lead), 0 errores. reporteTurno 14 lentos hasta 7,1 s.
  - Aperturas con datos nuevos: Pri 11,4 s y 9,2 s (Windows), Karim 8,3 s, Fran 8,1 s; con lo guardado 0,1-2,3 s.
- Banco:
  - datos_falsos.py: catálogo de WhatsApp copiado del CATALOGO de Wsp.gs del motor real (30 mensajes, textos inventados); wspDatos devuelve lo "mandado" (envios) como la hoja de envíos del motor.
  - Nuevo pruebas/probar_wsp_tarjeta.py: tarjeta de la consulta con resultado (Vino y no firmó, No vino) → 📤 → mensaje sugerido → Enviar. PREVIO=1: ayer Pri ya le mandó a Rubén; LENTO=6: enviarWsp tarda 6 s.
- Roles probados con correr.py (390 y 360): Mica, Fran, Sol, Juan, Karim (Julián no: en el banco tiene el PIN bloqueado a propósito). 0 errores de JavaScript, 0 pedidos fallidos, sin scroll horizontal. Pestañas: Mica y Juan → Finanzas, Agenda, Guiones, Falta cargar; Fran → Reporte, Agenda, Tareas, Seguimiento, Agendar; Sol → Finanzas, Agenda, Seguimiento, Agendar, Falta cargar; Karim → Reportes, Agenda, Tareas, Agendar, Falta cargar. Permisos OK con datos falsos.
- 📤 en la tarjeta de la consulta (nuevo del 20/11, Fran): aparece en Vino y no firmó y No vino, sugiere el mensaje correcto (Vino a consulta y no firmó / No vino a la consulta), manda 1 solo enviarWsp. Mica no lo ve. Problema: el botón no dice si ya se le mandó (ni mientras sale): con 3 intakers, para saber si Pri ya le escribió ayer hay que abrir la lista. → mejora/2026-11-21.
- Resultado de la rama (probar_wsp_tarjeta.py, Fran, 390 y 360): main → el botón dice siempre "📤 Mandar mensaje por WhatsApp"; rama → al abrir: "Último: Vino a consulta y no firmó · ayer 18:05 por Pri", mientras sale "⏳ Mandando el mensaje por WhatsApp…", después "Último: … hoy 11:20 por Fran". correr.py en la rama igual que main (130 pantallas auditadas idénticas, 0 errores, mismas pestañas). probar_wsp.py, probar_tel_wsp.py y probar_wsp_cancelar.py: misma salida en main y en la rama.
- Ideas grandes:
  - saveFin2 que devuelva la planilla ya actualizada (motor), así no hace falta el getFin2 de después de cada guardado (hoy 2 pedidos de 5-8 s por cliente que carga Sol).
  - getData en CacheService del motor (sigue pendiente; hoy picos de 20 s).

## 2026-11-21 (sábado noche, corrida de las 22:37)
- main sin cambios desde dfb4445 (20/11). El banco ya tenía index.html, sw.js y manifest iguales a main.
- Ramas pendientes: mejora/2026-11-19, -20 y -21 (3). Merge local contra main (sin pushear): las tres entran limpias, también juntas. Con 3 pendientes, esta noche NO se armó rama nueva. -05, -06, -06-repetidos/-reportes-claros/-semana-rama/-tareas-reportes y -08-flujo-sin-contactar figuran sin mergear pero su contenido está en main.
- Cambios del motor pendientes: mejora-2026-11-19.json y mejora-2026-11-20.json (sin cambios). No se bajó el Código.gs (sin rama nueva).
- Registro de uso real (USO, filas 7320-7517, 20/11 noche y sábado 21/11; casi todo Fran en Windows instalada, algo de Karim en navegador el 20/11):
  - Sin filas de error.
  - 1 aviso "El servidor no respondió a tiempo": getReporte de Fran (35,3 s, reporte). El corte y el reintento funcionan.
  - reporteTurno: ~15 lentos de 4-7 s en un solo día de Fran (se pide de nuevo en cada render de la pantalla Reporte). Es la idea ya anotada el 19/11.
  - getData lentos casi todos 4-10 s; pico 18,6 s (apertura con datos nuevos de Fran 18,9 s; con lo guardado 0,3-0,5 s). enviarWsp 4-6,7 s, 0 errores. derivar 7,5 s, subirEstudio 7,8 s.
  - Karim en navegador sin versión en el registro (lo arregla mejora/2026-11-20, pendiente). fin2Calentar 39,6 s de fondo.
- Roles probados con correr.py (390 y 360): Cele, Agus, Estefanía, Juan. 0 errores de JavaScript, 0 pedidos fallidos. Pestañas: Cele y Juan → Finanzas, Agenda, Guiones, Falta cargar; Agus → Reporte, Agenda, Tareas, Seguimiento, Agendar; Estefanía → Agenda, Falta cargar. Permisos OK con datos falsos.
- Las 3 pendientes juntas sobre main (solo local): correr.py con los mismos roles igual que main (0 errores, mismas pestañas); probar_wsp_tarjeta.py (Agus, 390) OK, con "Último: No vino a la consulta · 11:20 por Agus" en la rama; probar_pasar_bc.py OK (Mica no ve el botón).
- Nota del banco: el nombre va con acento en correr.py ("Estefanía").
- Sin problemas nuevos. No se mandó informe (sin novedades).
- Ideas grandes (siguen): Reporte del turno que no se renueve en cada render; getData en CacheService del motor.

## 2026-11-22 (domingo noche, corrida de las 22:36)
- main sin cambios desde dfb4445 (20/11). El banco ya tenía index.html, sw.js y manifest iguales a main.
- Ramas pendientes: mejora/2026-11-19, -20, -21 y -22-flujo-confirmaciones (4). Merge local contra main (sin pushear): las cuatro entran limpias, también juntas. Con 4 pendientes, esta noche NO se armó rama nueva.
- Cambios del motor pendientes: sin cambios (no se bajó el Código.gs, sin rama nueva).
- Registro de uso real: sin filas nuevas desde la noche del 21/11 (última fila 7517, Fran, sábado; planilla sin cambios desde el 21/11 14:03). Nada nuevo para mirar.
- Roles probados con correr.py (390 y 360): Mica, Pri, Sol, Karim. 0 errores de JavaScript, 0 pedidos fallidos, sin scroll horizontal. Pestañas: Mica → Finanzas, Agenda, Guiones, Falta cargar; Pri → Reporte, Agenda, Tareas, Seguimiento, Agendar; Sol → Finanzas, Agenda, Seguimiento, Agendar, Falta cargar; Karim → Reportes, Agenda, Tareas, Agendar, Falta cargar. Permisos OK con datos falsos.
- Las 4 pendientes juntas sobre main (solo local): correr.py con los mismos roles igual que main (0 errores, mismas pestañas; el audit cambia solo en Tareas/inicio de Pri y Karim, por la barra de confirmaciones). probar_confirmaciones.py OK (el único ERR_FAILED de consola es un pedido externo que el banco bloquea).
- Sin problemas nuevos. No se mandó informe (sin novedades).

## 2026-11-23 (lunes noche, corrida de las 22:36)
- main al día: 5b6d0bf (publicadas -19, -20, -21 y -22 con el ok de Karim; motor v92). Copiados al banco index.html, sw.js y manifest (la rama del banco no comparte historia con main: se copian, no se mergean).
- Ramas pendientes antes de esta noche: ninguna real. -05, -06, -06-repetidos y -08-flujo-sin-contactar figuran con commits fuera de main pero su contenido ya está en main. Hubo lugar para una nueva.
- Cambios del motor pendientes: ninguno nuevo. Bajé el Código.gs del motor real (solo lectura) para copiar la regla de editarDatos.
- Registro de uso real (USO, filas 7518-8386, lunes 23/11; Pri ~620 filas en Windows 1163x587 instalada, Fran ~200, Karim ~40, algo de Juan y Mica; nada de Cele, Sol, Estefanía, Agus, Julián):
  - Sin filas de error.
  - 3 avisos: getData "Sin conexión" (Karim, Windows navegador), getData "El servidor no respondió a tiempo" (Pri, 13,3 s) y editarDatos "Escribí el nombre." (Pri, agendar > ficha: el motor rechazó el nombre vacío después de 3-4 s). → mejora/2026-11-23.
  - Pri hizo Sin contactar en serie: lote de 38 pedidos con pares enviarWsp + cambiarFase (4-6 s cada uno, 0 errores; pico enviarWsp 27,7 s).
  - getData casi todo 2-8 s; picos 22,7 s y 20,3 s (Pri), 18 s (apertura de Pri 18,3 s). Muchas filas de resumen con 1 solo getData (se renueva al volver a la app; con lo guardado abre en 0,4-2 s).
  - reporteTurno sigue pidiéndose varias veces por sesión (4-7 s, Pri y Fran). Idea ya anotada.
  - Karim: fin2Calentar 36-40 s de fondo; getFin2Panel 16,4 s y apertura con datos nuevos 17,2 s (Finanzas).
- Banco: datos_falsos.py → editarDatos falso rechaza nombre de menos de 2 letras y teléfono de menos de 8 números como el motor real. Nuevo pruebas/probar_datos.py (Pri en 1163x587, 360x640 y 390x844: Cambiar fase y Corregir datos a la vista; nombre vacío, teléfono corto y teléfono bien).
- Roles probados con correr.py (390 y 360): Juan, Pri, Estefanía, Karim. 0 errores de JavaScript, 0 pedidos fallidos, sin scroll horizontal. Pestañas: Juan → Finanzas, Agenda, Guiones, Falta cargar; Pri → Reporte, Agenda, Tareas, Seguimiento, Agendar; Estefanía → Agenda, Falta cargar; Karim → Reportes, Agenda, Tareas, Agendar, Falta cargar. Permisos OK con datos falsos.
- Problemas encontrados (probar_datos.py en main):
  - Corregir datos con el nombre vacío o el teléfono corto: el botón deja mandar, sale 1 editarDatos y el motor contesta "Escribí el nombre." / "Revisá el teléfono." (en el uso real 3-4 s).
  - Cambiar fase y Corregir datos se abren fuera de la vista en 360x640 y en 1163x587 (panel a 555-650 px; Guardar cambios a 883-977 px): se toca y parece que no pasa nada. En 390x844 "Guardar cambios" queda abajo de todo.
- Resultado de la rama (probar_datos.py): en los 3 tamaños el panel y el botón quedan a la vista; nombre vacío → "⚠ Escribí el nombre (2 letras o más)." y botón apagado, 0 pedidos; teléfono "26155" → "⚠ Al teléfono le faltan números (ej.: 2615551234)." y 0 pedidos; teléfono bien → "Datos corregidos." con 1 editarDatos. correr.py en la rama igual que main (110 pantallas auditadas idénticas, 0 errores, mismas pestañas). probar_wsp.py, probar_tel_wsp.py y probar_email.py: misma salida en main y en la rama.
- Ideas grandes (siguen): Reporte del turno que no se renueve en cada render; getData en CacheService del motor (hoy picos de 20-23 s en Pri).

## Flujos rediseñados (tarea semanal de los domingos)
| Fecha | Flujo | Para quién | Toques antes → después | Rama | Motor |
|---|---|---|---|---|---|
| 2026-11-08 | Sin contactar → primer mensaje → Contacté → fase | Intakers (Fran, Pri) | 13 → 8 (2 leads, con navegación); por lead: 5 → 2 si contesta enseguida, 7 → 1-3 si contesta después. Hojas 2 → 0, scroll ~2.000 px → 0-360 px | mejora/2026-11-08-flujo-sin-contactar | Solo pantalla |
| 2026-11-15 | Agendar un lead (Agendar o Tareas → hoja de agendar) | Intakers (Fran, Pri) | Lo antes posible 7 → 4 (desde la lista 5 → 2); día y hora pedidos 7 → 5 (5 → 3); Juan con agenda rayada 8 → 4 (6 → 2). Deshacer: no había → sí. Ficha que había que cerrar: 1 → 0 | mejora/2026-11-15-flujo-agendar (RECHAZADA 18/11, revertida en main) | Solo pantalla |
| 2026-11-22 | Confirmaciones del día y mensaje previo (Tareas: Mensaje del día y Recordatorios) | Intakers (Fran, Pri, Agus) | Mandar 5 oficiales + 2 Tránsito: 13 → 5; con las respuestas (7 ✅): 20 → 12. Scroll hasta la primera fila 258 px → 0. Pedidos iguales (5 enviarWsp + 7 saveAction), ahora de a 2 | mejora/2026-11-22-flujo-confirmaciones | Solo pantalla |

### 2026-11-08 — Sin contactar (intakers)
- Por qué este: en USO (06-07/11) lo que más se repite de Fran es cambiarFase y editarDatos desde "tareas > ficha" y "agendar > ficha" (12 cambiarFase, 4-6 s cada uno, la pantalla ya lo muestra al instante) y levantarLead 5 veces. Es la primera semana de la tarea: no hay flujos repetidos.
- Antes (banco, Fran, 390 y 360): "Sin contactar" está al fondo de Tareas (~1.400-1.500 px de scroll). Para clasificar: ficha → Cambiar fase → fase → cerrar. Si toca "✓ Contacté" (sin Deshacer) el lead desaparece de Tareas y cuando contesta hay que buscarlo en Agendar. 13 toques, 2 hojas, ~2.000 px de scroll, 6 pedidos.
- Después: barra "📨 N leads sin contactar · M sin fase · Ver ›" arriba de Tareas; al volver de WhatsApp (4 s o más afuera) queda marcado solo con Deshacer (el pedido sale a los 10 s o al salir de la app); sección nueva "Falta la fase" (sin fase, ya con nombre de intaker, últimos 7 días) con A/B/Llamada/C/Otra en la fila; después de elegir queda "✓ Quedó en X" con Agendar. Si elige fase con el Contacté pendiente, no manda levantarLead (cambiarFase ya deja el nombre). 8 toques, 0 hojas, 0-360 px, 4 pedidos.
- Banco: datos_falsos.py ahora tiene sinContactar (6 leads) y levantarLead; cambiarFase de un intaker deja su nombre (como anotarIntaker_). Nuevos flujo_sc.py (antes/después), flujo_sc_util.py y probar_sin_contactar.py (17/17: vuelve a los 2 s no marca, Deshacer no manda, ✓ sale a los 10 s o al salir, fase + Deshacer, Otra abre la ficha, error del motor vuelve a Sin contactar, Karim sin cambios).
- Regresión correr.py (Mica, Fran, Karim, Sol, Juan, Estefanía; 390 y 360): sin errores en main ni en la rama, mismas pestañas por rol, sin scroll horizontal nuevo.
- Para más adelante: el envío de plantillas por la API de WhatsApp (Wsp.gs, en otra conversación) encaja acá: el "Primer mensaje" se mandaría desde la misma fila y levantarLead ya se llama solo.

### 2026-11-15 — Agendar un lead (intakers)
- Por qué este: en USO (08-15/11) Agendar es donde más espera hay: 159 getData lentos desde "agendar" (más que cualquier otra pantalla), 35 desde "agendar>ficha", rachas de 5-8 getData lentos seguidos en agendar (Pri y Karim el 12/11), agendar 7,1 s promedio (máx 10,3 s), agendarNuevo 7,7 s, cambiarFase desde agendar 55 veces. Sin repetir: el único rediseño anterior es Sin contactar (08/11). La rama pendiente mejora/2026-11-15 toca 📤 Enviar, no la hoja de agendar; entran juntas sin choques (probado sin pushear).
- Antes (banco, Pri, 390 y 360; flujo_agendar.py): la hoja abre en "Mañana" aunque hoy haya lugar; hay que elegir día → horario → botón "Agendar: …"; después se abre la ficha de la consulta y hay que cerrarla para seguir. Sin Deshacer: un error se arregla con Reagendar (y "Me equivoqué al cargarlo"). Juan con disponibilidad solo lunes y miércoles: la hoja abre en un día "No marcó disponibilidad" y hay que probar días (3 toques de día). 1 pedido (agendar), 7,1 s promedio en el uso real, ya se veía agendada al instante.
- Después: "Lo antes posible · tocá y queda agendada" con los 3 primeros libres por persona (Hoy 11:30, Lun 9/11 14:00…); tocar = agendada, hoja cerrada, toast "📅 Agendada: … · Deshacer"; el pedido sale a los 6 s (o al salir de la app / Salir). Chips "Otro día" con número de libres (apagados en 0) y la hoja abre en el primer día con lugar. Reagendar, corregir y firmar: igual que antes (seleccionar + confirmar). Mismo pedido al motor; Deshacer antes de los 6 s no manda nada.
- Banco: nuevos pruebas/flujo_agendar.py (antes/después: toques, scroll, Deshacer, pedidos) y pruebas/probar_agendar.py (casos borde: rechazo del motor → vuelve a Por agendar y reabre la hoja con el aviso; salir de la app → sale enseguida; Actualizar mientras espera → no lo pisa y sale una sola vez; Reagendar → sigue con botón; Juan abre en Lun 9/11). Todo OK. Los 2 errores "reading 'update'" de probar_agendar.py son del registro del service worker bloqueado por el banco al simular volver a la app (pasa igual en main).
- Regresión correr.py (Mica, Fran, Karim, Juan, Sol, Estefanía; 390 y 360): main y rama con 0 errores, 0 pedidos fallidos, mismas pestañas por rol, sin elementos chicos ni scroll horizontal nuevos.
- Ojo: con el día y hora pedidos, en 360x640 el horario queda ~100 px más abajo (la caja "Lo antes posible" ocupa lugar); se llega con un poco de scroll.

### 2026-11-22 — Confirmaciones del día y mensaje previo (intakers)
- Por qué este: Sin contactar (08/11) y Agendar (15/11) ya se hicieron; de lo que queda, es lo que los intakers hacen todos los días con más toques repetidos. En USO (16-21/11): rachas de saveAction de Pri (11 en un lote, 5-8,8 s) y ~30-40 enviarWsp por día (Pri, Fran), muchos desde "tareas" y "tareas > ficha". No se leyó USO fila por fila (3.000 filas): se usaron los resúmenes de la nocturna más las últimas filas del 21/11.
- Ramas pendientes que tocan cerca: mejora/2026-11-21 (📤 de la ficha y la tarjeta: "Último: …"). No toca las filas de Tareas. Las 3 pendientes (-19, -20, -21) entran limpias junto con la nueva (merge local, sin pushear) y el flujo nuevo anda igual con las 4 juntas.
- Antes (banco, Fran, 390 y 360; pruebas/flujo_conf.py): "Mensaje del día" a 258 px de scroll (debajo de Sin contactar y Seguimiento). Por cada consulta oficial: 📤 → vista previa → Enviar (2 toques). Después de mandar la fila quedaba igual (📤 verde, solo un "📤 11:20" chico): no se veía a quién faltaba mandarle. 20 toques en total (1 Tareas + 10 envío + 2 💬 + 7 ✅).
- Después: 1 Tareas + 📤 Mandar 5 (en la barra de arriba) + Enviar 5 + 2 💬 + 7 ✅ = 12. Barra después: "5 esperan respuesta · 2 por 💬". Scroll 0.
- Casos borde (pruebas/probar_confirmaciones.py): destildar uno → "Enviar 4" y salen 4; el 📤 gris de uno ya mandado abre la vista previa con "Ya se mandó…" y "Enviar igual"; motor que rechaza uno y conexión cortada en otro → "Se mandaron 3 de 5. No sé si le llegó a Sofía (…uChat…). No salió: Diego: …" y Sofía queda "a revisar en uChat" fuera del lote; Mica sin Tareas ni barra; Karim con barra; WhatsApp oficial apagado → sin botón de mandar ("7 por 💬").
- Banco: datos_falsos.py → enviarWsp elige la plantilla por momento (turno/previo/hoy) como Wsp.gs (antes siempre el primer mensaje). Nuevos flujo_conf.py (antes/después) y probar_confirmaciones.py.
- Regresión correr.py (Mica, Fran, Karim, Sol, Juan, Estefanía; 390 y 360): main y rama 0 errores, mismas pestañas; la única diferencia del audit es el alto de Tareas (+170-185 px por la barra y el botón de sección).
- Idea para más adelante: que el motor marque solo "Confirmó" cuando el cliente toca el botón de la plantilla en WhatsApp (necesita Wsp.gs y uChat: no se propuso).


## 2026-11-23 (publicación, con el ok de Karim)
- main: mejora/2026-11-22-flujo-confirmaciones (0260c2b) y después -19, -20 y -21 juntas (5b6d0bf). Antes de publicar: probar_confirmaciones, probar_pasar_bc, probar_email, probar_wsp_tarjeta y correr.py (Mica, Pri, Sol, Karim, Juan, Estefanía) sobre las 4 juntas: 0 errores. GitHub Pages OK.
- Motor real: mejora-2026-11-19.json y mejora-2026-11-20.json aplicados juntos (pares verificados sobre el Código.gs real, sintaxis OK) y publicados como v92 en la misma implementación (antes v91). La API responde. El entorno de prueba sigue atrasado (no aplica el par de getData del -20).
