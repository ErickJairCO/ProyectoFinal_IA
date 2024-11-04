import csv
from heapq import heappop, heappush
import math
from datetime import datetime

class AfluenciaEstaciones:
    def __init__(self):
        self.afluencia = {}

    def cargar_afluencia(self, archivo_afluencia):
        with open(archivo_afluencia) as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            next(lector_csv)  # Saltar el encabezado
            for renglon in lector_csv:
                estacion = renglon[1]
                tipo_afluencia = renglon[5]
                self.afluencia[estacion] = tipo_afluencia

    def obtener_afluencia(self, estacion):
        return self.afluencia.get(estacion, "Media")  # Predeterminado a "Media" si no se encuentra

class Grafo:
    def __init__(self):
        self.lista_adyacencia = {}
        self.lista_adyacencia_modificada = {}
        self.afluencia_estaciones = AfluenciaEstaciones()

    def cargar_grafo(self, archivo_grafo):
        with open(archivo_grafo) as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            for renglon in lector_csv:
                if len(renglon) > 0:
                    nodo = renglon[0]
                    self.añadir_vertice(nodo)

                    for i in range(1, len(renglon) - 1, 2):
                        sucesor = renglon[i]
                        peso = renglon[i + 1] if i + 1 < len(renglon) else None
                        
                        if sucesor.strip() and peso.strip():
                            try:
                                peso_entero = int(peso)
                                self.añadir_arista(nodo, sucesor, peso_entero)
                            except ValueError:
                                print(f"Error: el peso '{peso}' para la arista de {nodo} a {sucesor} no es un número válido.")

    def añadir_vertice(self, vertice):
        if vertice not in self.lista_adyacencia:
            self.lista_adyacencia[vertice] = {}

    def añadir_arista(self, nodo1, nodo2, peso):
        if nodo1 in self.lista_adyacencia:
            self.lista_adyacencia[nodo1][nodo2] = peso

    def ajustar_pesos_afluencia(self):
        # Crear una copia de la lista de adyacencia original para modificarla
        self.lista_adyacencia_modificada = {nodo: vecinos.copy() for nodo, vecinos in self.lista_adyacencia.items()}
        
        hora_actual = datetime.now().hour
        es_hora_pico = (5 <= hora_actual <= 9) or (18 <= hora_actual <= 22)

        for nodo, vecinos in self.lista_adyacencia_modificada.items():
            for vecino in vecinos:
                tipo_afluencia = self.afluencia_estaciones.obtener_afluencia(nodo)
                peso_original = self.lista_adyacencia[nodo][vecino]

                # Ajustar el peso en función de la afluencia y la hora
                if es_hora_pico:
                    if tipo_afluencia == "Mayor":
                        vecinos[vecino] = peso_original * 1.5  # Incremento en hora pico
                    elif tipo_afluencia == "Menor":
                        vecinos[vecino] = peso_original * 0.8  # Disminución en hora pico
                else:
                    if tipo_afluencia == "Mayor":
                        vecinos[vecino] = peso_original * 1.2  # Aumento menor fuera de hora pico
                    elif tipo_afluencia == "Menor":
                        vecinos[vecino] = peso_original  # Peso normal para afluencia menor
                    else:
                        vecinos[vecino] = peso_original * 1.1  # Incremento leve para afluencia media

    def ruta_mas_corta(self, source, destination):
        self.ajustar_pesos_afluencia()  # Ajustamos los pesos antes de la búsqueda

        distancia = {nodo: math.inf for nodo in self.lista_adyacencia_modificada}
        predecesor = {nodo: None for nodo in self.lista_adyacencia_modificada}
        distancia[source] = 0
        cola_prioridad = [(0, source)]
        
        while cola_prioridad:
            dist_actual, nodo_actual = heappop(cola_prioridad)

            if nodo_actual == destination:
                break

            for vecino, peso in self.lista_adyacencia_modificada[nodo_actual].items():
                nueva_distancia = dist_actual + peso
                if nueva_distancia < distancia[vecino]:
                    distancia[vecino] = nueva_distancia
                    predecesor[vecino] = nodo_actual
                    heappush(cola_prioridad, (nueva_distancia, vecino))

        camino = []
        nodo = destination
        while nodo is not None:
            camino.insert(0, nodo)
            nodo = predecesor[nodo]
        
        if distancia[destination] == math.inf:
            print("No hay ruta disponible entre los nodos especificados.")
            return None
        
        print(f"Ruta más corta desde {source} a {destination}: {camino}")
        print(f"Distancia total: {distancia[destination]}")
        return camino, distancia[destination]

# Inicialización de los datos
g = Grafo()
g.cargar_grafo('GrafoSistemaTransporte.csv')
g.afluencia_estaciones.cargar_afluencia('DATOSAFLUENCIA.csv')

# Ejemplo de búsqueda considerando afluencia
g.ruta_mas_corta('La Paz', 'Guelatao')
