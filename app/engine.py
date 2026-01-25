from app.models import SessionLocal, Comercio, Turno

sessions = {}

def process_message(phone: str, text: str) -> str:
    if phone not in sessions:
        sessions[phone] = {"estado": "inicio", "data": {}}

    session = sessions[phone]
    estado = session["estado"]
    text_lower = text.lower().strip()

    # Comando cancelar
    if text_lower == "cancelar":
        sessions[phone]["estado"] = "cancelar_nombre"
        return "Decime tu nombre por favor"

    # Comando reprogramar
    if text_lower == "reprogramar":
        sessions[phone]["estado"] = "reprogramar_nombre"
        return "Decime tu nombre por favor"

    # Comando /setup
    if text.strip() == "/setup":
        sessions[phone]["estado"] = "setup_nombre"
        return "Perfecto 👍 ¿Cómo se llama tu negocio?"

    # Estado cancelar_nombre
    if estado == "cancelar_nombre":
        nombre_cliente = text

        db = SessionLocal()
        comercio = db.query(Comercio).filter_by(telefono_dueno=phone).first()

        if comercio:
            turno = db.query(Turno).filter_by(
                comercio_id=comercio.id,
                cliente_nombre=nombre_cliente
            ).order_by(Turno.id.desc()).first()

            if turno:
                fecha = turno.fecha
                hora = turno.hora
                db.delete(turno)
                db.commit()
                db.close()

                sessions[phone]["estado"] = "inicio"
                sessions[phone]["data"] = {}
                return f"Tu turno del {fecha} a las {hora} fue cancelado ✅"
            else:
                db.close()
                sessions[phone]["estado"] = "inicio"
                sessions[phone]["data"] = {}
                return "No encontré turnos a tu nombre 😕"
        else:
            db.close()
            sessions[phone]["estado"] = "inicio"
            sessions[phone]["data"] = {}
            return "No encontré turnos a tu nombre 😕"

    # Estado reprogramar_nombre
    if estado == "reprogramar_nombre":
        nombre_cliente = text

        db = SessionLocal()
        comercio = db.query(Comercio).filter_by(telefono_dueno=phone).first()

        if comercio:
            turno = db.query(Turno).filter_by(
                comercio_id=comercio.id,
                cliente_nombre=nombre_cliente
            ).order_by(Turno.id.desc()).first()

            if turno:
                db.delete(turno)
                db.commit()
                db.close()

                sessions[phone]["estado"] = "esperando_dia"
                sessions[phone]["data"] = {}
                return "Perfecto 👍 ¿Qué día te gustaría ahora?"
            else:
                db.close()
                sessions[phone]["estado"] = "inicio"
                sessions[phone]["data"] = {}
                return "No encontré turnos a tu nombre 😕"
        else:
            db.close()
            sessions[phone]["estado"] = "inicio"
            sessions[phone]["data"] = {}
            return "No encontré turnos a tu nombre 😕"

    # Estado setup_nombre
    if estado == "setup_nombre":
        sessions[phone]["data"]["nombre"] = text
        sessions[phone]["estado"] = "setup_horarios"
        return "¿Cuáles son tus horarios? (ej: Lun-Vie 9-19)"

    # Estado setup_horarios
    elif estado == "setup_horarios":
        sessions[phone]["data"]["horarios"] = text
        sessions[phone]["estado"] = "setup_servicios"
        return "Pasame tus servicios y precios así:\n\ncorte:8000\nbarba:5000"

    # Estado setup_servicios
    elif estado == "setup_servicios":
        servicios = text
        nombre = sessions[phone]["data"]["nombre"]
        horarios = sessions[phone]["data"]["horarios"]

        db = SessionLocal()
        comercio = db.query(Comercio).filter_by(telefono_dueno=phone).first()
        if comercio:
            comercio.nombre = nombre
            comercio.horarios = horarios
            comercio.servicios = servicios
        else:
            comercio = Comercio(
                telefono_dueno=phone,
                nombre=nombre,
                horarios=horarios,
                servicios=servicios
            )
            db.add(comercio)
        db.commit()
        db.close()

        sessions[phone]["estado"] = "inicio"
        sessions[phone]["data"] = {}
        return "Listo ✅ Tu negocio quedó configurado."

    # Estado inicio
    if estado == "inicio":
        db = SessionLocal()
        comercio = db.query(Comercio).filter_by(telefono_dueno=phone).first()
        db.close()

        sessions[phone]["estado"] = "esperando_servicio"
        if comercio:
            return f"Hola, soy Nordia de {comercio.nombre} 👋 ¿Querés sacar un turno? Respondé SI"
        else:
            return "Hola 👋 ¿Querés sacar un turno? Respondé SI"

    elif estado == "esperando_servicio":
        if "si" in text_lower:
            sessions[phone]["estado"] = "esperando_dia"
            return "¿Qué servicio te interesa?"
        else:
            sessions[phone]["estado"] = "inicio"
            return "Ok, cualquier cosa avisame"

    elif estado == "esperando_dia":
        sessions[phone]["data"]["servicio"] = text
        sessions[phone]["estado"] = "esperando_hora"
        return "¿Qué día te gustaría? (ej: lunes, martes)"

    elif estado == "esperando_hora":
        sessions[phone]["data"]["dia"] = text
        sessions[phone]["estado"] = "esperando_nombre"
        return "¿A qué hora? (ej: 10:00, 14:30)"

    elif estado == "esperando_nombre":
        hora = text
        dia = sessions[phone]["data"]["dia"]

        # Validar disponibilidad
        db = SessionLocal()
        comercio = db.query(Comercio).filter_by(telefono_dueno=phone).first()
        if comercio:
            turno_existente = db.query(Turno).filter_by(
                comercio_id=comercio.id,
                fecha=dia,
                hora=hora
            ).first()
            db.close()

            if turno_existente:
                return "Ese horario ya está ocupado 😕\n¿Querés probar con otra hora?"
        else:
            db.close()

        sessions[phone]["data"]["hora"] = hora
        sessions[phone]["estado"] = "confirmado"
        return "¿Cuál es tu nombre?"

    elif estado == "confirmado":
        nombre_cliente = text
        servicio = sessions[phone]["data"]["servicio"]
        dia = sessions[phone]["data"]["dia"]
        hora = sessions[phone]["data"]["hora"]

        # Guardar turno en DB
        db = SessionLocal()
        comercio = db.query(Comercio).filter_by(telefono_dueno=phone).first()
        if comercio:
            turno = Turno(
                comercio_id=comercio.id,
                cliente_nombre=nombre_cliente,
                cliente_telefono=phone,
                fecha=dia,
                hora=hora,
                servicio=servicio
            )
            db.add(turno)
            db.commit()
        db.close()

        sessions[phone]["estado"] = "inicio"
        sessions[phone]["data"] = {}
        return "Listo, tu turno quedó agendado 👍"

    return "No entendí, escribí HOLA para empezar"
