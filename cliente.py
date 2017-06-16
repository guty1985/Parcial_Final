#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Pyro4
from Tkinter import *
from functools import partial
import ttk
import tkFont
import getpass
import json
import ast



class Aplicacion():
        def __init__(self):
            self.servidor="Marcela.com"
            self.raiz = Tk()

            self.raiz.geometry('430x200+500+50')  # Define la dimensión de la ventana

            # Establece que no se pueda cambiar el tamaño de la
            # ventana
            self.raiz.resizable(0, 0)
            self.raiz.title("Acceso")
            self.fuente = tkFont.Font(weight='bold')# Tipo de letra
            self.etiq1 = ttk.Label(self.raiz, text="Email:",
                                   font=self.fuente)
            self.etiq2 = ttk.Label(self.raiz, text="Contraseña:",
                                   font=self.fuente)

            # Declara una variable de cadena que se asigna a
            # la opción 'textvariable' de un widget 'Label' para
            # mostrar mensajes en la ventana. Se asigna el color
            # azul a la opción 'foreground' para el mensaje.

            self.mensa = StringVar()
            self.etiq3 = ttk.Label(self.raiz, textvariable=self.mensa,
                                   font=self.fuente, foreground='blue')

            self.usuario = StringVar()
            self.clave = StringVar()
            self.ctext1 = ttk.Entry(self.raiz,
                                    textvariable=self.usuario, width=30)
            self.ctext2 = ttk.Entry(self.raiz,
                                    textvariable=self.clave,
                                    width=30,
                                    show="*")
            self.separ1 = ttk.Separator(self.raiz, orient=HORIZONTAL)
            self.boton1 = ttk.Button(self.raiz, text="Aceptar",
                                     padding=(5, 5), command=self.aceptar)
            self.boton2 = ttk.Button(self.raiz, text="Limpiar",
                                     padding=(5, 5), command=self.borrar_mensa)
            self.boton3 = ttk.Button(self.raiz, text="Cancelar",
                                     padding=(5, 5), command=quit)

            # Se definen las ubicaciones de los widgets en la
            # ventana asignando los valores de las opciones 'x' e 'y'
            # en píxeles.

            self.etiq1.place(x=30, y=40)
            self.etiq2.place(x=30, y=80)

            self.etiq3.place(x=150, y=120)
            self.ctext1.place(x=150, y=42)
            self.ctext2.place(x=150, y=82)
            #self.ctext3.place(x=150, y=122)
            self.separ1.place(x=5, y=145, bordermode=OUTSIDE,
                              height=20, width=420)
            self.boton1.place(x=50, y=160)
            self.boton2.place(x=170, y=160)
            self.boton3.place(x=290, y=160)
            self.ctext1.focus_set() #Para que posicione el cursor en la caja de texto

            # Mostrar la ventana
            self.raiz.mainloop()

        # Declara método para validar la contraseña y mostrar
        # un mensaje en la propia ventana, utilizando la etiqueta
        # 'self.mensa'. Cuando la contraseña es correcta se
        # asigna el color azul a la etiqueta 'self.etiq3' y
        # cuando es incorrecta el color rojo. Para ello. se emplea
        # el método 'configure()' que permite cambiar los valores
        # de las opciones de los widgets.

        def aceptar(self):
            #print self.usuario.get()
            funciones = Pyro4.Proxy("PYRONAME:" + self.servidor)
            usuario = funciones.validar_usuario(self.usuario.get())
            if usuario == True:
                password = funciones.validar_contrasena(self.clave.get())
                if password == True:
                    self.etiq3.configure(foreground='red')
                    self.mensa.set("Acceso permitido")
                    tipo =funciones.validar_tipo(self.clave.get())
                    if tipo ==True:
                        self.abrir()
                    else:
                        self.cliente()
                else:
                    self.etiq3.configure(foreground='blue')
                    self.mensa.set("contraseña incorrecta")

            else:
                self.etiq3.configure(foreground='blue')
                self.mensa.set("usuario incorrecto")

        def abrir(self):

            ''' Construye una ventana nueva ventana inhabilitando la anterior '''
            self.servidor = "Marcela.com"
            self.menu = Tk()
            self.menubarra = Menu(self.menu)

            # Crea un menu desplegable y lo agrega al barra de la ventana
            self.menu_alertas = Menu(self.menubarra, tearoff=0)
            self.menu_alertas.add_command(label="Monto Maximo", command=self.maximo)
            # self.menuarchivo.add_command(label="Guardar", command=self.hola)
            self.menu_alertas.add_separator()
            self.menu_alertas.add_command(label="Salir", command=self.raiz.quit)
            self.menubarra.add_cascade(label="Alertas", menu=self.menu_alertas)
            self.menu_loterias = Menu(self.menubarra, tearoff=0)
            self.menu_loterias.add_command(label="Agregar", command=self.loteria)
            self.menu_loterias.add_separator()
            self.menu_loterias.add_command(label="Listar", command=self.listar_loteria)
            self.menu_loterias.add_separator()
            self.menu_loterias.add_command(label="Actualizar", command=self.actualizar_loteria)
            self.menu_loterias.add_separator()
            self.menu_loterias.add_command(label="Salir", command=self.raiz.quit)
            self.menubarra.add_cascade(label="Loterias", menu=self.menu_loterias)

            self.menu_ventas = Menu(self.menubarra, tearoff=0)
            self.menu_ventas.add_command(label="Chances", command=self.hola)
            self.menu_ventas.add_separator()
            self.menu_ventas.add_command(label="Detalles", command=self.hola)
            self.menu_ventas.add_separator()
            self.menu_ventas.add_command(label="Ventas", command=self.hola)
            self.menu_ventas.add_separator()
            self.menu_ventas.add_command(label="Salir", command=self.raiz.quit)
            self.menubarra.add_cascade(label="Ventas", menu=self.menu_ventas)

            self.menu_usuario = Menu(self.menubarra, tearoff=0)
            self.menu_usuario.add_command(label="Crear", command=self.crear_usuario)
            self.menu_usuario.add_separator()
            self.menu_usuario.add_command(label="Listar", command=self.hola)
            self.menu_usuario.add_separator()
            self.menu_usuario.add_command(label="Puntos", command=self.hola)
            self.menu_usuario.add_separator()
            self.menu_usuario.add_command(label="Salir", command=self.raiz.quit)
            self.menubarra.add_cascade(label="Usuario", menu=self.menu_usuario)

            self.menu_log = Menu(self.menubarra, tearoff=0)
            self.menu_log.add_command(label="Reporte", command=self.hola)
            self.menu_log.add_separator()
            self.menu_log.add_command(label="Salir", command=self.raiz.quit)
            self.menubarra.add_cascade(label="Informes", menu=self.menu_log)

            # Mostrar el menu
            self.menu.config(menu=self.menubarra)

            self.menu.geometry('430x400+500+50')
            self.menu.resizable(0, 0)
            self.menu.title("Apuestas Azar")

        def crear_usuario(self):
            self.fuente = tkFont.Font(weight='bold')
            self.etiq1 = ttk.Label(self.menu, text="Cedula:",
                                   font=self.fuente)
            self.etiq2 = ttk.Label(self.menu, text="Nombre:",
                                   font=self.fuente)
            self.etiq3 = ttk.Label(self.menu, text="Tipo:",
                                   font=self.fuente)
            self.etiq4 = ttk.Label(self.menu, text="Email:",
                                   font=self.fuente)
            self.etiq5 = ttk.Label(self.menu, text="Contraseña:",
                                   font=self.fuente)

            self.mensa_3 = StringVar()
            self.etiq6 = ttk.Label(self.menu, textvariable=self.mensa_3,
                                   font=self.fuente, foreground='blue')

            self.cedula = StringVar()
            self.nombre = StringVar()
            self.tipo = StringVar()
            self.email = StringVar()
            self.contrasena = StringVar()

            self.ctext1 = ttk.Entry(self.menu,
                                    textvariable=self.cedula, width=30)
            self.ctext2 = ttk.Entry(self.menu,
                                    textvariable=self.nombre,
                                    width=30)
            self.ctext3 = ttk.Entry(self.menu,
                                    textvariable=self.tipo,
                                    width=30)
            self.ctext4 = ttk.Entry(self.menu,
                                    textvariable=self.email,
                                    width=30)
            self.ctext5 = ttk.Entry(self.menu,
                                    textvariable=self.contrasena,
                                    width=30,
                                    show="*")

            self.separ1 = ttk.Separator(self.menu, orient=HORIZONTAL)
            self.boton1 = ttk.Button(self.menu, text="Guardar",
                                     padding=(5, 5), command=self.crear)
            self.boton2 = ttk.Button(self.menu, text="Limpiar",
                                     padding=(5, 5), command=self.borrar_mensa)
            self.boton3 = ttk.Button(self.menu, text="Cancelar",
                                     padding=(5, 5), command=quit)

            # Se definen las ubicaciones de los widgets en la
            # ventana asignando los valores de las opciones 'x' e 'y'
            # en píxeles.

            self.etiq1.place(x=30, y=40)
            self.etiq2.place(x=30, y=80)
            self.etiq3.place(x=30, y=120)
            self.etiq4.place(x=30, y=160)
            self.etiq5.place(x=30, y=200)
            self.etiq5.place(x=30, y=205)

            self.ctext1.place(x=150, y=42)
            self.ctext2.place(x=150, y=82)
            self.ctext3.place(x=150, y=122)
            self.ctext4.place(x=150, y=162)
            self.ctext5.place(x=150, y=202)

            self.separ1.place(x=5, y=280, bordermode=OUTSIDE,
                              height=30, width=420)
            self.boton1.place(x=50, y=300)
            self.boton2.place(x=170, y=300)
            self.boton3.place(x=290, y=300)
            self.ctext1.focus_set()

            # Mostrar la ventana
            self.menu.mainloop()


        def crear(self):
            cedula = self.ctext1.get()
            usuario = self.ctext2.get()
            tipo = self.ctext3.get()
            correo = self.ctext4.get()
            contrasena = self.ctext5.get()
            funciones = Pyro4.Proxy("PYRONAME:" + self.servidor)
            usuario = funciones.crear_usuario(cedula, usuario, tipo, correo, contrasena)
            if usuario == True:
                mensa = ttk.Label(self.menu, foreground='red', text="Usuario Creado Satisfactoriamente"
                                                                    + self.cedula.get(), font=self.fuente).place(x=120,
                                                                                                                  y=240)

            else:
                mensa = ttk.Label(self.menu, foreground='Blue', text="Usuario No Creado"
                                                                     + self.cedula.get(), font=self.fuente).place(x=120,
                                                                                                                   y=160)


        def actualizar_loteria(self):
            self.fuente = tkFont.Font(weight='bold')
            self.etiq4 = ttk.Label(self.menu, text="Loteria:",
                                   font=self.fuente)
            self.etiq5 = ttk.Label(self.menu, text="Dia:",
                                   font=self.fuente)
            self.etiq6 = ttk.Label(self.menu, text="Numero:",
                                   font=self.fuente)

            # Declara una variable de cadena que se asigna a
            # la opción 'textvariable' de un widget 'Label' para
            # mostrar mensajes en la ventana. Se asigna el color
            # azul a la opción 'foreground' para el mensaje.

            self.mensa_2 = StringVar()
            self.etiq7 = ttk.Label(self.menu, textvariable=self.mensa_2,
                                   font=self.fuente, foreground='blue')

            self.loteria = StringVar()
            self.dia = StringVar()
            self.numero = StringVar()
            self.ctext5 = ttk.Entry(self.menu,
                                    textvariable=self.loteria, width=30)
            self.ctext6 = ttk.Entry(self.menu,
                                    textvariable=self.dia,
                                    width=30)
            self.ctext7 = ttk.Entry(self.menu,
                                    textvariable=self.numero,
                                    width=30)
            self.separ1 = ttk.Separator(self.menu, orient=HORIZONTAL)
            self.boton1 = ttk.Button(self.menu, text="Guardar",
                                     padding=(5, 5), command=self.agregar)
            self.boton2 = ttk.Button(self.menu, text="Limpiar",
                                     padding=(5, 5), command=self.borrar_mensa)
            self.boton3 = ttk.Button(self.menu, text="Cancelar",
                                     padding=(5, 5), command=quit)

            # Se definen las ubicaciones de los widgets en la
            # ventana asignando los valores de las opciones 'x' e 'y'
            # en píxeles.

            self.etiq4.place(x=30, y=40)
            self.etiq5.place(x=30, y=80)
            self.etiq6.place(x=30, y=120)
            # self.etiq6.place(x=150, y=120)
            self.ctext5.place(x=150, y=42)
            self.ctext6.place(x=150, y=82)
            self.ctext7.place(x=150, y=122)
            self.separ1.place(x=5, y=200, bordermode=OUTSIDE,
                              height=30, width=420)
            self.boton1.place(x=50, y=300)
            self.boton2.place(x=170, y=300)
            self.boton3.place(x=290, y=300)
            self.ctext5.focus_set()

            # Mostrar la ventana
            self.menu.mainloop()

        def agregar(self):
            loteria = self.ctext5.get()
            dia = self.ctext6.get()
            numero = self.ctext7.get()
            funciones = Pyro4.Proxy("PYRONAME:" + self.servidor)
            loterias = funciones.actualizar_loteria(loteria, dia,numero)
            if loterias == True:
                mensa = ttk.Label(self.menu, foreground='red', text="Loteria Actualizada Satisfactoriamente"
                                                                    + self.loteria.get(), font=self.fuente).place(x=120,
                                                                                                                  y=160)

            else:
                mensa = ttk.Label(self.menu, foreground='Blue', text="Loteria No Agregada"
                                                                     + self.loteria.get(), font=self.fuente).place(x=120,
                                                                                                                   y=160)

        def listar_loteria(self):
            funciones = Pyro4.Proxy("PYRONAME:" + self.servidor)
            loterias = funciones.ver_loterias()
            lista = json.loads(loterias)
            Lb1 = Listbox(self.menu,x=30, y=40)
            con=1
            for i in lista:
                Lb1.insert(con, ast.literal_eval(json.dumps(i)))
                con+=1
            Lb1.pack()

            #mensa = ttk.Label(self.menu, foreground='black',
            #                  text=loterias,
            #                  font=self.fuente).place(x=20,y=80)

            # Declara un método para borrar el mensaje anterior y
            # la caja de entrada de la contraseña
        def borrar_mensa(self):
            self.usuario.set("")
            self.clave.set("")

        def borrar_mensa_1(self):
            self.loteria.set("")
            self.dia.set("")

        def hola(self):
            pass



        def hacer_chance(self):
            self.fuente = tkFont.Font(weight='bold')
            self.etiq1 = ttk.Label(self.menu_c, text="# Chance:",
                                   font=self.fuente)
            self.etiq2 = ttk.Label(self.menu_c, text="Loteria:",
                                   font=self.fuente)
            self.etiq3 = ttk.Label(self.menu_c, text="Cantidad:",
                                   font=self.fuente)
            self.etiq4 = ttk.Label(self.menu_c, text="Pago:",
                                   font=self.fuente)

            self.mensa_4 = StringVar()
            self.etiq5 = ttk.Label(self.menu_c, textvariable=self.mensa_4,
                                   font=self.fuente, foreground='blue')

            self.chance = StringVar()
            self.loteria = StringVar()
            self.cantidad = StringVar()
            self.pago = StringVar()

            self.ctext1 = ttk.Entry(self.menu_c,
                                    textvariable=self.chance, width=30)
            self.ctext2 = ttk.Entry(self.menu_c,
                                    textvariable=self.loteria,
                                    width=30)
            self.ctext3 = ttk.Entry(self.menu_c,
                                    textvariable=self.cantidad,
                                    width=30)
            self.ctext4 = ttk.Entry(self.menu_c,
                                    textvariable=self.pago,
                                    width=30)

            self.separ1 = ttk.Separator(self.menu_c, orient=HORIZONTAL)
            self.boton1 = ttk.Button(self.menu_c, text="Agregar",
                                     padding=(5, 5), command=self.chances)
            self.boton2 = ttk.Button(self.menu_c, text="Limpiar",
                                     padding=(5, 5), command=self.borrar_mensa)
            self.boton3 = ttk.Button(self.menu_c, text="Cancelar",
                                     padding=(5, 5), command=quit)

            # Se definen las ubicaciones de los widgets en la
            # ventana asignando los valores de las opciones 'x' e 'y'
            # en píxeles.

            self.etiq1.place(x=30, y=40)
            self.etiq2.place(x=30, y=80)
            self.etiq3.place(x=30, y=120)
            self.etiq4.place(x=30, y=160)
            self.etiq5.place(x=30, y=200)


            self.ctext1.place(x=150, y=42)
            self.ctext2.place(x=150, y=82)
            self.ctext3.place(x=150, y=122)
            self.ctext4.place(x=150, y=162)


            self.separ1.place(x=5, y=280, bordermode=OUTSIDE,
                              height=30, width=420)
            self.boton1.place(x=50, y=300)
            self.boton2.place(x=170, y=300)
            self.boton3.place(x=290, y=300)
            self.ctext1.focus_set()

            # Mostrar la ventana
            self.menu_c.mainloop()


        def chances(self):
            chance = self.ctext1.get()
            loteria = self.ctext2.get()
            cantidad = self.ctext3.get()
            pago = self.ctext4.get()
            funciones = Pyro4.Proxy("PYRONAME:" + self.servidor)
            usuario = funciones.generar_chance(chance, loteria, cantidad, pago)
            if usuario == True:
                mensa = ttk.Label(self.menu_c, foreground='red', text="Chance generado Satisfactoriamente"
                                                                    + self.chance.get(), font=self.fuente).place(x=120,
                                                                                                                 y=240)

            else:
                mensa = ttk.Label(self.menu_c, foreground='Blue', text="Chance No Creado"
                                                                     + self.chance.get(), font=self.fuente).place(x=120,
                                                                                                                  y=160)

        def maximo(self):
            funciones = Pyro4.Proxy("PYRONAME:" + self.servidor)
            maximo = funciones.maximo()
            #self.etiq3.configure(foreground='black')
            #self.mensa.set(maximo)

            print maximo

        def loteria(self):

            self.fuente = tkFont.Font(weight='bold')
            self.etiq4 = ttk.Label(self.menu, text="Loteria:",
                                   font=self.fuente)
            self.etiq5 = ttk.Label(self.menu, text="Dia:",
                                   font=self.fuente)

            # Declara una variable de cadena que se asigna a
            # la opción 'textvariable' de un widget 'Label' para
            # mostrar mensajes en la ventana. Se asigna el color
            # azul a la opción 'foreground' para el mensaje.

            self.mensa_1 = StringVar()
            self.etiq6 = ttk.Label(self.menu, textvariable=self.mensa_1,
                                   font=self.fuente, foreground='blue')

            self.loteria = StringVar()
            self.dia = StringVar()
            self.ctext3 = ttk.Entry(self.menu,
                                    textvariable=self.loteria, width=30)
            self.ctext4 = ttk.Entry(self.menu,
                                    textvariable=self.dia,
                                    width=30)
            self.separ1 = ttk.Separator(self.menu, orient=HORIZONTAL)
            self.boton1 = ttk.Button(self.menu, text="Guardar",
                                     padding=(5, 5), command=self.guardar)
            self.boton2 = ttk.Button(self.menu, text="Limpiar",
                                     padding=(5, 5), command=self.borrar_mensa)
            self.boton3 = ttk.Button(self.menu, text="Cancelar",
                                     padding=(5, 5), command=quit)

            # Se definen las ubicaciones de los widgets en la
            # ventana asignando los valores de las opciones 'x' e 'y'
            # en píxeles.

            self.etiq4.place(x=30, y=40)
            self.etiq5.place(x=30, y=80)
            #self.etiq6.place(x=150, y=120)
            self.ctext3.place(x=150, y=42)
            self.ctext4.place(x=150, y=82)
            self.separ1.place(x=5, y=145, bordermode=OUTSIDE,
                              height=10, width=420)
            self.boton1.place(x=50, y=160)
            self.boton2.place(x=170, y=160)
            self.boton3.place(x=290, y=160)
            self.ctext3.focus_set()

            # Mostrar la ventana
            self.menu.mainloop()

        def guardar(self):
            loteria =self.ctext3.get()
            dia =self.ctext4.get()
            funciones = Pyro4.Proxy("PYRONAME:" + self.servidor)
            loterias = funciones.agregar_loteria(loteria,dia)
            if loterias == True:
                mensa = ttk.Label(self.menu, foreground='red',  text="Loteria Creada Satisfactoriamente"
                                 +self.loteria.get(),font=self.fuente).place(x=150, y=120)

            else:
                mensa = ttk.Label(self.menu, foreground='Blue', text="Loteria No Agregada"
                                 +self.loteria.get(), font=self.fuente).place(x=150,y=120)



