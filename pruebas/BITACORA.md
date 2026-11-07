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
| mejora/2026-11-07 | En 360px el nombre de la consulta usa hasta 2 renglones (antes se cortaba en todas las tarjetas); Cerrar (X) de las hojas a 44px; "Cambiar" y "Ver como otra persona" del pie con zona táctil de 45px | Pendiente de aprobar |

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
- 08/11 00:55: CONTEO DEL REPORTE SEMANAL CORREGIDO (motor v76, con el ok de Karim: "si arreglalo"). Problema: Laboral 2-8/11 mostraba 7 "vinieron y no firmaron" y la agenda tiene 4. Los 3 de más eran C puestos por intakers a agendados que no vinieron (Brenda Ramirez y Nahuel Paredes el 5/11, Juan Pablo Avendaño el 4/11 antes de su turno); además Celia Crespo (BC, pidió reagendar) contaba como no show.
  - Regla nueva desde el 4/11/2026 (cuando empezaron los resultados desde la app): un C después de un turno cuenta como "vino y no era caso" solo si la abogada lo cargó como resultado en la app; un C o BC que pone un intaker a un agendado no cuenta como que vino ni como no show. Antes del 4/11 sigue la regla vieja (igual que la planilla de KPIs).
  - La app marca cada resultado en la columna M del HISTORIAL ("Resultado cargado en la app": "Resultado app: No era caso (Mica)"); el script de KPIs lee hasta la L. Corrección del mismo día: misma línea, marca nueva. Deshacer: borra la línea.
  - Pruebas: probar_conteo_reporte.js con el HISTORIAL real de Laboral → 2/11: 5 firmaron, 4 vinieron y no firmaron, 0 no show, 1 reagendó (Juan Pablo); 26/10 sin cambios. En la copia del motor, PRUEBA_probarV76: mismo resultado con getReporte; "No es caso" desde la app deja la marca y cuenta; corregir a "No firmó" actualiza la misma línea; Deshacer deja el HISTORIAL como estaba.
  - Real: v76 publicado (mismo ID de implementación), código guardado verificado contra el local, la API responde. Pantalla sin cambios.
  - Pendiente con Karim: Maria Cecilia (ART, turno 5/11 15:30 con Mica, "no era caso" en la agenda) se cargó antes de la marca y ya no cuenta como que vino; se puede marcar a mano su línea del HISTORIAL de ART. La planilla de KPIs sigue con la regla vieja (Laboral 2/11 da 7 ahí).
