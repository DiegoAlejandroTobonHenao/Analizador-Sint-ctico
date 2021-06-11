"""
Autores:    Diego Alejandro Parra Medina
            Diego Alejandro Tobon 
Proyecto: Analizador LL1

Clase que ejecuta la interfaz grafica principal
"""

#Importaciones
from FrameDatosIngreso import FrameDatosIngreso
from AnalizadorLL1 import AnalizadorLL1
from tkinter import StringVar
from tkinter import Tk
from tkinter import Label
from tkinter import Button
from tkinter import messagebox;

class FrameMain:
    
    def __init__(self):
        self.app = Tk()
        self.app.title('Analizador LL1')
        self.app.configure(bg="#424949")
        self.app.geometry("960x600")
        
        #Cada vez que agregue una producción se actualizara el Label que contiene estos datos
        Button(self.app, text='Agregar Producción', command=self.agregar, activebackground="#99CEFA",
               width=63, height=2, anchor="center").place(x=10, y=10)
        self.varProducciones = StringVar()
        self.labelProducciones = Label(self.app, textvariable=self.varProducciones, fg="yellow", bg="black",
                                       justify="left",font=("Verdana",20), width=26, height=15).place(x=10, y=60)
        
        #Cuando cancelo, borro toda la información que halla ingresado antes
        #Cuando confirmo estoy mandando los datos que halla registrado al analizador LL1
        Button(self.app, text='Cancelar', command=self.cancelar, activebackground="#99CEFA",
               width=20, height=2, anchor="center", bg="#FF5648").place(x=85, y=550)
        Button(self.app, text='Confirmar', command=self.confirmar, activebackground="#99CEFA",
               width=20, height=2, anchor="center", bg="#75FF70").place(x=235, y=550)
        
        #Cuando preciono uno de estos botones el mostrara la información respectiva
        self.botonPrimeros = Button(self.app, text='Primeros', command=self.primeros, activebackground="#99CEFA",
                                    state='disabled', width=20, height=2, anchor="center")
        self.botonPrimeros.place(x=500, y=10)
        self.botonSiguientes = Button(self.app, text='Siguientes', command=self.siguientes, activebackground="#99CEFA",
                                      state='disabled', width=20, height=2, anchor="center")
        self.botonSiguientes.place(x=650, y=10)
        self.botonConjuntoPrediccion = Button(self.app, text='Conjunto Predicciones', command=self.conjuntoPrediccion,
                                              activebackground="#99CEFA", state="disabled", width=20, height=2, anchor="center")
        self.botonConjuntoPrediccion.place(x=800, y=10)
        self.varInformacion = StringVar()
        self.labelInformacion = Label(self.app, textvariable=self.varInformacion, fg='yellow', bg='black',
                                       justify='left',font=('Verdana',20), width=26, height=15).place(x=500, y=60)
        
        #Se muestra la solución
        self.varLL1 = StringVar()
        self.labelSolucin = Label(self.app, textvariable=self.varLL1, justify="left", bg="#424949",
                                      font=("Verdana",12)).place(x=420, y=560)
        
        #Variables
        self.inicial = ""
        self.producciones = []
        self.noTerminales = []
        
        self.app.mainloop();
    
    def agregar(self):
        #Ejecuto una ventana que me pedira los datos
        ventana = FrameDatosIngreso(self.app);
        if ventana.res:
            #Reinicio la variable de información para que solo muestre datos confirmados
            self.varInformacion.set("")
            #Si no ingrese un no terminal el no hara nada
            if (ventana.noTerminal != ""):
                #Cuando agrego la primer producción el la identificara como la inicial
                if(len(self.producciones) == 0):
                        self.inicial = ventana.noTerminal
                #Verifica si la producción esta vacia de ser asi toma λ, la guarda en las producciones y actualiza la interfaz
                if(ventana.produccion == ""):
                    self.producciones.append((ventana.noTerminal,"λ"))
                    self.varProducciones.set(self.varProducciones.get() + ventana.noTerminal + " --> λ\n")
                else:
                    self.producciones.append((ventana.noTerminal,ventana.produccion))
                    self.varProducciones.set(self.varProducciones.get() + ventana.noTerminal + " --> " + ventana.produccion + "\n")
    
    def cancelar(self):
        #Reinicio los datos que se hallan leido antes
        self.inicial = ""
        self.producciones = []
        self.noTerminales = []
        #Reinicio las variables a vacias
        self.varProducciones.set("")
        self.varInformacion.set("")
        self.varLL1.set("")
        #Deshabilito los botones
        self.botonPrimeros.config(state='disabled')
        self.botonSiguientes.config(state='disabled')
        self.botonConjuntoPrediccion.config(state='disabled')
    
    def confirmar(self):
        try:
            #Reinicio la variable de información para que solo muestre datos confirmados
            self.varInformacion.set("")
            if(len(self.producciones) > 0):
                #Habilita los botones
                self.botonPrimeros.config(state='normal')
                self.botonSiguientes.config(state='normal')
                self.botonConjuntoPrediccion.config(state='normal')
                #Hallo los no terminales
                for produccion in self.producciones:
                    #Cada no terminal que encuentre y que no este en la lista lo agrega
                    if(produccion[0] not in self.noTerminales):
                        self.noTerminales.append(produccion[0])
                #Crea el analizador LL1 con los datos que hasta ese momento se hallan ingresado
                self.analizadorLL1 = AnalizadorLL1(self.noTerminales, self.inicial, self.producciones)
                #Cada vez que confirmemos el cambiara el mensaje de la solución
                self.varLL1.set(self.analizadorLL1.getMensaje())
            else:
                messagebox.showwarning('Advertencia','\nDebe ingresar producciones');
        except:
            messagebox.showwarning('Advertencia','\nLa gramática tiene recursión izquierda' +
                                   '\no se queda en infinita recursión \n\nElimenela antes de confirmar' +
                                   '\nSi ya eliminaste la recursión izquierda, es muy posible que la gramatica no sea valida para un analizador LL1');
    
    def primeros(self):
        #Limpiamos la variable que muestra la información
        self.varInformacion.set("")
        #Sacamos los primeros de cada no terminal y los mostramos
        for noTerminal in self.noTerminales:
            #Convertimos la lista de cada no terminal a una cadena para poder mostrarla por pantalla
            listaPrimeros = self.varInformacion.get() + noTerminal + " = {  "
            for p in self.analizadorLL1._primeros(noTerminal):
                listaPrimeros = listaPrimeros + p + " , "
            #Elimina la ultima ',' y da un salto de linea
            listaPrimeros = listaPrimeros[:-2] + " }\n"
            self.varInformacion.set(listaPrimeros)
    
    def siguientes(self):
        #Limpiamos la variable que muestra la información
        self.varInformacion.set("")
        #Sacamos los primeros de cada no terminal y los mostramos
        for noTerminal in self.noTerminales:
            #Convertimos la lista de cada no terminal a una cadena para poder mostrarla por pantalla
            listaSiguientes = self.varInformacion.get() + noTerminal + " = {  "
            for s in self.analizadorLL1._siguientes(noTerminal):
                listaSiguientes = listaSiguientes + s + " , "
            #Elimina la ultima ',' y da un salto de linea
            listaSiguientes = listaSiguientes[:-2] + " }\n"
            self.varInformacion.set(listaSiguientes)
    
    def conjuntoPrediccion(self):
        #Limpiamos la variable que muestra la información
        self.varInformacion.set("")
        #Sacamos el conjunto predicción de cada producción y lo mostramos
        for produccion in self.producciones:
            #Convertimos la lista de cada producción a una cadena para poder mostrarla por pantalla
            listaCP = self.varInformacion.get() + "CP (" + produccion[0] + " --> " + produccion[1] + ") = {  "
            for cp in self.analizadorLL1._conjuntoPrediccion(produccion):
                listaCP = listaCP + cp + " , "
            #Elimina la ultima ',' y da un salto de linea
            listaCP = listaCP[:-2] + " }\n"
            self.varInformacion.set(listaCP)
    