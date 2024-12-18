from funciones_gestion import *
from funciones_huesped import *
from funciones_hotel import *
from funciones_poi import *
from funciones_amenity import *
import random
from datetime import datetime, timedelta
from dateutil import relativedelta
from dateutil.relativedelta import relativedelta


# Lista de datos de los huéspedes a crear
def crear_huespedes():
    huespedes = [
        {"nombre": "Juan", "apellido": "Perez", "direccion": "Calle Falsa 123", "telefono": "123456789", "email": "juan.perez@example.com"},
        {"nombre": "Ana", "apellido": "Garcia", "direccion": "Avenida Siempre Viva 456", "telefono": "987654321", "email": "ana.garcia@example.com"},
        {"nombre": "Carlos", "apellido": "Lopez", "direccion": "Boulevard Principal 789", "telefono": "111222333", "email": "carlos.lopez@example.com"},
        {"nombre": "Marta", "apellido": "Martinez", "direccion": "Carrera 12 #34-56", "telefono": "444555666", "email": "marta.martinez@example.com"},
        {"nombre": "Luis", "apellido": "Gomez", "direccion": "Calle 7 #8-9", "telefono": "777888999", "email": "luis.gomez@example.com"}
    ]

    # Crear los huéspedes usando la función alta_huesped
    for huesped in huespedes:
        resultado = alta_huesped(
            huesped["nombre"], 
            huesped["apellido"], 
            huesped["direccion"], 
            huesped["telefono"], 
            huesped["email"]
        )
        print(resultado)
def crear_pois():
    pois = [
        {"nombre": "Obelisco", "detalle": "Monumento icónico en Buenos Aires", "direccion": "Av. 9 de Julio", "tipo": "Monumento"},
        {"nombre": "Puente de la Mujer", "detalle": "Puente moderno en Puerto Madero", "direccion": "Aime Paine 500", "tipo": "Atracción"},
        {"nombre": "Cementerio de la Recoleta", "detalle": "Cementerio histórico con arquitectura impresionante", "direccion": "Junín 1760", "tipo": "Histórico"},
        {"nombre": "Plaza Serrano", "detalle": "Plaza popular en el barrio de Palermo", "direccion": "Armenia 5000", "tipo": "Espacio Público"},
        {"nombre": "Mercado de San Telmo", "detalle": "Mercado tradicional en el barrio de San Telmo", "direccion": "Humberto Primo 831", "tipo": "Mercado"},
        {"nombre": "Teatro Colón", "detalle": "Famoso teatro de ópera en el centro de Buenos Aires", "direccion": "Cerrito 628", "tipo": "Teatro"},
        {"nombre": "Plaza de Mayo", "detalle": "Histórica plaza frente a la Casa Rosada", "direccion": "Av. Hipólito Yrigoyen s/n", "tipo": "Plaza"},
        {"nombre": "Museo Nacional de Bellas Artes", "detalle": "Museo de arte con una amplia colección de obras", "direccion": "Libertador 1473", "tipo": "Museo"},
        {"nombre": "Barrio Chino", "detalle": "Colorido barrio con tiendas y restaurantes chinos", "direccion": "Arribeños 2240", "tipo": "Barrio"},
        {"nombre": "Jardín Botánico", "detalle": "Jardín botánico con variedad de plantas y esculturas", "direccion": "Av. Santa Fe 3870", "tipo": "Parque"},
        {"nombre": "Planetario Galileo Galilei", "detalle": "Planetario con exhibiciones de astronomía", "direccion": "Sarmiento 3000", "tipo": "Ciencia"},
        {"nombre": "La Bombonera", "detalle": "Estadio de fútbol del club Boca Juniors", "direccion": "Brandsen 805", "tipo": "Estadio"},
        {"nombre": "Palacio Barolo", "detalle": "Edificio histórico inspirado en la Divina Comedia", "direccion": "Av. de Mayo 1370", "tipo": "Arquitectura"},
        {"nombre": "Bosques de Palermo", "detalle": "Parque grande con lagos y áreas recreativas", "direccion": "Av. Infanta Isabel 1500", "tipo": "Parque"}
    ]

    for poi in pois:
        resultado = alta_poi(
            poi["nombre"], 
            poi["detalle"], 
            poi["direccion"], 
            poi["tipo"]
        )
        print(resultado)
        
def crear_hoteles():
    hoteles = [
        {"nombre": "Hotel Puerto Madero", "direccion": "Dique 1, Puerto Madero", "telefono": "987654321", "email": "puertomadero@example.com"},
        {"nombre": "Hotel Obelisco", "direccion": "Cerrito 286", "telefono": "123456789", "email": "obelisco@example.com" },
        {"nombre": "Hotel Recoleta", "direccion": "Av. Alvear 1891", "telefono": "111222333", "email": "recoleta@example.com"},
        {"nombre": "Hotel Palermo", "direccion": "Honduras 4881", "telefono": "444555666", "email": "palermo@example.com"},
        {"nombre": "Hotel San Telmo", "direccion": "Defensa 1047", "telefono": "777888999", "email": "santelmo@example.com"}
    ]

    for hotel in hoteles:
        resultado = alta_hotel(
            hotel["nombre"], 
            hotel["direccion"], 
            hotel["telefono"], 
            hotel["email"], 
        )
         

