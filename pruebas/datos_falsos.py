# -*- coding: utf-8 -*-
"""DATOS DE PRUEBA — TODO ES INVENTADO.
Nombres, teléfonos y casos son ficticios. Nada de acá sale de las planillas reales.
El "servidor falso" (FakeApi) responde cada fn del motor con la forma que espera index.html
y guarda los cambios en memoria para que la pantalla los refleje.
"""
import copy, datetime as dt

ES_PRUEBA = True  # marca: datos de prueba

HOY = dt.date(2026, 11, 5)  # jueves (el script fija el reloj del navegador a este día)
def D(n):
    d = HOY + dt.timedelta(days=n)
    return d.isoformat()

EQUIPO = [
    {"nombre": "Mica", "rol": "abogada", "tiene": True},
    {"nombre": "Cele", "rol": "abogada", "tiene": True},
    {"nombre": "Sol", "rol": "abogada", "tiene": True},
    {"nombre": "Estefanía", "rol": "abogada", "tiene": True},
    {"nombre": "Juan", "rol": "abogada", "tiene": True},
    {"nombre": "Fran", "rol": "intaker", "tiene": True},
    {"nombre": "Pri", "rol": "intaker", "tiene": False},
    {"nombre": "Karim", "rol": "admin", "tiene": True},
    {"nombre": "Julián", "rol": "admin", "tiene": True},
]
RAMAS_POR_PERSONA = {"Mica": ["ART", "LABORAL"], "Cele": ["ART", "LABORAL"], "Estefanía": ["LABORAL"], "Juan": ["TRANSITO"]}
ABOGADAS = ["Mica", "Cele", "Estefanía", "Juan"]

PERMISOS = {
    "Mica": {"agenda": ["ART", "LABORAL"], "agendar": True, "leads": ["ART", "LABORAL"]},
    "Cele": {"agenda": ["ART", "LABORAL"], "agendar": True, "leads": ["ART", "LABORAL"]},
    "Sol": {"agenda": ["ART", "LABORAL"], "agendar": True, "leads": ["ART", "LABORAL"]},
    "Estefanía": {"agenda": ["LABORAL"], "agendar": False, "leads": []},
    "Juan": {"agenda": ["TRANSITO"], "agendar": True, "leads": ["TRANSITO"]},
    "Fran": {"agenda": ["ART", "LABORAL", "TRANSITO"], "agendar": True, "leads": ["ART", "LABORAL", "TRANSITO"]},
    "Pri": {"agenda": ["ART", "LABORAL", "TRANSITO"], "agendar": True, "leads": ["ART", "LABORAL", "TRANSITO"]},
    "Karim": {"agenda": ["ART", "LABORAL", "TRANSITO"], "agendar": True, "leads": ["ART", "LABORAL", "TRANSITO"]},
    "Julián": {"agenda": ["ART", "LABORAL", "TRANSITO"], "agendar": True, "leads": ["ART", "LABORAL", "TRANSITO"]},
}

RES_LARGO = ("[PRUEBA] Trabajador de depósito, 34 años. Se lesionó la espalda levantando cajas el 12/09. "
             "La ART le dio el alta a las 3 semanas pero sigue con dolor y no puede hacer fuerza. "
             "Tiene estudios (resonancia) y certificado del traumatólogo particular. "
             "Lo quieren reincorporar en el mismo puesto. Pregunta si puede reclamar incapacidad y qué pasa si lo despiden. "
             "Cobra en blanco, 6 años de antigüedad.")

def _lead(i, nombre, tel, rama, fecha, hora, abogada, fase="A", confPrev="", confDia="", resumen="", **kw):
    l = {"id": "P%03d" % i, "row": 100 + i, "nombre": nombre, "tel": tel, "email": "", "rama": rama,
         "fecha": fecha, "hora": hora, "abogada": abogada, "fase": fase, "confPrev": confPrev, "confDia": confDia,
         "resumen": resumen, "ingreso": D(-3), "intaker": "Fran", "comentarios": [], "info": [], "internas": [],
         "motivo": "", "detalle": ""}
    l.update(kw)
    return l

