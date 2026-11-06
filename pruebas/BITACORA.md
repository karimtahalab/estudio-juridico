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
| mejora/2026-11-06 | Crear PIN: el paso "Repetí el PIN" ya no muestra "Son 4 números." en rojo antes de escribir (el PIN se mandaba dos veces); "Editar" del Resumen del caso con zona táctil de 44px | Pendiente de aprobar |

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
  - Chips de persona/rama a 40-44px de alto (sigue pendiente de la noche anterior).
