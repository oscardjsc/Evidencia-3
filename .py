from ast import Continue
import datetime
import time

import openpyxl
import random

import sqlite3
from sqlite3 import Error

try:
    with sqlite3.connect("PrimerIntentoEvidencia3.db") as conn:
        mi_cursor = conn.cursor()
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS cliente (num_cliente INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL);")
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS sala (num_sala INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, cap_sala INTEGER NOT NULL);")
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS reservacion (folio_reservacion INTEGER PRIMARY KEY AUTOINCREMENT, num_sala INTEGER NOT NULL, num_cliente INTEGER NOT NULL, nombre_evento TEXT NOT NULL, fecha_reservacion timestamp, turno_reservacion TEXT NOT NULL,  FOREIGN KEY(num_sala) REFERENCES sala(num_sala), FOREIGN KEY(num_cliente) REFERENCES cliente(num_cliente));")
        print("Tablas creadas exitosamente")
finally:
  conn.close()

turnos = {1:"Matutino", 2:"Vespertino", 3:"Nocturno"}

fecha_actual = datetime.date.today()
diferencia_dias = 2
fecha_reservacion_procesada = ""

turnos = {1:"Matutino", 2:"Vespertino", 3:"Nocturno"}
lista_encontrados = []
reservaciones_posibles = []
reservaciones_posibles_final = []

