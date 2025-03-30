import heapq

class Estacion:
    def __init__(self, nombre):
        self.nombre = nombre
        self.conexiones = []

    def agregar_conexion(self, estacion_destino, tiempo_recorrido, tiempo_estimado, costo):
        self.conexiones.append((estacion_destino, tiempo_recorrido, tiempo_estimado, costo))

class SistemaTransporte:
    def __init__(self):
        self.estaciones = {}
        self.reglas = []

    def agregar_estacion(self, nombre):
        estacion = Estacion(nombre)
        self.estaciones[nombre] = estacion
        return estacion

    def agregar_regla(self, regla):
        self.reglas.append(regla)

    def evaluar_reglas(self, estacion_actual, vecino):
        for regla in self.reglas:
            if not regla(estacion_actual, vecino):
                return False
        return True

    def obtener_mejor_ruta(self, inicio, destino):

        cola = []
        heapq.heappush(cola, (
        0, inicio, [], 0, 0))
        visitados = set()

        while cola:
            costo_actual, estacion_actual, ruta_actual, tiempo_total, costo_total = heapq.heappop(cola)

            if estacion_actual == destino:
                return ruta_actual, costo_total, tiempo_total

            if estacion_actual in visitados:
                continue
            visitados.add(estacion_actual)

            for vecino, tiempo_recorrido, tiempo_estimado, costo in self.estaciones[estacion_actual].conexiones:
                if self.evaluar_reglas(estacion_actual, vecino):
                    nuevo_costo_total = costo_total + costo
                    nuevo_tiempo_total = tiempo_total + tiempo_recorrido
                    nueva_ruta = ruta_actual + [
                        (estacion_actual, vecino.nombre, tiempo_recorrido, tiempo_estimado, costo)]
                    heapq.heappush(cola, (
                    nuevo_costo_total, vecino.nombre, nueva_ruta, nuevo_tiempo_total, nuevo_costo_total))

        return None, float('inf'), 0

    def obtener_ruta_alterna(self, inicio, destino, mejor_ruta):
        visitados = set()
        cola = []
        heapq.heappush(cola, (
        0, inicio, [], 0, 0))

        while cola:
            costo_actual, estacion_actual, ruta_actual, tiempo_total, costo_total = heapq.heappop(cola)

            if estacion_actual == destino:
                return ruta_actual, costo_total, tiempo_total

            if estacion_actual in visitados:
                continue
            visitados.add(estacion_actual)

            if ruta_actual and any(estacion_actual == tramo[1] for tramo in mejor_ruta):
                continue

            for vecino, tiempo_recorrido, tiempo_estimado, costo in self.estaciones[estacion_actual].conexiones:
                if self.evaluar_reglas(estacion_actual, vecino):
                    nuevo_costo_total = costo_total + costo
                    nuevo_tiempo_total = tiempo_total + tiempo_recorrido
                    nueva_ruta = ruta_actual + [
                        (estacion_actual, vecino.nombre, tiempo_recorrido, tiempo_estimado, costo)]
                    heapq.heappush(cola, (
                    nuevo_costo_total, vecino.nombre, nueva_ruta, nuevo_tiempo_total, nuevo_costo_total))

        return None, float('inf'), 0

sistema = SistemaTransporte()

# Creamos el Arreglo de estaciones en el sistema
est1 = sistema.agregar_estacion("EstacionA")
est2 = sistema.agregar_estacion("EstacionB")
est3 = sistema.agregar_estacion("EstacionC")
est4 = sistema.agregar_estacion("EstacionD")
est5 = sistema.agregar_estacion("EstacionE")
est6 = sistema.agregar_estacion("EstacionF")
est7 = sistema.agregar_estacion("EstacionG")
est8 = sistema.agregar_estacion("EstacionH")
est9 = sistema.agregar_estacion("EstacionI")
est10 = sistema.agregar_estacion("EstacionJ")

# Establecemos las conexiones entre las estaciones con (tiempo_recorrido, tiempo_estimado, costo)
est1.agregar_conexion(est2, 10, 12, 5)
est2.agregar_conexion(est3, 15, 18, 8)
est3.agregar_conexion(est4, 20, 25, 12)
est4.agregar_conexion(est5, 10, 15, 6)
est5.agregar_conexion(est6, 5, 8, 3)
est6.agregar_conexion(est7, 15, 20, 10)
est7.agregar_conexion(est8, 10, 12, 7)
est8.agregar_conexion(est9, 20, 24, 15)
est9.agregar_conexion(est10, 25, 30, 18)
est1.agregar_conexion(est6, 30, 35, 22)
est2.agregar_conexion(est7, 18, 22, 14)
est5.agregar_conexion(est9, 22, 25, 17)
est6.agregar_conexion(est10, 12, 14, 9)
est7.agregar_conexion(est10, 15, 17, 11)

def evitar_congestion(estacion_actual, vecino):
    if vecino.nombre == "EstacionE":
        return False
    return True

sistema.agregar_regla(evitar_congestion)

def solicitar_origen_destino():
    origen = input("Ingrese el nombre de la estación de origen: ")
    destino = input("Ingrese el nombre de la estación de destino: ")
    return origen, destino

def preguntar_ruta_alterna():
    respuesta = input("¿Deseas obtener una ruta alterna? (s para nueva ruta, 'finalizar' para salir): ")
    return respuesta.lower()

origen, destino = solicitar_origen_destino()

ruta, costo, tiempo_total = sistema.obtener_mejor_ruta(origen, destino)

if ruta:
    print(f"Ruta desde {origen} a {destino}:")
    total_costo = 0
    for i, (origen, destino, tiempo_recorrido, tiempo_estimado, costo) in enumerate(ruta):
        costo_en_pesos = costo * 1000
        print(
            f"  - Desde {origen} a {destino}, Tiempo de recorrido: {tiempo_recorrido} minutos, Tiempo estimado: {tiempo_estimado} minutos, Costo: ${costo_en_pesos}")
        total_costo += costo_en_pesos
    print(f"\nCosto total del recorrido: ${total_costo}")
    print(f"Tiempo total del recorrido: {tiempo_total} minutos")

    while True:
        opcion = preguntar_ruta_alterna()

        if opcion == 'finalizar':
            print("Proceso finalizado.")
            break
        elif opcion == 's':
            ruta_alterna, costo_alterna, tiempo_alterna = sistema.obtener_ruta_alterna(origen, destino, ruta)
            if ruta_alterna:
                print("\nRuta Alternativa:")
                total_costo_alterna = 0
                for i, (origen, destino, tiempo_recorrido, tiempo_estimado, costo) in enumerate(ruta_alterna):
                    costo_en_pesos = costo * 1000
                    print(
                        f"  - Desde {origen} a {destino}, Tiempo de recorrido: {tiempo_recorrido} minutos, Tiempo estimado: {tiempo_estimado} minutos, Costo: ${costo_en_pesos}")
                    total_costo_alterna += costo_en_pesos
                print(f"\nCosto total de la ruta alternativa: ${total_costo_alterna}")
                print(f"Tiempo total de la ruta alternativa: {tiempo_alterna} minutos")
            else:
                print("No se encontró una ruta alternativa viable.")
        else:
            print("Opción no válida. Escribe 's' para obtener una ruta alterna o 'finalizar' para salir.")
else:
    print(f"No se encontró una ruta viable desde {origen} a {destino}.")
