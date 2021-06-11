"""
Autores:    Diego Alejandro Parra Medina
            Diego Alejandro Tobon 
Proyecto: Analizador LL1

Clase que representa un analizador LL1
"""

class AnalizadorLL1:
    
    def __init__(self, noTerminales, inicial, producciones):
        self._noTerminales = noTerminales
        self._inicial = inicial
        self._producciones = producciones
    
    def _primeros(self, noTerminal):
        #Inicializamos una lista de primeros vacia que se retorna al final
        listaPrimeros =  []
        #Buscamos las producciones de este no terminal
        for produccion in self._producciones:
            if(produccion[0] == noTerminal):
                #Dividimos la producción en una lista
                listaProduccion = produccion[1].split()
                #Añadimos cada primero sin que se repita
                #Primer caso: es lambda
                if(listaProduccion[0] == "λ"):
                    if(listaProduccion[0] not in listaPrimeros):
                        listaPrimeros.append(listaProduccion[0])
                #Segundo caso: es un terminal
                elif(listaProduccion[0] not in self._noTerminales):
                    if(listaProduccion[0] not in listaPrimeros):
                        listaPrimeros.append(listaProduccion[0])
                #Tercer caso: es un no terminal, recursivamente seran los primeros de este
                else:
                    for primero in self._primeros(listaProduccion[0]):
                        if(primero not in listaPrimeros):
                            listaPrimeros.append(primero)
        return listaPrimeros
    
    def _siguientes(self, noTerminal):
        #Inicializamos una lista de siguientes vacia que se retorna al final
        listaSiguientes =  []
        for produccion in self._producciones:
            #Dividimos la producción en una lista
            listaProduccion = produccion[1].split()
            #Verifica si esta el no terminal en la producción
            #Añadimos cada siguiente a la lista de siguiente sin que se repita
            #Primer caso: es el no terminal inicial --> se añade $ a la lista
            if(noTerminal == self._inicial and "$" not in listaSiguientes):
                    listaSiguientes.append("$")
            if(noTerminal in listaProduccion):
                #Hallamos la posición del no terminal
                i = listaProduccion.index(noTerminal)
                #Verifica que la posición no sea la ultima en caso de ser asi, sigue λ
                if(i < len(listaProduccion)-1):
                    #Segundo caso: el siguiente es un no terminal--> se añaden los primeros
                    #de este, se debe tener en cuenta si es λ
                    if(listaProduccion[i+1] in self._noTerminales):
                        for primero in self._primeros(listaProduccion[i+1]):
                            #Si es λ se añaden los sig(A) a los Sig(X)
                            if(primero == "λ"):
                                for siguiente in self._siguientes(listaProduccion[i+1]):
                                    if(siguiente not in listaSiguientes):
                                        listaSiguientes.append(siguiente)
                            #Si no, se añaden a la lista los primeros que por ende son terminales
                            else:
                                if(primero not in listaSiguientes):
                                    listaSiguientes.append(primero)
                    #Tercer caso: el siguiente es un terminal --> se añade el terminal
                    else:
                        if(listaProduccion[i+1] not in listaSiguientes):
                            listaSiguientes.append(listaProduccion[i+1])
                else:
                    #Cuarto caso: el siguiente es λ --> se añaden los sig(A)
                    #solo en caso de que A != X (para evitar recursión infinita)
                    if(produccion[0] != noTerminal):
                        for siguiente in self._siguientes(produccion[0]):
                            if(siguiente not in listaSiguientes):
                                listaSiguientes.append(siguiente)
        return listaSiguientes
    
    def _conjuntoPrediccion(self, produccion):
        #Inicializamos un conjunto predicción vacia que se retorna al final
        conjuntoPrediccion = []
        #Dividimos la producción en una lista
        listaProduccion = produccion[1].split()
        #Añadimos el primer de cada produccion a la lista segun sea el caso
        #Primer caso: es λ --> se añaden los sig(A)
        if(listaProduccion[0] == "λ"):
            conjuntoPrediccion.extend(self._siguientes(produccion[0]))
        #Segundo caso: es un no terminal --> se añaden los prim(X)
        elif(listaProduccion[0] in self._noTerminales):
            conjuntoPrediccion.extend(self._primeros(listaProduccion[0]))
        #Tercer caso: es un terminal --> se añade el terminal
        else:
            conjuntoPrediccion.append(listaProduccion[0])
        return conjuntoPrediccion
    
    def getMensaje(self):
        esLL1 = True
        #Analizamos si existe interseccion en los conjuntos de prediccion de cada no terminal
        #para determinar si la gramatica es  compatible para un analizador LL1
        for noTerminal in self._noTerminales:
            lista = []
            for produccion in self._producciones:
                if(produccion[0] == noTerminal):
                    for cp in self._conjuntoPrediccion(produccion):
                        #Si esta prediccion ya esta en la lista es por que hay intersección
                        #si no es asi, la agrega a la lista
                        if(cp in lista):
                            esLL1 = False
                        lista.append(cp)
        if(esLL1):
            return "Esta gramática es compatible para un analizador LL1"
        else:
            return "Esta gramática NO es compatible para un analizador LL1"
    