#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        def cliente(self):

            ''' Construye una ventana nueva ventana inhabilitando la anterior '''
            self.servidor = "Marcela.com"
            self.menu_c = Tk()
            self.menubarra = Menu(self.menu_c)

            # Crea un menu desplegable y lo agrega al barra de la ventana
            self.menu_chance = Menu(self.menubarra, tearoff=0)
            self.menu_chance.add_command(label="Numeros Suerte", command=self.maximo)
            self.menu_chance.add_separator()
            self.menu_chance.add_command(label="Chance", command=self.hacer_chance)
            self.menu_chance.add_separator()
            self.menu_chance.add_command(label="Salir", command=self.raiz.quit)
            self.menubarra.add_cascade(label="Hacer Chances", menu=self.menu_chance)


            self.menu_puntos = Menu(self.menubarra, tearoff=0)
            self.menu_puntos.add_command(label="Ver Puntos", command=self.loteria)
            self.menu_puntos.add_separator()
            self.menu_puntos.add_command(label="Cambiar Puntos", command=self.cambio_producto)
            self.menu_puntos.add_separator()
            self.menu_puntos.add_command(label="Salir", command=self.raiz.quit)
            self.menubarra.add_cascade(label="Puntos", menu=self.menu_puntos)

            self.menu_ventas = Menu(self.menubarra, tearoff=0)
            self.menu_ventas.add_command(label="Ver Chances", command=self.hola)
            self.menu_ventas.add_separator()
            self.menu_ventas.add_command(label="Detalles", command=self.hola)
            self.menu_ventas.add_separator()
            self.menu_ventas.add_command(label="Salir", command=self.raiz.quit)
            self.menubarra.add_cascade(label="Chances", menu=self.menu_ventas)

            # Mostrar el menu
            self.menu_c.config(menu=self.menubarra)

            self.menu_c.geometry('430x400+500+50')
            self.menu_c.resizable(0, 0)
            self.menu_c.title("Apuestas Azar")

        def cambio_producto(self):
            self.fuente = tkFont.Font(weight='bold')  # Tipo de letra
            self.etiq1 = ttk.Label(self.menu_c, text="Producto:",
                                   font=self.fuente)


            # Declara una variable de cadena que se asigna a
            # la opción 'textvariable' de un widget 'Label' para
            # mostrar mensajes en la ventana. Se asigna el color
            # azul a la opción 'foreground' para el mensaje.

            self.mensa_5 = StringVar()
            self.etiq2 = ttk.Label(self.menu_c, textvariable=self.mensa_5,
                                   font=self.fuente, foreground='blue')

            self.producto = StringVar()
            self.ctext1 = ttk.Entry(self.menu_c,
                                    textvariable=self.producto, width=30)
            self.separ1 = ttk.Separator(self.menu_c, orient=HORIZONTAL)
            self.boton1 = ttk.Button(self.menu_c, text="Cambiar",
                                     padding=(5, 5), command=self.productos)
            self.boton2 = ttk.Button(self.menu_c, text="Limpiar",
                                     padding=(5, 5), command=self.borrar_mensa)
            self.boton3 = ttk.Button(self.menu_c, text="Cancelar",
                                     padding=(5, 5), command=quit)

            # Se definen las ubicaciones de los widgets en la
            # ventana asignando los valores de las opciones 'x' e 'y'
            # en píxeles.

            self.etiq1.place(x=30, y=40)
            self.etiq2.place(x=30, y=80)
            self.ctext1.place(x=150, y=42)
            self.separ1.place(x=5, y=145, bordermode=OUTSIDE,
                              height=20, width=420)
            self.boton1.place(x=50, y=160)
            self.boton2.place(x=170, y=160)
            self.boton3.place(x=290, y=160)
            self.ctext1.focus_set()  # Para que posicione el cursor en la caja de texto

            # Mostrar la ventana
            self.menu_c.mainloop()

        def productos(self):
            producto = self.ctext1.get()
            funciones = Pyro4.Proxy("PYRONAME:" + self.servidor)
            loterias = funciones.cambiar_producto(producto)
            if loterias == True:
                mensa = ttk.Label(self.menu_c, foreground='red', text="Puntos Cambiados Exitosamente"
                                                                    + self.producto.get(), font=self.fuente).place(x=30,
                                                                                                                  y=120)

            else:
                mensa = ttk.Label(self.menu_c, foreground='Blue', text="No Posee los puntos necesarios para obtener el producto"
                                                                     + self.producto.get(), font=self.fuente).place(x=15,
                                                                                                                    y=120)




def main():
    mi_app = Aplicacion()
    #return 0

def conectar():
    servidor ="Marcela.com"
    funciones = Pyro4.Proxy("PYRONAME:"+servidor)


if __name__ == '__main__':
    main()


    #http://python-para-impacientes.blogspot.com.co/2015/12/tkinter-disenando-ventanas-graficas.html