import datetime
from tabulate import tabulate 

salas = {
    1: {"nombre": "Sala Proactiva", "cupo": 8},
    2: {"nombre": "Sala de Descanso", "cupo": 4},
    3: {"nombre": "Sala de trabajo", "cupo": 12}
}

clientes = {
    101: {"nombres": "Daniela", "apellidos": "Castelar Valdez"},
    102: {"nombres": "Cristian", "apellidos": "Amaro Quiroz"}
}

reservaciones = {}

next_sala_id = 4
next_cliente_id = 103
next_folio = 2071353 

turnos = ("Matutino", "Vespertino", "Nocturno")

def registrar_cliente():
    global next_cliente_id
    print("\n--- Registrar cliente ---")
    nombres = input("Nombres: ").strip()
    apellidos = input("Apellidos: ").strip()
    if not nombres or not apellidos:
        print("Nombre y apellidos no pueden estar vacíos :( ")
        return
    clientes[next_cliente_id] = {"nombres": nombres, "apellidos": apellidos}
    print(f"Cliente '{nombres} {apellidos}' guardado con id {next_cliente_id}")
    next_cliente_id += 1

def registrar_sala():
    global next_sala_id
    print("\n--- Registrar sala ---")
    nombre = input("Nombre de sala: ").strip()
    if not nombre:
        print("El nombre de la sala no puede estar vacío :) ")
        return
    try:
        cupo = int(input("Cupo de la sala: "))
    except ValueError:
        print("El cupo debe ser un número entero")
        return
    salas[next_sala_id] = {"nombre": nombre, "cupo": cupo}
    print(f"Sala registrada con id {next_sala_id}")
    next_sala_id += 1

def registrar_reservacion():
    global next_folio
    print("\n--- Registrar reservación ---")
    print("\nClientes disponibles:")
    clientes_ordenados = sorted(clientes.items(), key=lambda item: (item[1]['apellidos'], item[1]['nombres']))
    for clave, c in clientes_ordenados:
        print(f"  {clave} - {c['apellidos']}, {c['nombres']}")
    id_cliente = None
    while True:
        clave_txt = input("\nElige la clave del cliente (o escribe '0' para cancelar): ")
        if clave_txt == '0':
            print("Operación cancelada")
            return
        try:
            id_seleccionado = int(clave_txt)
            if id_seleccionado in clientes:
                id_cliente = id_seleccionado
                break
            else:
                print("No existe un cliente con esa clave, inténtalo de nuevo.")
        except ValueError:
            print("La clave debe ser un número, inténtalo de nuevo.")
    fecha_minima = datetime.date.today() + datetime.timedelta(days=2)
    print(f"\nLa fecha de reserva debe ser a partir de {fecha_minima.strftime('%Y-%m-%d')}.")
    fecha_txt = input("Fecha (YYYY-MM-DD): ")
    try:
        fecha = datetime.datetime.strptime(fecha_txt, "%Y-%m-%d").date()
    except ValueError:
        print("Formato de fecha inválido.")
        return
    if fecha < fecha_minima:
        print("La fecha debe ser con al menos dos días de anticipación.")
        return
    print("\n--- Salas y turnos disponibles ---")
    salas_disponibles = False
    for id_sala, info in salas.items():
        turnos_libres = [turno for turno in turnos if not esta_ocupado(id_sala, fecha, turno)]
        if turnos_libres:
            print(f"  {id_sala} - {info['nombre']} (Cupo: {info['cupo']}) | Turnos libres: {', '.join(turnos_libres)}")
            salas_disponibles = True
    if not salas_disponibles:
        print("Lo sentimos, no hay salas con turnos disponibles para la fecha seleccionada")
        return
    try:
        id_sala_elegida = int(input("\nElige el ID de una sala: "))
    except ValueError:
        print("El ID de la sala debe ser un número")
        return
    if id_sala_elegida not in salas:
        print("Ese ID de sala no existe")
        return
    turno_elegido = input("Elige el turno (Matutino, Vespertino, Nocturno): ").capitalize()
    if turno_elegido not in turnos:
        print("Turno incorrecto, escribe una de las opciones")
        return
    if esta_ocupado(id_sala_elegida, fecha, turno_elegido):
        print(f"El turno '{turno_elegido}' para la sala {id_sala_elegida} ya no está disponible")
        return
    evento = ""
    while not evento:
        evento = input("Nombre del evento: ").strip()
    reservaciones[next_folio] = {
        "id_cliente": id_cliente,
        "id_sala": id_sala_elegida,
        "fecha": fecha,
        "turno": turno_elegido,
        "evento": evento
    }
    print(f"Reservación creada con éxito, el folio es: {next_folio}")
    next_folio += 1

