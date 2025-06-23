import threading
import time
import random
from datetime import datetime, timedelta
from faker import Faker

faker = Faker("es_ES")  # Español de España

def generar_dni():
    letras = "TRWAGMYFPDXBNJZSQVHLCKE"
    num = random.randint(10000000, 99999999)
    letra = letras[num % 23]
    return f"{num}{letra}"

def generar_pasaporte_o_nie():
    return f"{faker.random_uppercase_letter()}{faker.random_number(digits=7)}{faker.random_uppercase_letter()}"

def iniciar_automatizacion(app):
    def insertar_datos():
        inicio = time.time()
        duracion = 20 * 60  # 20 minutos
        intervalo = 15  # segundos
        contador = 1

        while time.time() - inicio < duracion:
            print(f"[{contador}] Insertando cliente y reserva...")

            # CLIENTE
            app.cust_details()
            cliente = app.app
            campos = cliente.campos

            nombre_completo = faker.name()
            movil = faker.msisdn()[0:9]
            email = faker.email()
            direccion = faker.street_address()
            nacionalidad = faker.current_country()
            cp = faker.postcode()
            doc_tipo = random.choice(["DNI", "Pasaporte", "NIE"])
            num_doc = generar_dni() if doc_tipo == "DNI" else generar_pasaporte_o_nie()
            ref = f"AUTO{contador:04d}"

            campos["Ref cliente"].delete(0, "end")
            campos["Ref cliente"].insert(0, ref)

            campos["Nombre cliente"].delete(0, "end")
            campos["Nombre cliente"].insert(0, nombre_completo)

            campos["Género"].set(random.choice(["Masculino", "Femenino", "Otro"]))

            campos["Código Postal"].delete(0, "end")
            campos["Código Postal"].insert(0, cp)

            campos["Móvil"].delete(0, "end")
            campos["Móvil"].insert(0, movil)

            campos["Email"].delete(0, "end")
            campos["Email"].insert(0, email)

            campos["Nacionalidad"].delete(0, "end")
            campos["Nacionalidad"].insert(0, nacionalidad)

            campos["Tipo de Documento"].set(doc_tipo)

            campos["Número de Documento"].delete(0, "end")
            campos["Número de Documento"].insert(0, num_doc)

            campos["Dirección"].delete(0, "end")
            campos["Dirección"].insert(0, direccion)

            cliente.insertar_cliente()

            # RESERVA
            app.room_details()
            reserva = app.app
            datos = reserva.datos

            datos["Contacto del Cliente"].delete(0, "end")
            datos["Contacto del Cliente"].insert(0, movil)

            personas = random.randint(1, 4)
            datos["Nº de Personas"].delete(0, "end")
            datos["Nº de Personas"].insert(0, str(personas))

            entrada = datetime.today() + timedelta(days=random.randint(0, 3))
            salida = entrada + timedelta(days=random.randint(1, 5))
            datos["Fecha de Entrada"].set_date(entrada)
            datos["Fecha de Salida"].set_date(salida)

            tipo = random.choice(["Estándar", "Familiar", "Suite"])
            habitacion_id = f"{random.randint(101, 310)} {tipo}"
            datos["Habitación"].set(habitacion_id)

            datos["Comida"].set(random.choice(["Desayuno", "Media pensión", "Pensión completa"]))

            reserva.calcular_dias()
            reserva.insertar_reserva()

            contador += 1
            time.sleep(intervalo)

        print("✅ Finalizado: Clientes y reservas")

    threading.Thread(target=insertar_datos, daemon=True).start()