def sin_contactar():
    """Leads nuevos sin nombre de intaker en la primera columna (ficticios)."""
    xs = [
        _lead(71, "Brenda Nueva Ficticia", "2615550171", "LABORAL", "", "", "", fase="", ingreso=D(0)),
        _lead(72, "Gustavo Sin Contactar Demo", "2615550172", "ART", "", "", "", fase="", ingreso=D(-1)),
        _lead(73, "Lorena Prueba Tránsito", "2615550173", "TRANSITO", "", "", "", fase="", ingreso=D(-2)),
        _lead(74, "Hernán Lead Inventado", "2615550174", "LABORAL", "", "", "", fase="", ingreso=D(0)),
        _lead(75, "Valeria ART Demo", "2615550175", "ART", "", "", "", fase="", ingreso=D(0)),
        _lead(76, "Carlos Viejo C Test", "2615550176", "LABORAL", "", "", "", fase="C", ingreso=D(-4)),
    ]
    for l in xs: l["intaker"] = ""; l["levanto"] = ""
    return xs


def leads_agendados():
    return [
        _lead(1, "Rubén Prueba Gómez", "2615550101", "ART", D(0), "09:00", "Mica", fase="Agendado", confPrev="Confirmó", confDia="Confirmó", resumen=RES_LARGO,
              info=[{"label": "¿Qué pasó?", "text": "Me lastimé en el trabajo (dato de prueba)"}, {"label": "¿Tenés ART?", "text": "Sí"}],
              comentarios=[{"label": "Sol · 03/11", "text": "Pedir los estudios antes de la consulta (prueba)."}]),
        _lead(2, "Carla Ficticia Díaz", "2615550102", "LABORAL", D(0), "10:00", "Estefanía", fase="Agendado", confPrev="Confirmó", confDia="No respondió", resumen="[PRUEBA] Despido sin causa, le deben 2 meses."),
        _lead(3, "Marcos Inventado Ruiz", "2615550103", "ART", D(0), "11:30", "Cele", fase="Agendado", confPrev="No respondió", resumen=""),
        _lead(4, "Lucía Demo Ortiz", "2615550104", "LABORAL", D(0), "12:00", "Mica", fase="Agendado", confPrev="Confirmó", confDia="Confirmó", resumen="[PRUEBA] Trabaja en negro hace 2 años en un comercio."),
        _lead(5, "Hernán Test Molina", "2615550105", "TRANSITO", D(0), "10:30", "Juan", fase="Agendado", confPrev="Confirmó", confDia="Confirmó", resumen="[PRUEBA] Choque en moto, el otro auto cruzó en rojo. Tiene denuncia y fotos."),
        _lead(6, "Paula Ejemplo Sosa", "2615550106", "TRANSITO", D(0), "16:00", "Juan", fase="Agendado", confPrev="Confirmó", resumen="[PRUEBA] Peatón atropellada, lesión en rodilla."),
        _lead(7, "Diego Simulado Paz", "2615550107", "ART", D(0), "15:00", "Mica", fase="Agendado", confPrev="Confirmó", resumen="[PRUEBA] Accidente in itinere."),
        _lead(8, "Sofía Prueba Luna", "2615550108", "LABORAL", D(0), "17:30", "Estefanía", fase="Agendado", confPrev="", resumen="[PRUEBA] Acoso laboral."),
        _lead(9, "Jorge Falso Vega", "2615550109", "ART", D(1), "09:30", "Cele", fase="Agendado", confPrev="", resumen="[PRUEBA] Enfermedad profesional: hernia de disco."),
        _lead(10, "Ana Inventada Ríos", "2615550110", "LABORAL", D(1), "11:00", "Mica", fase="Reagenda", confPrev="Confirmó", resumen="[PRUEBA] Reagendó: no consiguió quien cuide a los chicos."),
        _lead(11, "Tomás Demo Castro", "2615550111", "TRANSITO", D(1), "10:00", "Juan", fase="Agendado", confPrev="No respondió", resumen=""),
        _lead(12, "Valeria Test Núñez", "2615550112", "LABORAL", D(1), "12:30", "Estefanía", fase="Agendado", resumen="[PRUEBA] Le cambiaron el horario sin aviso."),
        _lead(13, "Ezequiel Prueba Ibarra", "2615550113", "ART", D(4), "10:00", "Mica", fase="Agendado", resumen="[PRUEBA] Corte en la mano con amoladora."),
        _lead(14, "Romina Ficticia Peña", "2615550114", "ART", D(-1), "16:00", "Cele", fase="Caso en proceso", confPrev="Confirmó", confDia="Confirmó", resumen="[PRUEBA] Firmó ayer."),
    ]

