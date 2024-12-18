from py2neo import Graph
from pymongo import MongoClient
from funciones_gestion import *
from crear_entidades import *
from funciones_gestion import *
from funciones_amenity import *
from funciones_habitacion import *
from funciones_huesped import *
from funciones_reserva import *
from funciones_hotel import *

graph = Graph("bolt://neo4j:12345678@localhost:7687")
client = MongoClient('mongodb://localhost:27017/')
db = client['hotel_db']
reservas_collection = db['reservas']


def gestionar_entidad():
    while True:
        print("Seleccione la operación que desea realizar:")
        print("1. Crear")
        print("2. Modificar")
        print("3. Eliminar")
        print("5. Consultas")
        print("6. Crear Datos Iniciales")
        print("7. Salir")
        opcion = input("Ingrese el número de la operación (1-7): ")

        # Para todas las opciones menos consultas, se selecciona la entidad
        if opcion in ['1', '3']:
            print("---------------------------TURISBA---------------------------")
            print("Seleccione la entidad:")
            print("1. Hotel")
            print("2. Habitación")
            print("3. Amenity")
            print("4. POI")
            print("5. Huésped")
            print("6. Reserva")
            entidad = input("Ingrese el número de la entidad (1-6): ")

        if opcion in ['2']:
            print("---------------------------TURISBA---------------------------")
            print("Seleccione la entidad:")
            print("1. Hotel")
            print("2. Habitación")
            print("3. Amenity")
            print("4. POI")
            print("5. Huésped")
            entidad = input("Ingrese el número de la entidad (1-5): ")

        if opcion == '1':  # Crear
            
            if entidad == '1':  # Hotel
                print("---------------------------CREAR HOTEL---------------------------")
                nombre = input("Ingrese el nombre del hotel: ")
                direccion = input("Ingrese la dirección del hotel: ")
                telefono = input("Ingrese el teléfono del hotel: ")
                email = input("Ingrese el email del hotel: ")
                alta_hotel(nombre, direccion, telefono, email)
            
            elif entidad == '2':  # Habitación
               print("---------------------------CREAR HABITACION---------------------------")
               alta_habitacion()
            
            elif entidad == '3':  # Amenity
                print("---------------------------CREAR AMENITY---------------------------")
                nombre = input("Ingrese el nombre del amenity: ")
                alta_amenity(nombre)
            
            elif entidad == '4':  # POI
                print("-----------------------CREAR PUNTO DE INTERES-----------------------")
                nombre = input("Ingrese el nombre del POI: ")
                detalle = input("Ingrese el detalle del POI: ")
                direccion = input("Ingrese la direccion del POI: ")
                tipo = input("Ingrese el tipo del POI: ")
                alta_poi(nombre, detalle, direccion, tipo)
                mensaje = alta_poi(nombre, detalle, direccion, tipo)
                print(mensaje)
                
            elif entidad == '5':  # Huésped
                print("---------------------------CREAR HUESPED---------------------------")
                nombre = input("Ingrese el nombre del huésped: ")
                apellido = input("Ingrese el apellido del huésped: ")
                direccion = input("Ingrese la dirección del huésped: ")
                telefono = input("Ingrese el teléfono del huésped: ")
                email = input("Ingrese el email del huésped: ")
                alta_huesped(nombre, apellido, direccion, telefono, email)
            
            elif entidad == '6':  # Reserva
                print("---------------------------CREAR RESERVA---------------------------")
                crear_reserva()
        
        elif opcion == '2':  # Modificar

            if entidad == '1':  # Hotel  
                print("---------------------------MODIFICAR HOTEL---------------------------")            
                modificar_hotel()
            
            elif entidad == '2':  # Habitación
                print("------------------------MODIFICAR HABITACION------------------------")
                modificar_habitacion()
            
            elif entidad == '3':  # Amenity
                print("---------------------------MODIFICAR AMENITY---------------------------") 
                modificar_amenity()
            
            elif entidad == '4':  # POI
                print("----------------------MODIFICAR PUNTO DE INTERES---------- ----------")
                modificar_poi()
                
            elif entidad == '5':  # Huésped
                print("------------------------MODIFICAR HUESPED------------------------")
                modificar_huesped()

        elif opcion == '3':  # Eliminar
            if entidad == '1' :
                print("------------------------ELIMINAR HOTEL------------------------")
                baja_hotel()
                
            elif entidad == '2':  # Habitación
                print("------------------------ELIMINAR HABITACION------------------------")
                baja_habitacion()
            
            elif entidad == '3':  # Amenity
                print("------------------------ELIMINAR AMENITY------------------------")
                baja_amenity()
            
            elif entidad == '4':  # POI
                print("---------------------ELIMINAR PUNTO DE INTERES---------------------")
                baja_poi()
            elif entidad == '5':  # Huesped
                baja_huesped()
            elif entidad == '6': #Reserva
                print("------------------------ELIMINAR RESERVA------------------------")
                resultado = baja_reserva()
                print(resultado)

            
        elif opcion == '5':  # Consultas
            print("---------------------------TURISBA---------------------------")
            print("Seleccione la consulta que desea realizar:")
            print("1. Hoteles cerca de un POI")
            print("2. Información de un hotel")
            print("3. POIs cerca de un hotel")
            print("4. Habitaciones disponibles")
            print("5. Amenities de una habitación")
            print("6. Reservas por número de confirmación")
            print("7. Reservas de un huésped")
            print("8. Reservas por fecha en el hotel")
            print("9. Ver detalles del huésped")
            consulta = input("Ingrese el número de la consulta (1-9): ")

            # Lógica para cada consulta
            if consulta == '1':
                print("------------------------HOTELES CERCA DE PUNTO DE INTERES------------------------")
                hoteles_cerca_de_poi()
            elif consulta == '2':
                print("------------------------INFORMACION DE HOTEL------------------------")
                informacion_hotel()
            elif consulta == '3':
                print("------------------------PUNTO DE INTERES CERCA DE HOTELES------------------------")
                pois_cerca_de_hotel()
            elif consulta == '4':  # Habitaciones disponibles
                    print("-------------------HABITACIONES DIPONIBLES PARA RANGO DE FECHA-------------------")
                    id_hotel = listar_hoteles_con_validacion()
                    if id_hotel:
                        fecha_entrada = input("Ingrese la fecha de entrada (YYYY-MM-DD): ")
                        fecha_salida = input("Ingrese la fecha de salida (YYYY-MM-DD): ")
                        # Llama a la función y filtra las habitaciones por hotel
                        habitaciones_disponibles_en_hotel(id_hotel,fecha_entrada, fecha_salida)
                    
            elif consulta == '5':
                print("------------------------AMENITYS DE UNA HABITACION------------------------")
                mostrar_amenities_habitacion()
            elif consulta == '6':
                print("------------------------RESRVA POR NUMERO DE RESERVA------------------------")
                reservas_por_numero_confirmacion()
            elif consulta == '7':
                print("------------------------PRESRVA POR HUESPED------------------------")
                reservas_por_huesped()
            elif consulta == '8':
                print("------------------------PRESRVA PARA HOTEL PARA RANGO DE FECHA------------------------")
                fecha = input("Ingrese la fecha (YYYY-MM-DD): ")
                fecha2 = input("Ingrese la fecha (YYYY-MM-DD): ")
                reservas_por_fecha_en_hotel(fecha,fecha2)
            elif consulta == '9':
                print("------------------------DETALLE DE HUESPED------------------------")
                ver_detalles_huesped()
        
        elif opcion == '6':
            print("------------------------CREACION INICIAL DE DATOS------------------------")
            borrar_bd_reservas1()
            borrar_bd_nodos()
            crear_huespedes()
            crear_hoteles()
            crear_pois()
            crear_amenitys()
            crear_habitaciones()
            crear_reservas()
        elif opcion == '7':  # Salir
            print("Salir del sistema") 
            break

        else:
            print("Opción no válida.")

print("---------------------------TURISBA---------------------------")
      
gestionar_entidad()