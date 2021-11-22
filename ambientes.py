from time import sleep
from IPython.display import clear_output
import numpy as np
import copy

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import AnnotationBbox, OffsetImage, TextArea

class Conecta_4:

    def __init__(self):
        self.estado_inicial = np.zeros((7,6), dtype=np.int8)

    def pintar_estado(self,estado):
        fig, axes = plt.subplots()

        imagen_tablero = plt.imread("./imagenes/tableroV2.png")
        plt.imshow(imagen_tablero)

        figura_oscura = plt.imread("./imagenes/circuloOscuro.png")
        imagen_oscura = OffsetImage(figura_oscura, zoom=0.4)
        imagen_oscura.image.axes = axes

        figura_clara = plt.imread("./imagenes/circuloClaro.png")

        imagen_clara = OffsetImage(figura_clara, zoom=0.4)
        imagen_clara.image.axes = axes

        # inicio ---> 41,41
        # espacio en x = espacio en y ---> 99

        inicio_x = 41
        inicio_y = 41

        paso = 100

        for i in range(7):
            for j in range(6):
                
                pos_x = j
                pos_y = i

                if estado[i,j] == 1:
                    
                    ab = AnnotationBbox(
                                        imagen_oscura,
                                        [inicio_x + pos_x*paso, inicio_y + pos_y*paso],
                                        frameon=False)
                    axes.add_artist(ab)

                elif estado[i,j] == 2:
                    
                    ab = AnnotationBbox(
                                        imagen_clara,
                                        [inicio_x + pos_x*paso, inicio_y + pos_y*paso],
                                        frameon=False)
                    axes.add_artist(ab)


        axes.axis('off')
        plt.show()

        
    def a_jugar(self, estado):
        num_R = np.count_nonzero(estado==1)
        num_A = np.count_nonzero(estado==2)
        if num_R < num_A:
            return 1
        else:
            return 2
    
    def acciones(self, estado):
        ind = []

        fichas_abajo = []

        y = 6
        for x in reversed(range(6)):
            if estado[y, x] == 0:
                ind.append((x,y))
                    
            else:
                fichas_abajo.append((x,y))
                

        for i in fichas_abajo:
            if i[1] - 1 >= 0:
                if estado[i[1]-1, i[0]] == 0:
                    ind.append((i[0],i[1]-1))
                else:
                    fichas_abajo.append((i[0],i[1]-1))

        return ind
    
    def resultado(self,estado, indice):
        s = copy.deepcopy(estado)
        x = indice[0]
        y = indice[1]
        s[y,x] = self.a_jugar(estado)

        return s

    def es_terminal(self, estado):
        if np.count_nonzero(estado==0)==0:
            return True
        else:

            # Casos horizontales
            for i in range(7):
                for j in range(3):
                    if (estado[i,j] == 1 and estado[i,j+1] == 1 and estado[i,j+2] == 1 and estado[i,j+3] == 1) or (estado[i,j] == 2 and estado[i,j+1] == 2 and estado[i,j+2] == 2 and estado[i,j+3] == 2):
                        return True

            #casos verticales
            for j in range(6):
                for i in range(4):
                    if (estado[i,j] == 1 and estado[i+1,j] == 1 and estado[i+2,j] == 1 and estado[i+3,j] == 1) or (estado[i,j] == 2 and estado[i+1,j] == 2 and estado[i+2,j] == 2 and estado[i+3,j] == 2):
                        return True

            #casos diagonales
            
            for i in range(7):
                for j in range(6):

                    # diagonal abajo a la izquierda
                    if j > 2 and i < 4:
                        if (estado[i,j] == 1 and estado[i+1,j-1] == 1 and estado[i+2,j-2] == 1 and estado[i+3,j-3] == 1) or (estado[i,j] == 2 and estado[i+1,j-1] == 2 and estado[i+2,j-2] == 2 and estado[i+3,j-3] == 2):
                            return True

                    # diagonal arriba a la izquierda
                    if j > 2 and i > 2:
                        if (estado[i,j] == 1 and estado[i-1,j-1] == 1 and estado[i-2,j-2] == 1 and estado[i-3,j-3] == 1) or (estado[i,j] == 2 and estado[i-1,j-1] == 2 and estado[i-2,j-2] == 2 and estado[i-3,j-3] == 2):
                            return True       

                    # diagonal abajo a la derecha 
                    if j < 3 and i < 4:
                        if (estado[i,j] == 1 and estado[i+1,j+1] == 1 and estado[i+2,j+2] == 1 and estado[i+3,j+3] == 1) or (estado[i,j] == 2 and estado[i+1,j+1] == 2 and estado[i+2,j+2] == 2 and estado[i+3,j+3] == 2):
                            return True                                               
                        
                    # diagonal arriba a la derecha
                    if j < 3 and i > 2:
                        if (estado[i,j] == 1 and estado[i-1,j+1] == 1 and estado[i-2,j+2] == 1 and estado[i-3,j+3] == 1) or (estado[i,j] == 2 and estado[i-1,j+1] == 2 and estado[i-2,j+2] == 2 and estado[i-3,j+3] == 2):
                            return True   
                                
            return False

    def utilidad(self, estado, jugador):
        ob = self.es_terminal(estado)
        if ob:
            if np.count_nonzero(estado==0)==0:
                return 0
            else:
                if jugador == 1:
                    return 1
                if jugador == 2: 
                    return -1

        return None

#Algoritmo de busqueda minimax !
def minimax_search(juego,estado):
    jugador = juego.a_jugar(estado)
    valor, accion = max_value(juego,estado)
    return accion

def max_value(juego,estado):
    if juego.es_terminal(estado):
        jugador = juego.a_jugar(estado)
        return juego.utilidad(estado,jugador), None
    v = np.NINF
    for a in juego.acciones(estado):
        v2,a2 = min_value(juego,juego.resultado(estado,a))
        if v2 > v:
            v = v2
            accion = a
    return v,accion

def min_value(juego,estado):
    if juego.es_terminal(estado):
        jugador = juego.a_jugar(estado)
        return juego.utilidad(estado,jugador), None
    v = np.Inf
    for a in juego.acciones(estado):
        v2,a2 = max_value(juego,juego.resultado(estado,a))
        if v2 < v:
            v = v2
            accion = a
    return v,accion





def valor_maximo(juego, estado, alpha, beta):
    jugador = juego.a_jugar(estado)

    if juego.es_terminal(estado):
        return juego.utilidad(estado, jugador), None

    v = np.NINF

    for a in juego.acciones(estado):
        v2, a2 =  valor_minimo(juego, juego.resultado(estado,a), alpha, beta)

        if v2 > v:
            v = v2
            move = a
            alpha = max(alpha, v)

        if v >= beta:
            return v, move

    return v, move


def valor_minimo(juego, estado, alpha, beta):
    jugador = juego.a_jugar(estado)
    
    if juego.es_terminal(estado):
        return juego.utilidad(estado, jugador), None 

    v = np.Inf

    for a in juego.acciones(estado):
        v2, a2 = valor_maximo(juego, juego.resultado(estado,a), alpha, beta)

        if  v2 < v:
            v = v2
            move = a

            beta = min(beta, v)
        
        if v <= alpha: 
            return v, move

    return v, move 

def poda_alpha_beta(juego, estado):
    jugador = juego.a_jugar(estado)

    valor, mover = valor_maximo(juego, estado, np.NINF, np.Inf)
    return mover