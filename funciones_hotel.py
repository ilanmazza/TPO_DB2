from py2neo import Graph, Node
from funciones_gestion import *
from geopy.geocoders import Nominatim
#cambio lucca
# Conexion BD Neo4J y geocoders
graph = Graph("bolt://neo4j:12345678@localhost:7687")
geolocator = Nominatim(user_agent="geoapi")


def obtener_coordenadas(direccion):
    # Agrega "Capital Federal, Argentina" a la dirección
    direccion_completa = f"{direccion}, Capital Federal, Argentina"
    try:
        location = geolocator.geocode(direccion_completa)
        if location:
            return (location.latitude, location.longitude)
        else:
            print("No se encontraron coordenadas para la dirección proporcionada.")
            return None
    except Exception as e:
        print(f"Error al obtener coordenadas: {e}")
        return None

def mostrar_hoteles():
    try:
        # Consulta para obtener ID y nombre de todos los hoteles
        query = "MATCH (h:Hotel) RETURN h.id_hotel AS id, h.nombre AS nombre"
        results = graph.run(query).data()

        # Lista para almacenar diccionarios con id y nombre de cada hotel
        lista_hoteles = []

        # Verifica si hay resultados y muestra cada hotel
        if results:
            print("Lista de Hoteles:")
            for hotel in results:
                print(f"ID: {hotel['id']}, Nombre: {hotel['nombre']}")
                # Agrega el id y nombre como diccionario a la lista
                lista_hoteles.append({"id": hotel['id'], "nombre": hotel['nombre']})
        else:
            print("No se encontraron hoteles en la base de datos.")

        # Retorna la lista de diccionarios
        return lista_hoteles
    except Exception as e:
        print(f"Error al mostrar los hoteles: {e}")
        return []


def alta_hotel(nombre, direccion, telefono, email):
    try:
        # Encuentra el ID más alto de los hoteles actuales
        query = "MATCH (h:Hotel) RETURN coalesce(max(toInteger(h.id_hotel)), 0) AS max_id"
        result = graph.run(query).data()
        
        # Obtener el ID más alto
        max_id = result[0]["max_id"] if result else 0
        nuevo_id = max_id + 1

        id_hotel= nuevo_id

        # Crear el nuevo hotel
        latitude, longitude = obtener_coordenadas(direccion)
        if latitude is None or longitude is None:
            return f"No se pudieron obtener las coordenadas para la dirección: {direccion}"
        query = """
            CREATE (:Hotel {id_hotel: $id_hotel, nombre: $nombre, direccion: $direccion, 
            telefono: $telefono, email: $email, latitude: $latitude, longitude: $longitude})
        """
        graph.run(query, id_hotel=str(id_hotel), nombre=nombre, direccion=direccion, 
                  telefono=telefono, email=email, latitude=latitude, longitude=longitude)
        
        subquery="""
        MATCH (h:Hotel{id_hotel: $id_hotel}), (p:POI)
        WHERE point.distance(point({latitude: h.latitude, longitude: h.longitude}), point({latitude: p.latitude, longitude: p.longitude})) < 1000
        CREATE (h) - [:CERCA_DE {distancia: point.distance(point({latitude: h.latitude, longitude: h.longitude}),
        point({latitude: p.latitude, longitude: p.longitude})) }] -> (p)"""

        graph.run(subquery, id_hotel=str(id_hotel))

        return f"Hotel '{nombre}' creado exitosamente."
    except Exception as e:
        return f"Error al crear el hotel: {e}"
    
    
def baja_hotel(id_hotel):
    try:
        # Eliminar el hotel y todas sus relaciones
        query = """
            MATCH (h:Hotel {id_hotel: $id_hotel}) 
            DETACH DELETE h
        """
        graph.run(query, id_hotel=id_hotel)
        return f"Hotel con ID {id_hotel} eliminado exitosamente."
    except Exception as e:
        return f"Error al eliminar el hotel: {e}"
    
    
    
def modificar_hotel(id_hotel, nombre=None, direccion=None, telefono=None, email=None):
    
    try:
        # Actualizar solo los campos que no son None
        update_fields = []
        
        if nombre:
            update_fields.append(f"h.nombre = '{nombre}'")
        if direccion:
            update_fields.append(f"h.direccion = '{direccion}'")
            latitud, longitud = obtener_coordenadas(direccion)
            update_fields.append(f"h.latitude = {latitud}")
            update_fields.append(f"h.longitude = {longitud}")

        if telefono:
            update_fields.append(f"h.telefono = '{telefono}'")
        if email:
            update_fields.append(f"h.email = '{email}'")
        if not update_fields:
            return "No se proporcionó ningún campo para modificar."
        query = f"""
            MATCH (h:Hotel {{id_hotel: $id_hotel}})
            SET {', '.join(update_fields)}
        """
        result = graph.run(query, id_hotel=id_hotel)

        if direccion:
            delete_query = """
                MATCH (h:Hotel {id_hotel: $id_hotel})-[r:CERCA_DE]->(p:POI)
                DELETE r
            """
            graph.run(delete_query, id_hotel=id_hotel)

            create_query = """
                MATCH (h:Hotel {id_hotel: $id_hotel}), (p:POI)
                WHERE point.distance(point({latitude: h.latitude, longitude: h.longitude}), point({latitude: p.latitude, longitude: p.longitude})) < 1000
                CREATE (h)-[:CERCA_DE {distancia: point.distance(point({latitude: h.latitude, longitude: h.longitude}), point({latitude: p.latitude, longitude: p.longitude}))}]->(p)
            """
            graph.run(create_query, id_hotel=str(id_hotel))

        return f"Hotel con ID {id_hotel} modificado exitosamente."
    except Exception as e:
        return f"Error al modificar el hotel: {e}"
    

def listar_hoteles_2():
    try:
        query = "MATCH (h:Hotel) RETURN h.id_hotel, h.nombre ORDER BY h.nombre"
        result = graph.run(query)
        hoteles = result.data()  # Devuelve una lista de diccionarios con los hoteles
        
        if not hoteles:
            print("No hay hoteles disponibles para modificar.")
            return None
        
        print("Seleccione el hotel a modificar:")
        for idx, hotel in enumerate(hoteles, start=1):
            print(f"{idx}. {hotel['h.nombre']} ")
        
        seleccion = int(input("Ingrese el número del hotel que desea modificar: "))
        if 1 <= seleccion <= len(hoteles):
            return hoteles[seleccion - 1]['h.id_hotel']  # Retorna el id del hotel seleccionado
        else:
            print("Selección inválida.")
            return None
    except Exception as e:
        print(f"Error al listar los hoteles: {e}")
        return None