def consultar_reservaciones():
    print("\n--- Consultar reservaciones ---")
    fecha_txt = input("Fecha (YYYY-MM-DD): ")
    try:
        fecha = datetime.datetime.strptime(fecha_txt, "%Y-%m-%d").date()
    except ValueError:
        print("Formato de fecha incorrecto")
        return
    tabla_datos = []
    headers = ["Sala (Cupo)", "Turno", "Estado", "Cliente", "Evento", "Folio"]
    for id_sala, info_sala in sorted(salas.items()):
        for turno in turnos:
            reserva_encontrada = None
            for folio, res in reservaciones.items():
                if res['id_sala'] == id_sala and res['fecha'] == fecha and res['turno'] == turno:
                    reserva_encontrada = res
                    folio_encontrado = folio
                    break
            nombre_sala = f"{info_sala['nombre']} ({info_sala['cupo']})"
            if reserva_encontrada:
                cliente_info = clientes[reserva_encontrada['id_cliente']]
                nombre_cliente = f"{cliente_info['nombres']} {cliente_info['apellidos']}"
                fila = [
                    nombre_sala,
                    turno,
                    "Ocupado",
                    nombre_cliente,
                    reserva_encontrada['evento'],
                    folio_encontrado
                ]
            else:
                fila = [nombre_sala, turno, "Disponible", "-", "-", "-"]
            tabla_datos.append(fila)
    print(f"\n--- Reservaciones en {fecha} ---")
    if not tabla_datos:
        print("No hay salas registradas para mostrar.")
    else:
        print(tabulate(tabla_datos, headers=headers, tablefmt="grid"))

def editar_reservacion():
    print("\n--- Editar reservación ---")
    try:
        folio = int(input("Folio de la reservación que quieran editar: "))
    except ValueError:
        print("Error, el folio debe ser un número")
        return
    if folio in reservaciones:
        print(f"Evento actual: '{reservaciones[folio]['evento']}'")
        nuevo_nombre = ""
        while not nuevo_nombre:
            nuevo_nombre = input("Nuevo nombre del evento: ").strip()
            if not nuevo_nombre:
                print("El nombre no puede dejarse vacío")
        reservaciones[folio]["evento"] = nuevo_nombre
        print("Evento actualizado con éxito")
    else:
        print("No existe ninguna reservación con ese folio")

def esta_ocupado(id_sala, fecha, turno):
    for r in reservaciones.values():
        if r["id_sala"] == id_sala and r["fecha"] == fecha and r["turno"] == turno:
            return True 
    return False  

def menu():
    while True:
        print("\n" "================" " MENU " "================")
        print("1. Registrar una Reservación")
        print("2. Editar nombre de una Reservación")
        print("3. Consultar Reservaciones por Fecha")
        print("4. Registrar un Cliente")
        print("5. Registrar una Sala")
        print("6. Salir")
        print("======================================") 
        opcion = input("Opción: ")
        if opcion == "1":
            registrar_reservacion()
        elif opcion == "2":
            editar_reservacion()
        elif opcion == "3":
            consultar_reservaciones()
        elif opcion == "4":
            registrar_cliente()
        elif opcion == "5":
            registrar_sala()
        elif opcion == "6":
            print("Hasta luego...")
            break
        else:
            print("Opción incorrecta, por favor elige un número del 1 al 6.")
        input("\n(Presiona Enter para continuar)")
if _name_ == "_main_":
    menu()