def por_agendar():
    return [
        _lead(50, "Gabriel Sin Día Prueba", "2615550150", "ART", "", "", "Mica", fase="Reagenda", sinDia=True, resumen="[PRUEBA] Pidió reagendar sin día."),
        _lead(51, "Mariela Nueva Demo", "2615550151", "LABORAL", "", "", "", fase="", ingreso=D(0), resumen=""),
        _lead(52, "Oscar Lead Test", "2615550152", "ART", "", "", "", fase="A", ingreso=D(-1)),
        _lead(53, "Patricia Llamar Prueba", "2615550153", "TRANSITO", "", "", "", fase="Llamada pendiente", ingreso=D(-2)),
        _lead(54, "Nicolás Fase B Demo", "2615550154", "LABORAL", "", "", "", fase="B", ingreso=D(-6)),
        _lead(55, "Silvina Tránsito Test", "2615550155", "TRANSITO", "", "", "", fase="A", ingreso=D(0)),
        _lead(56, "Ramiro ART Ficticio", "2615550156", "ART", "", "", "", fase="", ingreso=D(-10)),
    ]

OTRAS = {
    "Seguimiento": [_lead(70, "Elena Seguimiento Prueba", "2615550170", "LABORAL", D(-7), "10:00", "Mica", fase="Seguimiento")],
    "C": [_lead(71, "Fabián No Caso Demo", "2615550171", "ART", D(-9), "11:00", "Cele", fase="C")],
    "BC": [], "Repetido": [], "Numero incorrecto": [], "No show": [_lead(72, "Irene No Vino Test", "2615550172", "TRANSITO", D(-2), "12:00", "Juan", fase="No show")],
    "Caso en proceso": [],
}

# WhatsApp oficial FALSO: catálogo y textos inventados para el banco (no se manda nada)
WSP_CATALOGO = [
    {"tpl": "inicio_accidente_art", "label": "Primer mensaje (accidente ART)", "grupo": "Primer contacto", "vars": ["nombre", "firma"], "req": "", "ramas": ["ART"]},
    {"tpl": "inicio_enfermedad_art", "label": "Primer mensaje (enfermedad ART)", "grupo": "Primer contacto", "vars": ["nombre", "firma"], "req": "", "ramas": ["ART"]},
    {"tpl": "inicio_laboral", "label": "Primer mensaje (Laboral)", "grupo": "Primer contacto", "vars": ["nombre", "firma"], "req": "", "ramas": ["LABORAL"]},
    {"tpl": "consulta_tiempo_trabajado", "label": "Cuánto tiempo trabajó", "grupo": "Primer contacto", "vars": ["nombre"], "req": "", "ramas": ["LABORAL"], "alterno": True},
    {"tpl": "seguimiento_sin_respuesta_1", "label": "Sin respuesta 1", "grupo": "Seguimiento", "vars": ["nombre"], "req": "", "serie": 1},
    {"tpl": "confirmacion_consulta", "label": "Confirmación de la consulta", "grupo": "Consulta", "vars": ["nombre", "diaYFecha", "hora"], "req": "turno"},
    {"tpl": "recordatorio_consulta_manana", "label": "Recordatorio: mañana", "grupo": "Consulta", "vars": ["nombre", "hora"], "req": "manana"},
    {"tpl": "recordatorio_consulta_hoy", "label": "Recordatorio: hoy", "grupo": "Consulta", "vars": ["nombre", "hora"], "req": "hoy"},
]
WSP_TEXTOS = {o["tpl"]: "[PRUEBA] Hola {{1}}, " + o["label"].lower() + " ({{2}} {{3}}). Texto inventado del banco." for o in WSP_CATALOGO}

