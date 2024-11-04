import csv
from heapq import heappop, heappush
import math

class Grafo:

    def __init__(self):
        self.lista_adyacencia = {}

    def cargar_grafo(self):
        with open('GrafoSistemaTransporte.csv') as archivo_csv:
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
                                peso_entero = int(peso)  # Convertimos el peso a un número entero
                                self.añadir_arista(nodo, sucesor, peso_entero)
                            except ValueError:
                                print(f"Error: el peso '{peso}' para la arista de {nodo} a {sucesor} no es un número válido.")
    
    def añadir_vertice(self, vertice):
        if vertice not in self.lista_adyacencia:
            self.lista_adyacencia[vertice] = {}

    def añadir_arista(self, nodo1, nodo2, peso):
        if nodo1 in self.lista_adyacencia:
            self.lista_adyacencia[nodo1][nodo2] = peso

    def mostrar_lista_adyacencia(self):
        #print("Procesando impresion de valores")
        for nodo, vecinos in self.lista_adyacencia.items():
            print(f"{nodo} -> {vecinos}")

    def ruta_mas_corta(self, source, destination):
        #Inicializamos las distancias y la cola de prioridad
        distancia = {nodo: math.inf for nodo in self.lista_adyacencia}
        predecesor = {nodo: None for nodo in self.lista_adyacencia}
        distancia[source] = 0
        cola_prioridad = [(0, source)]  # (distancia, nodo)
        
        while cola_prioridad:
            dist_actual, nodo_actual = heappop(cola_prioridad)

            # Se detiene la busqueda si se encuentra el vertice destino
            if nodo_actual == destination:
                break

            # Paso 2: Relajar las aristas
            for vecino, peso in self.lista_adyacencia[nodo_actual].items():
                nueva_distancia = dist_actual + peso
                if nueva_distancia < distancia[vecino]:
                    distancia[vecino] = nueva_distancia
                    predecesor[vecino] = nodo_actual
                    heappush(cola_prioridad, (nueva_distancia, vecino))

        # Reconstruir o formando el camino más corto
        camino = []
        nodo = destination
        while nodo is not None:
            camino.insert(0, nodo)
            nodo = predecesor[nodo]
        
        # Veridfica si se encontro un camino, de lo contrario imprime que no hay ruta disponible
        if distancia[destination] == math.inf:
            print("No hay ruta disponible entre los nodos especificados.")
            return None
        
        print(f"Ruta más corta desde {source} a {destination}: {camino}")
        print(f"Distancia total: {distancia[destination]}")
        return camino, distancia[destination]


g = Grafo()
g.cargar_grafo()
#g.mostrar_lista_adyacencia()

g.ruta_mas_corta('La Paz','Guelatao')