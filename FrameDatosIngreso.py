"""
Autores:    Diego Alejandro Parra Medina
            Diego Alejandro Tobon 
Proyecto: Analizador LL1

Clase que ejecuta la interfaz grafica que lee los datos de ingreso
"""

#Importaciones
from tkinter import Toplevel;
from tkinter import Entry
from tkinter import Label
from tkinter import Button
from tkinter import messagebox;

class FrameDatosIngreso:

    def __init__(self, app):
        self.res = False;
        self.t1 = Toplevel(app);
        self.t1.geometry('220x120');
        self.t1.title('Datos de Ingreso');
        self.t1.focus_set();
        self.t1.grab_set();
        self.t1.transient(master=app);
        
        Label(self.t1, text='Ingrese los datos de la producción:').place(x=12, y=10);
        
        self.noTerminal = Entry(self.t1, width=3)
        self.noTerminal.place(x=35, y=40)
        Label(self.t1, text='-->').place(x=65, y=40);
        self.produccion = Entry(self.t1, width=13)
        self.produccion.place(x=100, y=40)

        Button(self.t1, text='AGREGAR', command=self.verificacion).place(x=75, y=80)
        
        self.t1.wait_window(self.t1)
        
    def verificacion(self):
        try:
            noTerminal = self.noTerminal.get();
            self.noTerminal = noTerminal;
            produccion = self.produccion.get();
            self.produccion = produccion;
            self.res = True;
            self.t1.destroy();
        except:
            messagebox.showwarning('Advertencia','\nLos datos son incorrectos \nIngreselos de nuevo');
    