def crear_amenitys():
    amenitys = [
        "Sales de Baño",
        "Chocolates",
        "Copa de Bienvenida",
        "Mini Bar",
        "Toallas Extra",
        "Bata de Baño",
        "Desayuno en Habitación",
        "Almohadas Adicionales",
        "Wi-Fi Gratuito"
    ]

    for nombre in amenitys:
        resultado = alta_amenity(nombre)


def crear_habitaciones():
    try:
        # Obtener la lista de hoteles
        hoteles = mostrar_hoteles()
        if not hoteles:
            print("No hay hoteles disponibles para crear habitaciones.")
            return

        # Obtener la lista de amenities
        amenitys = traer_amenitys()
        if not amenitys:
            print("No hay amenities disponibles para asignar a las habitaciones.")
            return
        
        tipos_habitacion = ["Suite", "Doble", "Simple"]  # Tipos de habitación disponibles

        for hotel in hoteles:
            id_hotel = hotel["id"]
            nombre_hotel = hotel["nombre"].replace(" ", "_")

            for i in range(2):  # Crear 5 habitaciones por hotel
                # Generar un nuevo ID de habitación
                nuevo_id = i + 1
                id_habitacion = f"{nombre_hotel}_{nuevo_id}"

                # Seleccionar un tipo de habitación aleatorio
                tipo_habitacion = random.choice(tipos_habitacion)

                # Crear la habitación y relacionarla con el hotel
                query = """
                    MATCH (h:Hotel {id_hotel: $id_hotel})
                    CREATE (h)-[:TIENE]->(:Habitacion {id_habitacion: $id_habitacion, tipo_habitacion: $tipo_habitacion})
                """
                graph.run(query, id_hotel=id_hotel, id_habitacion=id_habitacion, tipo_habitacion=tipo_habitacion)
                print(f"Habitación '{id_habitacion}' de tipo '{tipo_habitacion}' creada exitosamente en el hotel '{nombre_hotel}'.")

                # Asignar entre 0 y 2 amenities a la habitación
                num_amenities = random.randint(0, 2)  # Número aleatorio de amenities
                selected_amenities = random.sample(amenitys, num_amenities)  # Seleccionar amenities aleatorios

                for amenity in selected_amenities:
                    # Crear la relación entre la habitación y el amenity
                    query = """
                        MATCH (a:Amenity {id_amenity: $id_amenity})
                        MATCH (h:Habitacion {id_habitacion: $id_habitacion})
                        CREATE (h)-[:INCLUYE]->(a)
                    """
                    graph.run(query, id_habitacion=id_habitacion, id_amenity=amenity["id"])
                    print(f"Amenity con ID {amenity['id']} asignado a la habitación {id_habitacion} exitosamente.")

    except Exception as e:
        print(f"Error al crear las habitaciones: {e}")



def crear_reservas():
    # Lista de huéspedes
    huespedes = [1, 2, 3, 4, 5]  # IDs de los huéspedes generados previamente
    habitaciones = ["Hotel_Puerto_Madero_1", "Hotel_Puerto_Madero_2", "Hotel_Recoleta_1"]  # IDs de habitaciones creadas
    reservas = []

    # Fechas hardcodeadas para las reservas
    fechas_reservas = [
        ("2025-11-05", "2025-11-10"),
        ("2025-11-11", "2025-11-15"),
        ("2025-11-16", "2025-11-20"),
        ("2025-11-21", "2025-11-25"),
        ("2025-11-26", "2025-11-30"),
        ("2025-12-01", "2025-12-05"),
        ("2025-12-06", "2025-12-10"),
        ("2025-12-11", "2025-12-15"),
        ("2025-12-16", "2025-12-20"),
        ("2025-12-21", "2025-12-25"),
    ]

    for i in range(10):  # Crear 10 reservas
        huesped = huespedes[i % len(huespedes)]  # Selecciona un huésped en base al índice
        
        # Selecciona una habitación
        habitacion = habitaciones[i % len(habitaciones)]
        
        # Selecciona las fechas de entrada y salida de la lista hardcodeada
        fecha_entrada, fecha_salida = fechas_reservas[i]
        
        # Calcular precio
        dias_reserva = (datetime.strptime(fecha_salida, "%Y-%m-%d") - datetime.strptime(fecha_entrada, "%Y-%m-%d")).days
        precio = random.randint(100, 500) * dias_reserva

        # Crear una reserva en MongoDB
        reserva = {
            "id_huesped": huesped,
            "id_habitacion": habitacion,
            "fecha_entrada": fecha_entrada,
            "fecha_salida": fecha_salida,
            "precio": precio
        }
        
        # Manejo de excepciones al insertar en la base de datos
        try:
            reservas_collection.insert_one(reserva)
            reservas.append(reserva)
            print(f"Reserva creada: {reserva}")
        except Exception as e:
            print(f"Error al crear la reserva: {e}")


# Asegúrate de importar y configurar `reservas_collection` antes de ejecutar esta función.

# Asegúrate de llamar a la función crear_reservas() en el lugar adecuado de tu código.