while True:
    print("Bienvenidos al sistema para la reservacion de renta de espacios coworking")

    print("\t [A]Reservaciones")

    print("\t [B]Reportes")

    print("\t [C]Registrar una sala")

    print("\t [D]Registrar un cliente")

    print("\t [E]Salir")

    opcion=input("Elije la opcion deseada, oprimiendo la tecla de la letra que corresponda: ")
    print("*" * 60)

    if (not opcion.upper() in "ABCDE"):
            print("Opcion incorrecta, favor de volver a intentarlo")
            print("*" * 60)

    if (opcion.upper()== "A"):
        while True:
            print("\t [A]Registrar una nueva reservacion")
            print("\t [B]Modificar descripcion de una reservacion")
            print("\t [C]Consultar disponibilidad de una fecha")
            print("\t [D]Eliminar una reservacion")
            print("\t [E]Volver al menu principal")

            opcion2=input("Elije la opcion deseada, oprimiendo la tecla de la letra que corresponda: ")
            print("*" * 60)

            if (not opcion2.upper() in "ABCDE"):
                print("Opcion incorrecta, favor de volver a intentarlo")
                print("*" * 60)

            if (opcion2.upper()== "A"):
              while True:
                try:
                  respuesta = int(input("Ingresar su numero de cliente: "))
                  print("*" * 60)
                  break
                except ValueError:
                  print("El numero de cliente no puede omitirse ni ser de caracter string, favor de intentarlo nuevamente")
                  continue

              with sqlite3.connect("PrimerIntentoEvidencia3.db") as conn:
                mi_cursor = conn.cursor()
                mi_cursor.execute("SELECT num_cliente FROM cliente")
                registros = mi_cursor.fetchall()
                if registros is None:
                  break
                  
                  
              if (respuesta,) in registros:
                while True:
                  try:
                    sala = int(input("Ingresa el numero de sala que sera utilizada: "))
                    print("*" * 60)
                    break
                  except ValueError:
                      print("El numero de sala no puede omitirse ni ser de caracter string, favor de intentarlo nuevamente")
                      continue


                with sqlite3.connect("PrimerIntentoEvidencia3.db") as conn:
                  mi_cursor = conn.cursor()
                  mi_cursor.execute("SELECT num_sala FROM sala")
                  registros = mi_cursor.fetchall()

                  if (sala,) in registros: 
                    while True:
                      nombre_evento=input("¿Cual es el nombre de su evento?: ")
                      if nombre_evento == "":
                        print("El nombre del evento no se debe de omitir, favor de intentarlo nuevamente")
                        print("*" * 60)
                      else:
                          break
                    while True:
                      try:
                        fecha_reservacion = input("¿Cual seria la fecha en que deseea realizar su reservacion? (DD/MM/AAAA): ")
                        if fecha_reservacion == "":
                          print("La fecha de reservacion no se debe de omitir, favor de intentarlo nuevamente")
                          print("*" * 60)
                          continue
                        fecha_reservacion_procesada = datetime.datetime.strptime(fecha_reservacion, "%d/%m/%Y").date()
                        break
                      except ValueError:
                        print("Formato de fecha no valido, favor de volver a intentarlo")

                    diferencia_dias=fecha_reservacion_procesada - fecha_actual
                    if diferencia_dias.days <=2:
                      print("La reservacion de una sala, tiene que ser por lo minimo 2 dias con anterioridad")
                      print("*" * 60)
                      break
                    else:
                      while True:
                        try:
                          turno_reservacion = int(input("Favor de seleccionar el turno deseado (1. Matutino, 2. Vespertino, 3. Nocturno): "))
                          if turno_reservacion == 1:
                            turno_reservacion = "Matutino"
                            break
                          elif turno_reservacion == 2:
                             turno_reservacion = "Vespertino"
                             break 
                          elif turno_reservacion == 3:
                             turno_reservacion = "Nocturno"
                             break    
                          else:
                            print("Eleccion erronea, favor de volver a intentarlo")
                            print("*" * 60)
                            continue
                        except ValueError:
                            print("El numero de sala no puede omitirse ni ser de caracter string, favor de intentarlo nuevamente")
                            print("*" * 60)
                            continue
                           
                            

                    with sqlite3.connect("PrimerIntentoEvidencia3.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
                      mi_cursor = conn.cursor()
                      valores = {"num_sala":sala, "nombre_evento":nombre_evento, "fecha_reservacion":fecha_reservacion_procesada, "turno_reservacion":turno_reservacion}
                      mi_cursor.execute("SELECT count(*) FROM reservacion WHERE num_sala=:num_sala AND DATE(fecha_reservacion)=:fecha_reservacion AND turno_reservacion=:turno_reservacion", valores)
                      registros2 = mi_cursor.fetchall()
                                            

                      if (1,) in registros2:
                        print("Lo sentimos, ya existe una reservacion para esta sala, en el dia y turno seleccionado")
                        print("*" * 60)
                        break
                      else:
                        with sqlite3.connect("PrimerIntentoEvidencia3.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
                          mi_cursor = conn.cursor()
                          valores = {"num_sala":sala,"cliente":respuesta, "nombre_evento":nombre_evento, "fecha_reservacion":fecha_reservacion_procesada, "turno_reservacion":turno_reservacion}
                          mi_cursor.execute("INSERT INTO reservacion VALUES(NULL, :num_sala,:cliente, :nombre_evento, :fecha_reservacion, :turno_reservacion)", valores)
                        with sqlite3.connect("PrimerIntentoEvidencia3.db") as conn:
                          mi_cursor = conn.cursor()
                          valores = {"num_sala":sala, "nombre_evento":nombre_evento, "fecha_reservacion":fecha_reservacion_procesada, "turno_reservacion":turno_reservacion}
                          mi_cursor.execute("SELECT folio_reservacion FROM reservacion WHERE num_sala=:num_sala AND DATE(fecha_reservacion)=:fecha_reservacion AND turno_reservacion=:turno_reservacion", valores)
                          registros = mi_cursor.fetchall()  
                          for folio, in registros:
                            folio_imprimir=folio                                             
                          print(f"Registro agregado exitosamente, su numero de folio de reservacion es {folio_imprimir} ")
                          break
                  else:
                      print("Sala seleccionada no existente")
                      print("*" * 60)
                      break
              else:
                  print("Para realizar una reservacion es necesario ser cliente registrado, favor de primero hacer su registro")
                  print("*" * 60)
                  break
              break


            if (opcion2.upper()== "B"):
              while True:
                try:
                    folio_reservacion = int(input("¿Cual es el numero de folio de su reservacion?: "))
                    print("*" * 60)
                    break
                except ValueError:
                  print("El folio de reservacion no se puede omitir ni ser caracteres alfanumericos, favor de intentarlo nuevamente")
                  print("*" * 60)


              with sqlite3.connect("PrimerIntentoEvidencia3.db") as conn:
                mi_cursor = conn.cursor()
                valores = {"folio_reservacion":folio_reservacion}
                mi_cursor.execute("SELECT folio_reservacion FROM reservacion WHERE folio_reservacion=:folio_reservacion", valores)
                registros = mi_cursor.fetchall()


                if (folio_reservacion,) in registros:
                  while True:
                    nuevo_nombre = input("¿Cual sera el nuevo nombre de su evento: ")
                    if nuevo_nombre == "":
                      print("El nuevo nombre no se debe de omitir, favor de intentarlo nuevamente")
                      print("*" * 60)
                    else:
                      break                                      
                      print("*" * 60)
                  with sqlite3.connect("PrimerIntentoEvidencia3.db") as conn:
                    mi_cursor = conn.cursor()
                    valores = {"nuevo_nombre":nuevo_nombre, "folio_reservacion":folio_reservacion} 
                    mi_cursor.execute("UPDATE reservacion SET nombre_evento=:nuevo_nombre WHERE folio_reservacion=:folio_reservacion", valores)
                    print("Descripcion modificada exitosamente")
                    print("*" * 60)
                    break
                else:
                    print("El numero de folio de reservacion no fue encontrado")
                    print("*" * 60)
                    break



                
            if (opcion2.upper()== "C"):
              while True:
                try:
                  fecha_buscada=input("Ingresa la fecha buscada:")
                  if fecha_buscada == "":
                    print("La fecha buscada no se debe de omitir, favor de intentarlo nuevamente")
                    print("*" * 60)
                    continue
                  fecha_reservacion_procesada2 = datetime.datetime.strptime(fecha_buscada, "%d/%m/%Y").date() 
                  break
                except ValueError:
                  print("Formato de fecha no valido, favor de volver a intentarlo")
                  print("*" * 60)    

              with sqlite3.connect("PrimerIntentoEvidencia3.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
                mi_cursor = conn.cursor()
                valores = {"fecha_buscada":fecha_reservacion_procesada2}
                mi_cursor.execute("SELECT num_sala, turno_reservacion FROM reservacion WHERE DATE(fecha_reservacion)=:fecha_buscada", valores)
                registros = mi_cursor.fetchall()     

                for sala, turno in registros:
                  lista_encontrados.append((sala,turno))
                
    
                reservaciones_encontradas=set(lista_encontrados)                  

                mi_cursor.execute("SELECT num_sala FROM sala")
                registros2 = mi_cursor.fetchall() 
                for sala, in registros2:
                  for eleccion in turnos.items():
                    reservaciones_posibles.append((sala,eleccion[1]))

                for elemento in reservaciones_posibles:
                  if elemento not in reservaciones_posibles_final:
                      reservaciones_posibles_final.append(elemento)
                
                reservaciones_posibles_realizar=set(reservaciones_posibles_final)
                total=  sorted(reservaciones_posibles_realizar - reservaciones_encontradas)
                print(f'LA DISPONIBILIDAD PARA EL DIA {fecha_buscada} ES LA SIGUIENTE: ')
                print("Sala        Turno")
                for datos in total:
                  print(f'{datos[0]}        {datos[1]} ')
                print("*" * 60)
                break                
              break

            if (opcion2.upper()== "D"):
              while True:
                try:
                  folio =int(input("Ingresa el numero de folio de la reservacion que deseas eliminar: "))
                  print("*" * 60)
                  break
                except ValueError:
                  print("El folio de la reservacion a eliminar, no se debe de omitir ni ser caracteres alfanumericos, favor de intentarlo nuevamente")
                  print("*" * 60)
              while True:
                try:
                  fecha_eliminar = input("Ingresa la fecha en la que la reservacion esta agendada (DD/MM/AAAA): ")
                  if fecha_eliminar == "":
                    print("La fecha buscada no se debe de omitir, favor de intentarlo nuevamente")
                    print("*" * 60)
                    continue
                  fecha_eliminar_procesada = datetime.datetime.strptime(fecha_eliminar, "%d/%m/%Y").date()
                  break
                except ValueError:
                  print("Formato de fecha no valido, favor de volver a intentarlo")
                  print("*" * 60)
                  
              with sqlite3.connect("PrimerIntentoEvidencia3.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
                mi_cursor = conn.cursor()
                valores = {"folio":folio, "fecha_eliminar":fecha_eliminar_procesada}
                mi_cursor.execute("SELECT count(*) FROM reservacion WHERE folio_reservacion=:folio AND fecha_reservacion=:fecha_eliminar ", valores)
                registros = mi_cursor.fetchall()
                                        
                if (0,) in registros:
                  print("No se encontre ningun folio con el numero y fecha ingresada, favor de verificar los valores ingresados")
                  print("*" * 60)
                  break
                else:
                   with sqlite3.connect("PrimerIntentoEvidencia3.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
                      mi_cursor = conn.cursor()
                      valores = {"folio":folio, "fecha_eliminar":fecha_eliminar_procesada}
                      mi_cursor.execute("SELECT folio_reservacion, num_sala, num_cliente, nombre_evento, DATE(fecha_reservacion), turno_reservacion FROM reservacion WHERE folio_reservacion=:folio AND DATE(fecha_reservacion)=:fecha_eliminar", valores)
                      registros = mi_cursor.fetchall()

                      print("LOS DATOS DEL FOLIO DE RESERVACION INGRESADOS SON LOS SIGUIENTE:")
                      print("*" * 60)
                      for folio_reservacion, num_sala, num_cliente, nombre_evento, fecha_reservacion, turno_reservacion  in registros:
                          print(f"Folio de Reservacion = {folio_reservacion}")
                          print(f"Numero de Sala = {num_sala}")
                          print(f"Numero de Cliente = {num_cliente}")
                          print(f"Nombre de Evento = {nombre_evento}")
                          print(f"Fecha de reservacion = {fecha_reservacion}")
                          print(f"Turno de reservacion = {turno_reservacion}")

                      
                      diferencia_dias2=fecha_eliminar_procesada - fecha_actual
                      if diferencia_dias2.days <=3:
                        print("*" * 60)
                        print("La eliminacion de la reservacion no se puede realizar a menos de 3 dias de anticipacion del evento")
                        break
                      else:
                        print("¡RECUERDA QUE AL ELIMINAR UNA RESERVACION, ESO NO PODRA SER DESECHO!")
                        print("*" * 60)
                        while True:
                          try:
                            decision_eliminar=int(input("Desea eliminar la reservacion: 1.Si  2.No: "))
                            print("*" * 60)
                            break
                          except ValueError:
                            print("La respuesta ingresada no fue correcta, favor de volver a intentarlo")
                        print("*" * 60)
                        if decision_eliminar==1:
                          with sqlite3.connect("PrimerIntentoEvidencia3.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
                              mi_cursor = conn.cursor()
                              valores = {"folio":folio, "fecha_eliminar":fecha_eliminar_procesada}
                              mi_cursor.execute("DELETE FROM reservacion WHERE folio_reservacion=:folio", valores)
                              registros = mi_cursor.fetchall()
                              print("Eliminacion de la reservacion hecha con exito")
                              print("*" * 60)
                              break
                        elif decision_eliminar==2:
                          print("Eliminacion cancelada")
                          print("*" * 60)
                          break
                        else:
                          print("Opcion incorrecta, eliminacion no realizada")



            if (opcion2.upper()== "E"):
              break

    if (opcion.upper()== "B"):
        while True:
            print("\t [A]Reporte en pantalla de reservaciones en una fecha")
            print("\t [B]Exportar reporte tabular en excel")
            print("\t [C]Volver al menu principal")

            opcion3=input("Elije la opcion deseada, oprimiendo la tecla de la letra que corresponda: ")
            print("*" * 60)

            if (not opcion3.upper() in "ABC"):
                print("Opcion incorrecta, favor de volver a intentarlo")
                print("*" * 60)

            if (opcion3.upper()=="A"):
              while True:
                try:
                  fecha_mostrar= input("¿Cual seria la fecha en que deseea ver las reservaciones realizadas? (DD/MM/AAAA): ")
                  if fecha_mostrar == "":
                    print("No se ingreso ningun dato, favor de volver a intentarlo")
                    print("*"*60)
                    continue
                  fecha_mostrar_procesada = datetime.datetime.strptime(fecha_mostrar, "%d/%m/%Y").date()
                  break
                except ValueError:
                  print("Formato de fecha no valido, favor de volver a intentarlo")
                  print("*"*60)

              with sqlite3.connect("PrimerIntentoEvidencia3.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
                mi_cursor = conn.cursor()
                valores = {"fecha_mostrar":fecha_mostrar_procesada}
                mi_cursor.execute("SELECT num_sala, num_cliente, nombre_evento, turno_reservacion FROM reservacion WHERE DATE(fecha_reservacion)=:fecha_mostrar", valores)
                registros = mi_cursor.fetchall() 

                if registros:
                  print("*" * 60)
                  print(f'REPORTE DE RESERVACIONES DEL DIA {fecha_mostrar}')
                  print("*" * 60)
                  print("Sala    Numero de Cliente       Nombre de reservacion        Turno")
                  print("*" * 80)
                  for sala, cliente, evento, turno in registros:
                    print(f'{sala}                {cliente}                     {evento}              {turno}')
                  break
                else:
                  print("No se cuentan con reservaciones agendadas para la fecha buscada")
                  break

            
            if (opcion3.upper()=="B"):
              while True:
                try:
                  fecha_exportar= input("¿Cual seria la fecha en que deseea obtener el reporte de reservaciones en Excel? (DD/MM/AAAA):")
                  if fecha_exportar == "":
                    print("No se ingreso ningun dato, favor de volver a intentarlo")
                    print("*" * 60)
                    continue
                  fecha_exportar_procesada = datetime.datetime.strptime(fecha_exportar, "%d/%m/%Y").date()
                  break
                except ValueError:
                  print("Formato de fecha no valido, favor de volver a intentarlo")
                  print("*" * 60)

              with sqlite3.connect("PrimerIntentoEvidencia3.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
                mi_cursor = conn.cursor()
                valores = {"fecha_exportar":fecha_exportar_procesada}
                mi_cursor.execute("SELECT folio_reservacion, num_sala, num_cliente, nombre_evento, DATE(fecha_reservacion), turno_reservacion FROM reservacion WHERE DATE(fecha_reservacion)=:fecha_exportar", valores)
                registros = mi_cursor.fetchall()  

                if registros:
                  wb = openpyxl.Workbook()
                  hoja1 = wb.create_sheet("Hoja")
                  hoja = wb.active
                  hoja.append(('Folio de reservacion','Numero de sala', ' Numero del cliente', 'Nombre del evento', 'Fecha', 'Turno'))

                  for reservaciones in registros:
                    hoja.append(reservaciones)
                    wb.save('Reservaciones.xlsx')
                  print("Datos exportados correctamente a un archivo de MsExcel")
                  print("*" * 60)
                else:
                  print("No se cuentan con reservaciones agendadas para ese dia, por lo tanto no hubo exportacion de datos")
                  print("*" * 60)
                  break
                break

                  

            if (opcion3.upper()=="C"):
                break


    if (opcion.upper()== "C"):
        while True:
          nombre_sala=input("Ingresa el nombre de la sala: ")
          print("*" * 60)
          if nombre_sala == "":
            print("El nombre de la sala no debe de omitirse, intentelo nuevamente")
            print("*" * 60)
          else:
            break
        while True:
          try:
            cap_sala=int(input("Ingresa la cantidad de aforo maximo de la sala: "))
            print("*" * 60)
            if cap_sala <=0:
              print("El cupo no puede omitirse y/o ser menor a 0, intentelo nuevamente ")
              print("*" * 60)
              continue
            else:
              break
          except ValueError:
            print("El numero de sala no puede omitirse ni ser de caracter string, favor de intentarlo nuevamente")
            print("*" * 60)
            continue
        try:
          with sqlite3.connect("PrimerIntentoEvidencia3.db") as conn:
              mi_cursor = conn.cursor()
              valores = {"nombre_sala":nombre_sala, "cap_sala":cap_sala}
              mi_cursor.execute("INSERT INTO sala VALUES(NULL, :nombre_sala, :cap_sala)", valores)
              print("Registro agregado exitosamente")
        finally:
            conn.close()
        try:
            with sqlite3.connect("PrimerIntentoEvidencia3.db") as conn:
              mi_cursor = conn.cursor()
              mi_cursor.execute("SELECT num_sala FROM sala WHERE nombre=:nombre_sala AND cap_sala=:cap_sala", valores)
              registros = mi_cursor.fetchall()

              for sala, in registros:
                  sala_imprimir=sala
              print(f'El numero de la sala asignado es: {sala_imprimir}')
        finally:
            conn.close()        
       

        
    if (opcion.upper()== "D"):
        while True:
          nombre_cliente=input("Ingrese su nombre completo: ")
          print("*" * 60)
          if nombre_cliente == "":
            print("El nombre del cliente no se debe de omitir, favor de intentarlo nuevamente")
            print("*" * 60)
          else:
            break
        try:
          with sqlite3.connect("PrimerIntentoEvidencia3.db") as conn:
              mi_cursor = conn.cursor()
              valores = {"nombre":nombre_cliente}
              mi_cursor.execute("INSERT INTO cliente VALUES(NULL, :nombre)", valores)
              print("Registro agregado exitosamente")
        finally:
            conn.close()
        try:
            with sqlite3.connect("PrimerIntentoEvidencia3.db") as conn:
              mi_cursor = conn.cursor()
              mi_cursor.execute("SELECT num_cliente FROM cliente WHERE nombre=:nombre", valores)
              registros = mi_cursor.fetchall()

              for cliente, in registros:
                cliente_imprimir=cliente
              print(f'Su numero de cliente asignado es: {cliente_imprimir}')
        finally:
            conn.close()


    if (opcion.upper()== "E"):
      print("¡Que tenga un bonito dia!")
      break