def wsp_datos(who):
    return {"activo": True, "prueba": False, "yo": who, "firma": who + " (prueba)", "horas": 20, "catalogo": copy.deepcopy(WSP_CATALOGO),
            "textos": dict(WSP_TEXTOS), "envios": {}, "abogadas": {"Mica": "Dra. Mica", "Cele": "Dra. Cele"}}

class FakeApi:
    def __init__(self):
        self.leads = leads_agendados()
        self.pa = por_agendar()
        self.sc = sin_contactar()
        self.bloqueos = [{"id": "B1", "fecha": D(0), "abogada": "Cele", "desde": "13:00", "hasta": "14:00", "todoDia": False, "aclaracion": "Trámite en tribunales (prueba)"}]
        self.disp = {"modos": {}, "fijo": {}, "fechas": {}}
        self.pin_bloq = {"Julián": True}
        self.sin_fake = set()
        self.calls = []
        self.seq = 900
        self.wsp_enviados = []  # WhatsApp que se "habrían" mandado (todo falso)

    def _quien(self, arg):
        t = (arg or {}).get("tok", "")
        return t[5:] if t.startswith("fake-") else None

    def _ve(self, who, l):
        p = PERMISOS.get(who, {})
        ag = p.get("agenda", [])
        if l.get("rama") not in ag: return False
        if who == "Estefanía": return l.get("abogada") == "Estefanía"
        return True

    def _abogadas(self, who):
        # Como el motor: quien ve una sola agenda (Juan, Estefanía) recibe solo la suya
        if who in ABOGADAS and who in ("Juan", "Estefanía"): return [who]
        ag = PERMISOS.get(who, {}).get("agenda", [])
        return [a for a in ABOGADAS if any(r in ag for r in RAMAS_POR_PERSONA.get(a, []))]

    def _find(self, i):
        for xs in [self.leads, self.pa, self.sc] + list(OTRAS.values()):
            for l in xs:
                if l["id"] == i: return l
        return None

    def get_data(self, who):
        eq = copy.deepcopy(EQUIPO)
        d = {
            "__prueba": True, "modoPrueba": False, "user": {"name": who},
            "permisos": PERMISOS.get(who, {}),
            "equipo": eq, "abogadas": self._abogadas(who), "ramasPorPersona": RAMAS_POR_PERSONA,
            "leads": [l for l in self.leads if self._ve(who, l)],
            "porAgendar": [l for l in self.pa + [x for x in self.sc if x["fase"] in ("", "A", "B", "Llamada pendiente")] if l["rama"] in PERMISOS.get(who, {}).get("leads", [])],
            "bloqueos": self.bloqueos, "horario": {"desde": "09:00", "hasta": "19:00"}, "duracion": 30,
            "disponibilidad": self.disp, "dispRango": {"desde": "08:00", "hasta": "21:00"}, "modoDefecto": "bloqueos",
            "motivos": ["Lo va a pensar", "Le pareció caro", "Ya tiene abogado", "No tiene los papeles", "Otro"],
            "origenes": ["WhatsApp", "Instagram", "Facebook", "Referido", "Otro"],
            "respuestas": {"criterio": ["Es caso", "No es caso", "Falta info"], "llamada": ["Lo llamé", "No atendió"]},
            "feriados": [], "internas": {"criterio": {"ART": ["Mica", "Cele"], "LABORAL": ["Mica", "Estefanía"], "TRANSITO": ["Juan"]},
                                         "llamada": {"ART": ["Mica"], "LABORAL": ["Mica"], "TRANSITO": ["Juan"]}, "telefonos": {}},
            "sinContactar": [copy.deepcopy(l) for l in self.sc if l["rama"] in PERMISOS.get(who, {}).get("leads", []) and next((e["rol"] for e in EQUIPO if e["nombre"] == who), "") in ("intaker", "admin")],
            "paraMi": [], "visto": None, "diasPorAgendar": 90, "duplicados": [],
        }
        if who in ("Karim", "Julián"):
            d["pines"] = [{"nombre": e["nombre"], "tiene": e["tiene"], "bloqueado": self.pin_bloq.get(e["nombre"], False), "fijo": e["nombre"] == "Julián"} for e in eq]
            d["finAcceso"] = True; d["finRamas"] = ["ART", "LABORAL", "TRANSITO"]; d["finModo"] = {"ART": "full", "LABORAL": "full", "TRANSITO": "full"}; d["finPin"] = {"tiene": True, "bloqueado": False}
        return d

    def handle(self, fn, arg):
        """Devuelve (ok, data_o_error)."""
        arg = arg or {}
        who = self._quien(arg) or arg.get("who")
        self.calls.append(fn)
        if fn == "equipoLogin": return True, copy.deepcopy(EQUIPO)
        if fn == "tienePin": return True, next((e["tiene"] for e in EQUIPO if e["nombre"] == arg.get("nombre")), False)
        if fn in ("login", "crearPin"):
            n = arg.get("nombre")
            if self.pin_bloq.get(n): return False, "PIN bloqueado por intentos. Pedile a Karim que lo desbloquee."
            if fn == "login" and arg.get("pin") != "1234": return False, "PIN incorrecto. Te quedan 4 intentos."
            return True, {"tok": "fake-" + n, "nombre": n}
        if not who: return False, "AUTH|Tu sesión venció. Poné tu PIN de nuevo."
        if fn == "logout": return True, {}
        if fn == "getData": return True, self.get_data(who)
        if fn == "leadsDeFase":
            if arg.get("todas"): return True, {"porFase": {f: {"leads": v, "total": len(v)} for f, v in OTRAS.items()}}
            if arg.get("q") is not None or arg.get("buscar"): return True, {"leads": [], "total": 0}
            v = OTRAS.get(arg.get("fase"), []); return True, {"leads": v, "total": len(v)}
        if fn in ("saveAction", "deshacerResultado", "cambiarFase", "editarDatos", "agregarNota", "agendar", "derivar", "reagendaSinDia"):
            l = self._find(arg.get("id"))
            if not l: return False, "No encontré esa consulta (prueba)."
            if fn == "saveAction":
                if arg.get("action") == "resultado":
                    l["fase"] = {"firmo": "Caso en proceso", "nofirmo": "Seguimiento", "novino": "No show", "nocaso": "C"}.get(arg.get("value"), l["fase"])
                    l["motivo"] = arg.get("motivo") or ""; l["detalle"] = arg.get("detalle") or ""
                else: l[arg.get("action")] = arg.get("value")
            elif fn == "deshacerResultado": l.update({k: arg.get(k, "") for k in ("fase", "motivo", "detalle")})
            elif fn == "cambiarFase":
                l["fase"] = arg.get("fase")
                # Como anotarIntaker_ del motor: el primer cambio de fase de un intaker deja su nombre
                if who in ("Fran", "Pri") and l in self.sc: self.sc.remove(l); l["intaker"] = who; self.pa.insert(0, l)
            elif fn == "editarDatos": l.update({k: arg[k] for k in ("nombre", "tel", "email") if arg.get(k) is not None})
            elif fn == "agregarNota": l["comentarios"] = l["comentarios"] + [{"label": "%s · hoy" % who, "text": arg.get("texto", "")}]
            elif fn == "agendar":
                l.update({"fecha": arg.get("fecha"), "hora": arg.get("hora"), "abogada": arg.get("abogada") or l["abogada"]})
                if l.get("sinDia"): l["sinDia"] = False
                if l["fase"] in ("", "A", "B", "Llamada pendiente"): l["fase"] = "Agendado"
                if l in self.pa: self.pa.remove(l); self.leads.append(l)
            elif fn == "derivar":
                l["abogada"] = arg.get("a")
                if arg.get("hora"): l["hora"] = arg["hora"]
            elif fn == "reagendaSinDia":
                l.update({"fase": "Reagenda", "fecha": "", "hora": ""});
                if l in self.leads: self.leads.remove(l); self.pa.insert(0, l)
            return True, copy.deepcopy(l)
        if fn == "saveResumenes":
            out = []
            for it in arg.get("items", []):
                l = self._find(it.get("id"))
                if l: l["resumen"] = it.get("texto", ""); out.append(copy.deepcopy(l))
            return True, {"leads": out, "faltan": []}
        if fn == "saveVisto": return True, {}
        if fn == "levantarLead":
            l = self._find(arg.get("id"))
            if not l: return False, "No encontré esa consulta (prueba)."
            if who not in ("Fran", "Pri"): return False, "Esto lo marcan los intakers (Fran o Pri)."
            if l.get("intaker"): return True, {"lead": copy.deepcopy(l), "ya": l["intaker"]}
            l["intaker"] = who
            if l in self.sc:
                self.sc.remove(l)
                if l["fase"] in ("", "A", "B", "Llamada pendiente"): self.pa.insert(0, l)
            return True, {"lead": copy.deepcopy(l), "ya": ""}
        if fn == "saveBloqueo":
            self.seq += 1; b = {k: arg.get(k) for k in ("fecha", "desde", "hasta", "todoDia", "abogada", "aclaracion")}; b["id"] = "B%d" % self.seq
            self.bloqueos.append(b); return True, self.bloqueos
        if fn == "deleteBloqueo":
            self.bloqueos = [b for b in self.bloqueos if b["id"] != arg.get("id")]; return True, self.bloqueos
        if fn == "saveDisponibilidad": return True, self.disp
        if fn == "agendarNuevo":
            self.seq += 1
            l = _lead(self.seq, arg.get("nombre", ""), arg.get("tel", ""), arg.get("rama", "ART"), arg.get("fecha", ""), arg.get("hora", ""), arg.get("abogada", ""), fase=arg.get("fase") or "Agendado", ingreso=D(0))
            (self.pa if arg.get("sinAgendar") else self.leads).append(l); return True, {"lead": copy.deepcopy(l)}
        if fn == "pedirInterna":
            l = self._find(arg.get("id")); return True, {"lead": copy.deepcopy(l), "tel": ""}
        if fn == "responderInterna":
            l = self._find(arg.get("id")); return True, {"lead": copy.deepcopy(l)}
        if fn == "derivarMarca":
            l = self._find(arg.get("id")); return True, {"lead": copy.deepcopy(l)}
        if fn in ("resetPin", "resetFinPin", "desbloquearPin"):
            if fn == "desbloquearPin": self.pin_bloq.pop(arg.get("nombre"), None)
            return True, {"pines": self.get_data(who).get("pines", [])}
        if fn == "wspDatos":
            return True, wsp_datos(who)
        if fn in ("wspVista", "wspOpciones"):
            return False, "(prueba) %s no tiene respuesta falsa: la pantalla arma todo con wspDatos." % fn
        if fn == "enviarWsp":
            l = self._find(arg.get("id"))
            if not l: return False, "No encontré esa consulta (prueba)."
            tpl = arg.get("tpl") or ("inicio_laboral" if l["rama"] == "LABORAL" else "inicio_accidente_art")
            self.wsp_enviados.append({"id": l["id"], "tel": l.get("tel"), "tpl": tpl, "quien": who})
            print("[harness] WhatsApp FALSO (no sale nada): a %s (%s) plantilla %s, por %s" % (l.get("nombre"), l.get("tel"), tpl, who), flush=True)
            levanto = False
            if l in self.sc and who in ("Fran", "Pri", "Karim", "Julián"):
                self.sc.remove(l); l["intaker"] = l.get("intaker") or who; levanto = True
                if l["fase"] in ("", "A", "B", "Llamada pendiente"): self.pa.insert(0, l)
            return True, {"ok": True, "label": next((o["label"] for o in WSP_CATALOGO if o["tpl"] == tpl), tpl), "tpl": tpl, "prueba": False, "levanto": levanto, "lead": copy.deepcopy(l)}
        if fn == "getReporte":
            return True, {"__prueba": True, "filas": [], "semana": arg.get("semana")}
        if fn == "getEstudios": return True, {"lista": [], "puedeSubir": True, "maxMB": 10}
        if fn == "getCreativos": return True, {"ramas": []}
        if fn in ("finPinEntrar",): return True, {"ftok": "fake-fin", "creado": False}
        self.sin_fake.add(fn)
        print("[harness] fn SIN respuesta falsa:", fn, flush=True)
        return True, {}
