#!/usr/bin/python
# -*- coding: utf-8 -*-

# python -m Pyro4.naming

import Pyro4
import random
import json
import time
import os
import MySQLdb
import datetime

@Pyro4.expose

class Funciones():

    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASS = ''
    DB_NAME = 'apuestas_azar'


    def run_query(self,query=''):
        datos = [self.DB_HOST, self.DB_USER, self.DB_PASS, self.DB_NAME]

        conn = MySQLdb.connect(*datos)  # Conectar a la base de datos
        cursor = conn.cursor()  # Crear un cursor
        cursor.execute(query)  # Ejecutar una consulta

        if query.upper().startswith('SELECT'):
            data = cursor.fetchall()  # Traer los resultados de un select
        else:
            conn.commit()  # Hacer efectiva la escritura de datos
            data = None

        cursor.close()  # Cerrar el cursor
        conn.close()  # Cerrar la conexión

        return data

    def validar_usuario(self,cadena):
        lista =[[cadena]]
        query = "SELECT email FROM usuarios WHERE email = '%s'" % cadena
        result = self.run_query(query)
        usuario = json.dumps(result)
        validar = json.dumps(lista)

        if(usuario == validar):
            return True
        else:
            return False

    def validar_contrasena(self,cadena):
        lista =[[cadena]]
        query = "SELECT contrasena FROM usuarios WHERE contrasena = '%s'" % (cadena)
        result = self.run_query(query)
        contrasena = json.dumps(result)
        validar = json.dumps(lista)

        if (contrasena == validar):
            return True
        else:
            return False

    def validar_tipo(self,cadena):
        lista =[["Administrador"]]
        query = "SELECT tipo_usuario FROM usuarios WHERE contrasena = '%s'" % (cadena)
        result = self.run_query(query)
        contrasena = json.dumps(result)
        validar = json.dumps(lista)
        if (contrasena == validar):
            return True
        else:
            return False

    def agregar_loteria(self,loteria, dia):
        numero = int(1985)
        query = "INSERT INTO loteria (nombre,dia,numero) VALUES ('%s','%s','%s')" % (loteria, dia, numero)
        self.run_query(query)
        return True

    def actualizar_loteria(self,nombre, dia, numero):
        query = "UPDATE loteria SET numero=%i WHERE nombre = '%s' and dia ='%s' " % (int(numero), nombre, dia)
        self.run_query(query)
        return True


    def crear_usuario(self,cedula, usuario, tipo, correo, contrasena):
        fecha = datetime.date.today()
        hoy = fecha.strftime("%d/%m/%y")
        query = "INSERT INTO usuarios (cedula,nombre_usuario,tipo_usuario,email,contrasena,fecha_registro)VALUES('%s','%s','%s','%s','%s','%s')" % (
        cedula, usuario, tipo, correo, contrasena, hoy)
        self.run_query(query)
        return True


    def maximo(self):
        query = "SELECT sum(pago_ganador) FROM aciertos"
        result = self.run_query(query)
        cadena = json.dumps(result)
        valor = [["20000000.0"]]
        print cadena
        if cadena > valor:
            lista = ["No se puede realizar mas chances, Excedio el limite de pago"]
        else:
            lista = ["No hay problemas de limite de pago"]

        enviar = json.dumps(lista)
        return enviar

    def ver_loterias(self):
        dia_loteria = time.strftime("%A")
        dia = self.convertir(dia_loteria)

        query = "SELECT nombre FROM loteria WHERE dia = '%s'" % dia
        result = self.run_query(query)
        cadena = json.dumps(result)
        return cadena

    def generar_chance(self, chance, loteria, valor, dinero_cliente):
        comprador ="Fernando"
        fecha = datetime.date.today()
        hoy = fecha.strftime("%d/%m/%y")
        hora = time.strftime("%X")
        acierto = [[chance]]
        query = "INSERT INTO chance (nombre_comprador,numero_chance,loteria,valor,fecha,hora)VALUES('%s','%s','%s','%s','%s','%s')" % (
        comprador, chance, loteria, valor, hoy, hora)
        self.run_query(query)

        valors=int(valor)

        puntos = valors / 100
        print str(puntos)

        query = "INSERT INTO puntos (nombre_persona,puntos) VALUES('%s','%s')" % (comprador, str(puntos))
        self.run_query(query)

        pago = valors * 5000

        query = "SELECT numero FROM loteria WHERE numero = '%s'" % chance
        result = self.run_query(query)
        cadena = json.dumps(result)

        if acierto == cadena:
            query = "INSERT INTO aciertos (nombre_ganador,loteria,numero_chance,valor_chance,fecha,pago_ganador)VALUES('%s','%s','%s','%s','%s','%s')" % (
            comprador, loteria, chance, valor, hoy, str(pago))
            self.run_query(query)
        return True

    def cambiar_producto(self,producto):
        comprador ="Fernando"

        query = "SELECT puntos FROM puntos WHERE nombre_persona = '%s'" % comprador
        result = self.run_query(query)
        puntos = json.dumps(result)

        query = "SELECT puntos FROM productos WHERE nombre_producto = '%s'" % producto
        result = self.run_query(query)
        puntos_producto = json.dumps(result)
        print puntos_producto

        if puntos == puntos_producto:
            return True
        else:
            return False





    def convertir(self,dia):

        if dia == "Monday":
            dia_loteria = "Lunes"
        if dia == "Tuesday":
            dia_loteria = "Martes"

        if dia == "Wednesday":
            dia_loteria = "Miercoles"

        if dia == "Thursday":
            dia_loteria = "Jueves"

        if dia == "Friday":
            dia_loteria = "Viernes"

        if dia == "Saturday":
            dia_loteria = "Sabado"

        if dia == "Sunday":
            dia_loteria = "Domingo"

        return dia_loteria


def main():
    demonio = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri =  demonio.register(Funciones)
    ns.register("Marcela.com", uri)
    demonio.requestLoop()

if __name__ == '__main__':
    main()