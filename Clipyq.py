#!/usr/bin/env python3
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QAbstractItemView, QApplication
import pathlib, glob, os, subprocess
from pathlib import Path

numero_ediciones = 0
diccionario_ediciones={} #Mejor diccionario para poder eliminar todas las ediciones/argumentos con la opción del botón.
carpeta_destino = ""

def realizar_conversion():
    global resultado
    resultado = ""
    lista_conversiones = []
    for clave, valor in diccionario_ediciones.items():
        if clave != "formato":
            lista_conversiones.extend(valor) #extend() porque se añadirán más de uno.
    print("A realizar:", lista_conversiones)

    if listWidgetEntrada.count() > 0:
        barraProgreso.show()
        barraProgreso.setValue(0)
        lista_archivos = []
        porcentages = 100 / listWidgetEntrada.count()
      

        #Bucle para añadir los elementos del widget de la lista en una lista de Python.
        for archivo in range(listWidgetEntrada.count()):
            item = listWidgetEntrada.item(archivo)
            lista_archivos.append(item.text())

        recuento = 0
        for archivo in lista_archivos:        
            extension_archivo = pathlib.Path(archivo).suffix
            nombre_archivo = pathlib.Path(archivo).name
            nombre_archivo_sin_extension = nombre_archivo.replace(extension_archivo, "")
            ruta_completa_archivo = str(pathlib.Path(archivo))
            global carpeta_destino
            global misma_carpeta
            #misma_carpeta = False
            if carpeta_destino == "":
                carpeta_destino = ruta_completa_archivo.replace(nombre_archivo, "")
                misma_carpeta = True

            if "formato" in diccionario_ediciones:
                if diccionario_ediciones["formato"] == extension_archivo and misma_carpeta == True:
                    try:
                        proceso = subprocess.Popen(["magick", archivo, *lista_conversiones, carpeta_destino+"modificado-"+nombre_archivo_sin_extension+diccionario_ediciones["formato"]])
                    except FileNotFoundError:
                        proceso = subprocess.Popen(["convert", archivo, *lista_conversiones, carpeta_destino+"modificado-"+nombre_archivo_sin_extension+diccionario_ediciones["formato"]])
                else:
                    try:
                        proceso = subprocess.Popen(["magick", archivo, *lista_conversiones, carpeta_destino+nombre_archivo_sin_extension+diccionario_ediciones["formato"]])
                    except FileNotFoundError:
                        proceso = subprocess.Popen(["convert", archivo, *lista_conversiones, carpeta_destino+nombre_archivo_sin_extension+diccionario_ediciones["formato"]])
                 
            else:
                if misma_carpeta == True:
                    try:
                        proceso = subprocess.Popen(["magick", archivo, *lista_conversiones, carpeta_destino+"modificado-"+nombre_archivo])
                    except FileNotFoundError:
                        proceso = subprocess.Popen(["convert", archivo, *lista_conversiones, carpeta_destino+"modificado-"+nombre_archivo])
                else:
                    try:
                        proceso = subprocess.Popen(["magick", archivo, *lista_conversiones, carpeta_destino+nombre_archivo])
                    except FileNotFoundError:
                        proceso = subprocess.Popen(["convert", archivo, *lista_conversiones, carpeta_destino+nombre_archivo])
            proceso.wait()
            if proceso.returncode == 1:
                resultado = "fallo"
            elif proceso.returncode == 0:
                resultado = "exito"
            

            recuento +=1
            progreso = porcentages * recuento
            print(progreso)
            barraProgreso.setValue(int(progreso))
            QApplication.processEvents() #Se fuerza la ejecución de todos los eventos y se puede refrescar la barra de progreso en tiempo real.
        #El siguiente if/else lo tenía detrás del que hay fuera de este bloque. Puesto aquí para evitar que saque el mensaje de éxito si no ha hecho nada.
        if resultado == "fallo":
            mensaje_informacion = QMessageBox()
            mensaje_informacion.setIcon(QMessageBox.Warning)
            mensaje_informacion.setWindowTitle("Conversión")
            mensaje_informacion.setText('<b>Ha habido un error</b>')
            mensaje_informacion.setInformativeText("<p style=\"margin-right:25px\">Ha fallado la conversión en al menos uno de los archivos de la lista. Las conversiones que se han realizado con éxito están guardadas en la ruta especificada.")
            mensaje_informacion.setDetailedText("Puede que haya habido un error en la conversión de una imagen, pero también que intentara convertir un archivo no compatible. Esto es así por diseño, porque se intentará trabajar con cualquier formato de imagen.")
            mensaje_informacion.exec_()
        elif resultado == "exito":
            mensaje_informacion = QMessageBox()
            mensaje_informacion.setIcon(QMessageBox.Information)
            mensaje_informacion.setWindowTitle("Conversión")
            mensaje_informacion.setText('<b>¡Finalizado con éxito!</b>')
            mensaje_informacion.setInformativeText("<p style=\"margin-right:25px\">Todas las conversiones se han realizado con éxito. Las imágenes se han guardado en la ruta especificada.")
            mensaje_informacion.exec_()
        else:
            print("Ha pasado algo")
            
    else:
        mensaje_informacion = QMessageBox()
        mensaje_informacion.setIcon(QMessageBox.Warning)
        mensaje_informacion.setWindowTitle("Conversión")
        mensaje_informacion.setText('<b>Sin imágenes</b>')
        mensaje_informacion.setInformativeText("<p style=\"margin-right:25px\">La lista de imágenes está vacía. Elige al menos una imagen para poder continuar.")
        mensaje_informacion.exec_()
    


class Ui_MainWindow(object):

    def ventana_formato_compresion(self):
        self.formato_compresion = QtWidgets.QMainWindow()
        self.ui = Ui_FormatoCompresion()
        self.ui.setupUi(self.formato_compresion)
        self.formato_compresion.show()
    
    def ventana_redimensionar(self):
        self.redimensionar = QtWidgets.QMainWindow()
        self.ui = Ui_Redimensionar()
        self.ui.setupUi(self.redimensionar)
        self.redimensionar.show()

    def ventana_contraste(self):
        self.contraste = QtWidgets.QMainWindow()
        self.ui = Ui_Contraste()
        self.ui.setupUi(self.contraste)
        self.contraste.show()

    def ventana_rotar(self):
        self.rotar = QtWidgets.QMainWindow()
        self.ui = Ui_Rotar()
        self.ui.setupUi(self.rotar)
        self.rotar.show()
    
    def ventana_recortar(self):
        self.recortar = QtWidgets.QMainWindow()
        self.ui = Ui_Recortar()
        self.ui.setupUi(self.recortar)
        self.recortar.show()

    def ventana_marca_agua(self):
        self.marcaagua =QtWidgets.QMainWindow()
        self.ui = Ui_MarcaAgua()
        self.ui.setupUi(self.marcaagua)
        self.marcaagua.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(685, 480)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/clipyq.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listaConversiones = QtWidgets.QListWidget(self.centralwidget)
        self.listaConversiones.setGeometry(QtCore.QRect(72, 98, 111, 151))
        self.listaConversiones.setObjectName("listaConversiones")
        self.listaConversiones.itemClicked.connect(self.agregar_edicion_a_cola)
        marcaAguaItemLista = QtWidgets.QListWidgetItem()
        self.listaConversiones.addItem(marcaAguaItemLista)
        recortarItemLista = QtWidgets.QListWidgetItem()
        self.listaConversiones.addItem(recortarItemLista)
        rotarItemLista = QtWidgets.QListWidgetItem()
        self.listaConversiones.addItem(rotarItemLista)
        contrasteItemLista = QtWidgets.QListWidgetItem()
        self.listaConversiones.addItem(contrasteItemLista)
        tamanhoItemLista = QtWidgets.QListWidgetItem()
        self.listaConversiones.addItem(tamanhoItemLista)
        formatoItemLista = QtWidgets.QListWidgetItem()
        self.listaConversiones.addItem(formatoItemLista)
        iniciarItemLista = QtWidgets.QListWidgetItem()
        self.listaConversiones.addItem(iniciarItemLista)
        candelarItemLista = QtWidgets.QListWidgetItem()
        self.listaConversiones.addItem(candelarItemLista)
        self.listaFormato = QtWidgets.QListWidget(self.centralwidget)
        self.listaFormato.setGeometry(QtCore.QRect(72, 98, 84, 76))
        self.listaFormato.setObjectName("listaFormato")
        self.listaFormato.itemClicked.connect(self.configurar_formato)
        formatoEdicionItemLista = QtWidgets.QListWidgetItem()
        self.listaFormato.addItem(formatoEdicionItemLista)
        formatoEliminarItemLista = QtWidgets.QListWidgetItem()
        self.listaFormato.addItem(formatoEliminarItemLista)
        formatoCandelarItemLista = QtWidgets.QListWidgetItem()
        self.listaFormato.addItem(formatoCandelarItemLista)
        self.listaTamanho = QtWidgets.QListWidget(self.centralwidget)
        self.listaTamanho.setGeometry(QtCore.QRect(72, 98, 84, 76))
        self.listaTamanho.setObjectName("listaTamanho")
        self.listaTamanho.itemClicked.connect(self.configurar_tamanho)
        tamanhoEdicionItemLista = QtWidgets.QListWidgetItem()
        self.listaTamanho.addItem(tamanhoEdicionItemLista)
        tamanhoEliminarItemLista = QtWidgets.QListWidgetItem()
        self.listaTamanho.addItem(tamanhoEliminarItemLista)
        tamanhoCancelarItemLista = QtWidgets.QListWidgetItem()
        self.listaTamanho.addItem(tamanhoCancelarItemLista)
        self.listaContraste = QtWidgets.QListWidget(self.centralwidget)
        self.listaContraste.setGeometry(QtCore.QRect(72, 98, 84, 76))
        self.listaContraste.setObjectName("listaContraste")
        self.listaContraste.itemClicked.connect(self.configurar_contraste)
        contrasteEdicionItemLista = QtWidgets.QListWidgetItem()
        self.listaContraste.addItem(contrasteEdicionItemLista)
        contrasteEliminarItemLista = QtWidgets.QListWidgetItem()
        self.listaContraste.addItem(contrasteEliminarItemLista)
        contrasteCancelarItemLista = QtWidgets.QListWidgetItem()
        self.listaContraste.addItem(contrasteCancelarItemLista)
        self.listaRotar = QtWidgets.QListWidget(self.centralwidget)
        self.listaRotar.setGeometry(QtCore.QRect(72, 98, 84, 76))
        self.listaRotar.setObjectName("listaRotar")
        self.listaRotar.itemClicked.connect(self.configurar_rotacion)
        rotarEdicionItemLista = QtWidgets.QListWidgetItem()
        self.listaRotar.addItem(rotarEdicionItemLista)
        rotarEliminarItemLista = QtWidgets.QListWidgetItem()
        self.listaRotar.addItem(rotarEliminarItemLista)
        rotarCancelarItemLista = QtWidgets.QListWidgetItem()
        self.listaRotar.addItem(rotarCancelarItemLista)
        self.listaRecortar = QtWidgets.QListWidget(self.centralwidget)
        self.listaRecortar.setGeometry(QtCore.QRect(72, 98, 84, 76))
        self.listaRecortar.setObjectName("listaRotar")
        self.listaRecortar.itemClicked.connect(self.configurar_recorte)
        recortarEdicionItemLista = QtWidgets.QListWidgetItem()
        self.listaRecortar.addItem(recortarEdicionItemLista)
        recortarEliminarItemLista = QtWidgets.QListWidgetItem()
        self.listaRecortar.addItem(recortarEliminarItemLista)
        recortarCancelarItemLista = QtWidgets.QListWidgetItem()
        self.listaRecortar.addItem(recortarCancelarItemLista)
        self.listaMarcaAgua = QtWidgets.QListWidget(self.centralwidget)
        self.listaMarcaAgua.setGeometry(QtCore.QRect(72, 98, 84, 76))
        self.listaMarcaAgua.setObjectName("listaMarcaAgua")
        self.listaMarcaAgua.itemClicked.connect(self.configurar_marca_agua)
        marcaAguaEdicionItemLista = QtWidgets.QListWidgetItem()
        self.listaMarcaAgua.addItem(marcaAguaEdicionItemLista)
        marcaAguaEliminarItemLista = QtWidgets.QListWidgetItem()
        self.listaMarcaAgua.addItem(marcaAguaEliminarItemLista)
        marcaAguaCancelarItemLista = QtWidgets.QListWidgetItem()
        self.listaMarcaAgua.addItem(marcaAguaCancelarItemLista)
        self.restablecerButton = QtWidgets.QPushButton(self.centralwidget)
        self.restablecerButton.setGeometry(QtCore.QRect(440, 223, 102, 40))
        self.restablecerButton.setObjectName("restablecerButton")
        self.restablecerButton.clicked.connect(self.restablecer)
        self.aplicarButton = QtWidgets.QPushButton(self.centralwidget)
        self.aplicarButton.setGeometry(QtCore.QRect(552, 223, 102, 40))
        self.aplicarButton.setObjectName("aplicarButton")
        self.aplicarButton.clicked.connect(realizar_conversion)
        self.carpetaButton = QtWidgets.QPushButton(self.centralwidget)
        self.carpetaButton.setGeometry(QtCore.QRect(440, 270, 102, 40))
        self.carpetaButton.setObjectName("carpetaButton")
        self.carpetaButton.clicked.connect(self.elegir_carpeta_destino)
        self.salirButton = QtWidgets.QPushButton(self.centralwidget)
        self.salirButton.setGeometry(QtCore.QRect(552, 270, 102, 40))
        self.salirButton.setObjectName("carpetaButton")
        self.salirButton.clicked.connect(lambda: app.quit())
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 165, 671, 41))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayoutProgreso = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayoutProgreso.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayoutProgreso.setObjectName("horizontalLayoutProgreso")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayoutProgreso.addItem(spacerItem)
        global barraProgreso
        barraProgreso = self.barraProgreso = QtWidgets.QProgressBar(self.horizontalLayoutWidget_2)
        self.barraProgreso.hide()
        self.barraProgreso.setObjectName("barraProgreso")
        self.horizontalLayoutProgreso.addWidget(self.barraProgreso)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayoutProgreso.addItem(spacerItem1)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 170, 671, 31))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 190, 400, 267))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridEntrada = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridEntrada.setContentsMargins(0, 0, 0, 0)
        self.gridEntrada.setObjectName("gridEntrada")
        self.labelArchivosEntrada = QtWidgets.QLabel(self.layoutWidget)
        self.labelArchivosEntrada.setEnabled(True)
        self.listaAgregarImagenes = QtWidgets.QListWidget(self.layoutWidget)
        self.listaAgregarImagenes.setGeometry(QtCore.QRect(0, 160, 185, 80))
        self.listaAgregarImagenes.setObjectName("listaAgregarImagenes")
        self.listaAgregarImagenes.itemClicked.connect(self.agregar_imagenes)
        agregarImagenSuelta = QtWidgets.QListWidgetItem()
        self.listaAgregarImagenes.addItem(agregarImagenSuelta)
        agregarImagenesCarpeta = QtWidgets.QListWidgetItem()
        self.listaAgregarImagenes.addItem(agregarImagenesCarpeta)
        cancelarAgregarImagenes = QtWidgets.QListWidgetItem()
        self.listaAgregarImagenes.addItem(cancelarAgregarImagenes)
        self.listaEliminarImagenes = QtWidgets.QListWidget(self.layoutWidget)
        self.listaEliminarImagenes.setGeometry(QtCore.QRect(170, 160, 230, 80))
        self.listaEliminarImagenes.setObjectName("listaEliminarImagenes")
        self.listaEliminarImagenes.itemClicked.connect(self.eliminar_imagenes)
        eliminarImagenSuelta = QtWidgets.QListWidgetItem()
        self.listaEliminarImagenes.addItem(eliminarImagenSuelta)
        eliminarTodasImagenes = QtWidgets.QListWidgetItem()
        self.listaEliminarImagenes.addItem(eliminarTodasImagenes)
        cancelarEliminarImagenes = QtWidgets.QListWidgetItem()
        self.listaEliminarImagenes.addItem(cancelarEliminarImagenes)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.labelArchivosEntrada.setFont(font)
        self.labelArchivosEntrada.setObjectName("labelArchivosEntrada")
        self.gridEntrada.addWidget(self.labelArchivosEntrada, 0, 0, 1, 2)
        global listWidgetEntrada
        listWidgetEntrada = self.listWidgetEntrada = QtWidgets.QListWidget(self.layoutWidget)        
        self.listWidgetEntrada.setObjectName("listWidgetEntrada")
        self.listWidgetEntrada.setSelectionMode(QAbstractItemView.ExtendedSelection) #Permitir seleccionar más de un elemento de la lista
        self.gridEntrada.addWidget(self.listWidgetEntrada, 1, 0, 1, 2)
        self.agregarImagenesButton = QtWidgets.QPushButton(self.layoutWidget)
        self.agregarImagenesButton.setObjectName("agregarImagenesButton")
        self.agregarImagenesButton.clicked.connect(lambda: self.mostrar_listas_opciones(lista="agregar imagenes"))
        self.gridEntrada.addWidget(self.agregarImagenesButton, 2, 0, 1, 1)
        self.eliminarImagenesButton = QtWidgets.QPushButton(self.layoutWidget)
        self.eliminarImagenesButton.setObjectName("eliminarImagenesButton")
        self.eliminarImagenesButton.clicked.connect(lambda: self.mostrar_listas_opciones(lista="eliminar imagenes"))
        self.gridEntrada.addWidget(self.eliminarImagenesButton, 2, 1, 1, 1)
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(30, 15, 671, 161))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayoutEdicionesGeneral = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayoutEdicionesGeneral.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayoutEdicionesGeneral.setObjectName("horizontalLayoutEdicionesGeneral")
        global horizontalLayoutEdiciones
        horizontalLayoutEdiciones = self.horizontalLayoutEdiciones = QtWidgets.QHBoxLayout()
        self.horizontalLayoutEdiciones.setObjectName("horizontalLayoutEdiciones")
        global marcaAguaButton
        marcaAguaButton = self.marcaAguaButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        self.marcaAguaButton.setMinimumSize(QtCore.QSize(0, 150))
        self.marcaAguaButton.setObjectName("marcaAguaButton")
        self.marcaAguaButton.hide()
        self.marcaAguaButton.clicked.connect(lambda: self.mostrar_listas_opciones(lista="marca de agua"))
        #self.horizontalLayoutEdiciones.addWidget(self.marcaAguaButton)
        global recortarButton
        recortarButton = self.recortarButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        self.recortarButton.setMinimumSize(QtCore.QSize(0, 150))
        self.recortarButton.setObjectName("recortarButton")
        self.recortarButton.hide()
        self.recortarButton.clicked.connect(lambda: self.mostrar_listas_opciones(lista="recortar"))
        #self.horizontalLayoutEdiciones.addWidget(self.recortarButton)
        global rotarButton
        rotarButton = self.rotarButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        self.rotarButton.setMinimumSize(QtCore.QSize(0, 150))
        self.rotarButton.setObjectName("rotarButton")
        self.rotarButton.hide()
        self.rotarButton.clicked.connect(lambda: self.mostrar_listas_opciones(lista="rotar"))
        #self.horizontalLayoutEdiciones.addWidget(self.rotarButton)
        global contrasteButton
        contrasteButton = self.contrasteButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        self.contrasteButton.setMinimumSize(QtCore.QSize(0, 150))
        self.contrasteButton.setObjectName("contrasteButton")
        self.contrasteButton.hide()
        self.contrasteButton.clicked.connect(lambda: self.mostrar_listas_opciones(lista="contraste"))
        #self.horizontalLayoutEdiciones.addWidget(self.contrasteButton)
        global tamanhoButton
        tamanhoButton = self.tamanhoButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        self.tamanhoButton.setMinimumSize(QtCore.QSize(0, 150))
        self.tamanhoButton.setObjectName("tamanhoButton")
        self.tamanhoButton.hide()
        self.tamanhoButton.clicked.connect(lambda: self.mostrar_listas_opciones(lista="tamaño"))
        #self.horizontalLayoutEdiciones.addWidget(self.tamanhoButton)
        global formatoButton
        formatoButton = self.formatoButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        self.formatoButton.setMaximumSize(QtCore.QSize(16777215, 150))
        self.formatoButton.setObjectName("formatoButton")
        self.formatoButton.hide()
        self.formatoButton.clicked.connect(lambda: self.mostrar_listas_opciones(lista="formato"))
        #self.horizontalLayoutEdiciones.addWidget(self.formatoButton)
        self.horizontalLayoutEdicionesGeneral.addLayout(self.horizontalLayoutEdiciones)
        self.agregarEdicionButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        self.agregarEdicionButton.setMaximumSize(QtCore.QSize(90, 150))
        self.agregarEdicionButton.clicked.connect(lambda: self.mostrar_listas_opciones(lista="edicion"))
        font = QtGui.QFont()
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.agregarEdicionButton.setFont(font)
        self.agregarEdicionButton.setObjectName("agregarEdicionButton")
        self.horizontalLayoutEdicionesGeneral.addWidget(self.agregarEdicionButton)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayoutEdicionesGeneral.addItem(spacerItem4)
        self.listaConversiones.raise_()
        self.listaConversiones.hide()
        self.listaFormato.raise_()
        self.listaFormato.hide()
        self.listaTamanho.raise_()
        self.listaTamanho.hide()
        self.listaContraste.raise_()
        self.listaContraste.hide()
        self.listaRotar.raise_()
        self.listaRotar.hide()
        self.listaRecortar.raise_()
        self.listaRecortar.hide()
        self.listaMarcaAgua.raise_()
        self.listaMarcaAgua.hide()
        self.listaAgregarImagenes.raise_()
        self.listaAgregarImagenes.hide()
        self.listaEliminarImagenes.raise_()
        self.listaEliminarImagenes.hide()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 690, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    def caja_informacion(self, titulo_ventana, info_corta, info_explicacion, info_detallada, icono):
        global mensaje_informacion
        mensaje_informacion = QMessageBox()
        if icono == "informacion":
            mensaje_informacion.setIcon(QMessageBox.Information)
        elif icono == "aviso":
            mensaje_informacion.setIcon(QMessageBox.Warning)
        else:
            mensaje_informacion.setIcon(QMessageBox.Critical)
        mensaje_informacion.setWindowTitle(titulo_ventana)
        mensaje_informacion.setText('<b>'+info_corta+'</b>')
        mensaje_informacion.setInformativeText(info_explicacion)
        mensaje_informacion.setDetailedText(info_detallada)
        mensaje_informacion.exec_()



    def agregar_imagenes(self):
        self.barraProgreso.hide()
        item = self.listaAgregarImagenes.currentItem().text()
        if item == "Agregar imagen individual":
            self.listaAgregarImagenes.hide()
            home_dir = str(Path.home())
            dialogo_archivo = QFileDialog()
            dialogo_archivo.setDirectory(home_dir)
            self.nombre_archivo = dialogo_archivo.getOpenFileName()
            self.listWidgetEntrada.addItem(self.nombre_archivo[0])
            self.listaAgregarImagenes.setCurrentRow(-1)
        elif item == "Agregar carpeta":
            self.listaAgregarImagenes.hide()
            home_dir = str(Path.home())
            dialogo_carpeta = QFileDialog()
            dialogo_carpeta.setDirectory(home_dir)
            nombre_carpeta = dialogo_carpeta.getExistingDirectory()
            if nombre_carpeta:
                nombres_archivos = glob.glob(os.path.join(nombre_carpeta, "*.*"))
        
                for archivo in nombres_archivos:
                    self.listWidgetEntrada.addItem(archivo)
                self.listaAgregarImagenes.setCurrentRow(-1)
            
        else:
            self.listaAgregarImagenes.hide()
            self.listaAgregarImagenes.setCurrentRow(-1)

    def eliminar_imagenes(self):
        item = self.listaEliminarImagenes.currentItem().text()
        if item == "Eliminar todas las imágenes":
            self.listWidgetEntrada.clear()
            self.listaEliminarImagenes.hide()
            self.listaEliminarImagenes.setCurrentRow(-1)
        elif item == "Eliminar imágenes seleccionadas":
            # Obtener los índices de los elementos seleccionados en el widget
            indices_seleccionados = [self.listWidgetEntrada.row(item) for item in self.listWidgetEntrada.selectedItems()]
            self.listaEliminarImagenes.setCurrentRow(-1)
            if indices_seleccionados != []:
                # Eliminar los elementos seleccionados uno por uno
                for indice in sorted(indices_seleccionados, reverse=True):
                    item = self.listWidgetEntrada.takeItem(indice)
                    del item
                self.listaEliminarImagenes.hide()
            else:
                self.listaEliminarImagenes.hide()
                self.caja_informacion("Eliminar imágenes", "Selección vacía", "No hay imagenes que eliminar de la lista.", "", icono="informacion")
        else:
            self.listaEliminarImagenes.hide()
            self.listaEliminarImagenes.setCurrentRow(-1)


    def elegir_carpeta_destino(self):
        home_dir = str(Path.home())
        dialogo_carpeta = QFileDialog()
        dialogo_carpeta.setDirectory(home_dir)
        nombre_carpeta = dialogo_carpeta.getExistingDirectory()
        print(nombre_carpeta)
        global carpeta_destino
        carpeta_destino = nombre_carpeta+"/"
        self.barraProgreso.hide()


    def restablecer(self):
        global diccionario_ediciones
        diccionario_ediciones = {}
        global numero_ediciones
        numero_ediciones = 0
        print(diccionario_ediciones)
        #self.listWidgetEntrada.clear()
        self.formatoButton.hide()
        self.horizontalLayoutEdiciones.removeWidget(self.formatoButton)
        self.tamanhoButton.hide()
        self.horizontalLayoutEdiciones.removeWidget(self.tamanhoButton)
        self.contrasteButton.hide()
        self.horizontalLayoutEdiciones.removeWidget(self.contrasteButton)
        self.rotarButton.hide()
        self.horizontalLayoutEdiciones.removeWidget(self.rotarButton)
        self.recortarButton.hide()
        self.horizontalLayoutEdiciones.removeWidget(self.recortarButton)
        self.marcaAguaButton.hide()
        self.horizontalLayoutEdiciones.removeWidget(self.marcaAguaButton)
        self.agregarEdicionButton.setText("+")
        self.barraProgreso.hide()
        self.ocultar_listas()
        
    

    #No es especialmente elegante, pero muestra los menús en su sitio
    def mostrar_listas_opciones(self, lista):
        print("Lista de", lista)
        self.barraProgreso.hide()
        posicion = None
        if lista == "edicion":
            self.listaFormato.hide()
            self.listaTamanho.hide()
            self.listaContraste.hide()
            self.listaRotar.hide()
            self.listaRecortar.hide()
            self.listaMarcaAgua.hide()
            self.listaAgregarImagenes.hide()
            self.listaEliminarImagenes.hide()
            
            if self.agregarEdicionButton.text() == "+":
                global numero_ediciones
                self.listaConversiones.show()
                if numero_ediciones == 0:
                    self.listaConversiones.setGeometry(QtCore.QRect(72, 98, 109, 197))
                elif numero_ediciones == 1:
                    self.listaConversiones.setGeometry(QtCore.QRect(162, 98, 109, 197))
                elif numero_ediciones == 2:
                    self.listaConversiones.setGeometry(QtCore.QRect(252, 98, 109, 197))
                elif numero_ediciones == 3:
                    self.listaConversiones.setGeometry(QtCore.QRect(342, 98, 109, 197))
                elif numero_ediciones == 4:
                    self.listaConversiones.setGeometry(QtCore.QRect(432, 98, 109, 197))
                elif numero_ediciones == 5:
                    self.listaConversiones.setGeometry(QtCore.QRect(522, 98, 109, 197))
                else:
                    self.listaConversiones.hide()
            else: 
                realizar_conversion()

            self.listaConversiones.setCurrentRow(-1)
        elif lista == "formato":
            self.listaTamanho.hide()
            self.listaContraste.hide()
            self.listaRotar.hide()
            self.listaRecortar.hide()
            self.listaMarcaAgua.hide()
            self.listaConversiones.hide()
            posicion = self.horizontalLayoutEdiciones.indexOf(self.formatoButton)
            print("Posición botón formato", posicion)
            if posicion == 0:
                self.listaFormato.setGeometry(QtCore.QRect(72, 98, 114, 76))
            elif posicion == 1:
                self.listaFormato.setGeometry(QtCore.QRect(162, 98, 114, 76))
            elif posicion == 2:
                self.listaFormato.setGeometry(QtCore.QRect(252, 98, 114, 76))
            elif posicion == 3:
                self.listaFormato.setGeometry(QtCore.QRect(342, 98, 114, 76))
            elif posicion == 4:
                self.listaFormato.setGeometry(QtCore.QRect(432, 98, 114, 76))
            elif posicion == 5:
                self.listaFormato.setGeometry(QtCore.QRect(522, 98, 114, 76))
            self.listaFormato.show()
        elif lista == "tamaño":
            self.listaFormato.hide()
            self.listaContraste.hide()
            self.listaRotar.hide()
            self.listaRecortar.hide()
            self.listaMarcaAgua.hide()
            self.listaConversiones.hide()
            posicion = self.horizontalLayoutEdiciones.indexOf(self.tamanhoButton)
            print("Posición botón tamaño", posicion)
            if posicion == 0:
                self.listaTamanho.setGeometry(QtCore.QRect(72, 98, 114, 76))
            elif posicion == 1:
                self.listaTamanho.setGeometry(QtCore.QRect(162, 98, 114, 76))
            elif posicion == 2:
                self.listaTamanho.setGeometry(QtCore.QRect(252, 98, 114, 76))
            elif posicion == 3:
                self.listaTamanho.setGeometry(QtCore.QRect(342, 98, 114, 76))
            elif posicion == 4:
                self.listaTamanho.setGeometry(QtCore.QRect(432, 98, 114, 76))
            elif posicion ==5:
                self.listaTamanho.setGeometry(QtCore.QRect(522, 98, 114, 76))
            self.listaTamanho.show()
        elif lista == "contraste":
            self.listaFormato.hide()
            self.listaTamanho.hide()
            self.listaRotar.hide()
            self.listaRecortar.hide()
            self.listaMarcaAgua.hide()
            self.listaConversiones.hide()
            posicion = self.horizontalLayoutEdiciones.indexOf(self.contrasteButton)
            print("Posición boton contraste", posicion)
            if posicion == 0:
                self.listaContraste.setGeometry(QtCore.QRect(72, 98, 114, 76))
            elif posicion == 1:
                self.listaContraste.setGeometry(QtCore.QRect(162, 98, 114, 76))
            elif posicion == 2:
                self.listaContraste.setGeometry(QtCore.QRect(252, 98, 114, 76))
            elif posicion == 3:
                self.listaContraste.setGeometry(QtCore.QRect(342, 98, 114, 76))
            elif posicion == 4:
                self.listaContraste.setGeometry(QtCore.QRect(432, 98, 114, 76))
            else:
                self.listaContraste.setGeometry(QtCore.QRect(522, 98, 114, 76))
            self.listaContraste.show()
        elif lista == "rotar":
            self.listaFormato.hide()
            self.listaTamanho.hide()
            self.listaContraste.hide()
            self.listaRecortar.hide()
            self.listaMarcaAgua.hide()
            self.listaConversiones.hide()
            posicion = self.horizontalLayoutEdiciones.indexOf(self.rotarButton)
            print("Posición boton rotar", posicion)
            if posicion == 0:
                self.listaRotar.setGeometry(QtCore.QRect(72, 98, 114, 76))
            elif posicion == 1:
                self.listaRotar.setGeometry(QtCore.QRect(162, 98, 114, 76))
            elif posicion == 2:
                self.listaRotar.setGeometry(QtCore.QRect(252, 98, 114, 76))
            elif posicion == 3:
                self.listaRotar.setGeometry(QtCore.QRect(342, 98, 114, 76))
            elif posicion == 4:
                self.listaRotar.setGeometry(QtCore.QRect(432, 98, 114, 76))
            else:
                self.listaRotar.setGeometry(QtCore.QRect(522, 98, 114, 76))
            self.listaRotar.show()
        elif lista == "recortar":
            self.listaFormato.hide()
            self.listaTamanho.hide()
            self.listaContraste.hide()
            self.listaRotar.hide()
            self.listaMarcaAgua.hide()
            self.listaConversiones.hide()
            posicion = self.horizontalLayoutEdiciones.indexOf(self.recortarButton)
            print("Posición boton recortar", posicion)
            if posicion == 0:
                self.listaRecortar.setGeometry(QtCore.QRect(72, 98, 114, 76))
            elif posicion == 1:
                self.listaRecortar.setGeometry(QtCore.QRect(162, 98, 114, 76))
            elif posicion == 2:
                self.listaRecortar.setGeometry(QtCore.QRect(252, 98, 114, 76))
            elif posicion == 3:
                self.listaRecortar.setGeometry(QtCore.QRect(342, 98, 114, 76))
            elif posicion == 4:
                self.listaRecortar.setGeometry(QtCore.QRect(432, 98, 114, 76))
            else:
                self.listaRecortar.setGeometry(QtCore.QRect(522, 98, 114, 76))
            self.listaRecortar.show()
        elif lista == "marca de agua":
            self.listaFormato.hide()
            self.listaTamanho.hide()
            self.listaContraste.hide()
            self.listaRotar.hide()
            self.listaRecortar.hide()
            self.listaConversiones.hide()
            posicion = self.horizontalLayoutEdiciones.indexOf(self.marcaAguaButton)
            print("Boton Marca de agua en", posicion)
            if posicion == 0:
                self.listaMarcaAgua.setGeometry(QtCore.QRect(72, 98, 114, 76))
            elif posicion == 1:
                self.listaMarcaAgua.setGeometry(QtCore.QRect(162, 98, 114, 76))
            elif posicion == 2:
                self.listaMarcaAgua.setGeometry(QtCore.QRect(252, 98, 114, 76))
            elif posicion == 3:
                self.listaMarcaAgua.setGeometry(QtCore.QRect(342, 98, 114, 76))
            elif posicion == 4:
                self.listaMarcaAgua.setGeometry(QtCore.QRect(432, 98, 114, 76))
            else:
                self.listaMarcaAgua.setGeometry(QtCore.QRect(522, 98, 114, 76))
            self.listaMarcaAgua.show()
        elif lista == "agregar imagenes":
            self.listaAgregarImagenes.show()
            self.listaConversiones.hide()
            self.listaEliminarImagenes.hide()
            self.listaFormato.hide()
            self.listaTamanho.hide()
            self.listaContraste.hide()
            self.listaRecortar.hide()
            self.listaRotar.hide()
            self.listaMarcaAgua.hide()
        elif lista == "eliminar imagenes":
            self.listaEliminarImagenes.show()
            self.listaConversiones.hide()
            self.listaAgregarImagenes.hide()
            self.listaFormato.hide()
            self.listaTamanho.hide()
            self.listaContraste.hide()
            self.listaRecortar.hide()
            self.listaRotar.hide()
            self.listaMarcaAgua.hide()


    def ocultar_listas(self):
        self.listaRecortar.hide()
        self.listaFormato.hide()
        self.listaTamanho.hide()
        self.listaContraste.hide()
        self.listaRotar.hide()
        self.listaMarcaAgua.hide()
        self.listaConversiones.hide()
        self.listaAgregarImagenes.hide()
        self.listaEliminarImagenes.hide()

    def agregar_edicion_a_cola(self):
        self.barraProgreso.hide()
        global numero_ediciones
        item = self.listaConversiones.currentItem().text()
        if item == "Formato":
            if "formato" not in diccionario_ediciones:
                self.ventana_formato_compresion()
                self.horizontalLayoutEdiciones.addWidget(self.formatoButton)
                self.formatoButton.show()
                numero_ediciones += 1
                diccionario_ediciones["formato"] = []
                if numero_ediciones == 6:
                    self.agregarEdicionButton.setText("✔")
                    self.agregarEdicionButton.setStatusTip("Iniciar conversión")
                self.listaConversiones.hide()
            else: 
                self.listaConversiones.hide()
                self.caja_informacion("Ediciones", "Ya en lista", "<p style=\"margin-right:30px;\">Esta edición ya está en la lista y no se puede volver a añadir.", "", icono="aviso")
        elif item == "Tamaño":
            if "tamaño" not in diccionario_ediciones:
                self.ventana_redimensionar()
                self.horizontalLayoutEdiciones.addWidget(self.tamanhoButton)
                self.tamanhoButton.show()
                numero_ediciones += 1
                diccionario_ediciones["tamaño"] = []
                if numero_ediciones == 6:
                    self.agregarEdicionButton.setText("✔")
                    self.agregarEdicionButton.setStatusTip("Iniciar conversión")
                self.listaConversiones.hide()
            else: 
                self.listaConversiones.hide()
                self.caja_informacion("Ediciones", "Ya en lista", "<p style=\"margin-right:30px;\">Esta edición ya está en la lista y no se puede volver a añadir.", "", icono="aviso")
        elif item == "Contraste":
            if "contraste" not in diccionario_ediciones:
                self.ventana_contraste()
                self.horizontalLayoutEdiciones.addWidget(self.contrasteButton)
                self.contrasteButton.show()
                numero_ediciones += 1
                diccionario_ediciones["contraste"] = []
                if numero_ediciones == 6:
                    self.agregarEdicionButton.setText("✔")
                    self.agregarEdicionButton.setStatusTip("Iniciar conversión")
                self.listaConversiones.hide()
            else: 
                self.listaConversiones.hide()
                self.caja_informacion("Ediciones", "Ya en lista", "<p style=\"margin-right:30px;\">Esta edición ya está en la lista y no se puede volver a añadir.", "", icono="aviso")
        elif item == "Rotar":
            if "rotar" not in diccionario_ediciones:
                self.ventana_rotar()
                self.horizontalLayoutEdiciones.addWidget(self.rotarButton)
                self.rotarButton.show()
                numero_ediciones += 1
                diccionario_ediciones["rotar"] = []
                if numero_ediciones == 6:
                    self.agregarEdicionButton.setText("✔")
                    self.agregarEdicionButton.setStatusTip("Iniciar conversión")
                self.listaConversiones.hide()
            else: 
                self.listaConversiones.hide()
                self.caja_informacion("Ediciones", "Ya en lista", "<p style=\"margin-right:30px;\">Esta edición ya está en la lista y no se puede volver a añadir.", "", icono="aviso")
        elif item == "Recortar":
            if "recortar" not in diccionario_ediciones:
                self.ventana_recortar()
                self.horizontalLayoutEdiciones.addWidget(self.recortarButton)
                self.recortarButton.show()
                numero_ediciones += 1
                diccionario_ediciones["recortar"] = []
                if numero_ediciones == 6:
                    self.agregarEdicionButton.setText("✔")
                    self.agregarEdicionButton.setStatusTip("Iniciar conversión")
                self.listaConversiones.hide()
            else: 
                self.listaConversiones.hide()
                self.caja_informacion("Ediciones", "Ya en lista", "<p style=\"margin-right:30px;\">Esta edición ya está en la lista y no se puede volver a añadir.", "", icono="aviso")
        elif item == "Marca de agua":
            if "marca de agua" not in diccionario_ediciones:
                self.ventana_marca_agua()
                self.horizontalLayoutEdiciones.addWidget(self.marcaAguaButton)
                self.marcaAguaButton.show()
                numero_ediciones += 1
                diccionario_ediciones["marca de agua"] = []
                if numero_ediciones == 6:
                    self.agregarEdicionButton.setText("✔")
                    self.agregarEdicionButton.setStatusTip("Iniciar conversión")
                self.listaConversiones.hide()
            else: 
                self.listaConversiones.hide()
                self.caja_informacion("Ediciones", "Ya en lista", "<p style=\"margin-right:30px;\">Esta edición ya está en la lista y no se puede volver a añadir.", "", icono="aviso")
        elif item == "Cancelar ✗✗✗":
            self.listaConversiones.hide()
        else:
            if numero_ediciones > 0:
                self.agregarEdicionButton.setText("✔")
                self.agregarEdicionButton.setStatusTip("Iniciar conversión")
                self.listaConversiones.hide()
            else: 
                self.listaConversiones.hide()
                self.caja_informacion("Ediciones", "Nada que convertir", "<p style=\"margin-right:30px;\">Añade algún tipo de conversión antes de aceptar y continuar.", "", icono="aviso")

        #self.agregarEdicionButton.show()

    def configurar_formato(self):
        self.barraProgreso.hide()
        global numero_ediciones
        itemFormato = self.listaFormato.currentItem().text()

        if itemFormato == "Eliminar edición":
            self.formatoButton.setText("Formato")
            self.formatoButton.hide()
            self.horizontalLayoutEdiciones.removeWidget(self.formatoButton)
            self.listaFormato.setCurrentRow(-1) #Elige una fila de fuera y se des-selecciona
            self.listaFormato.hide()
            del diccionario_ediciones["formato"]
            horizontalLayoutEdiciones.invalidate()
            try:
                del diccionario_ediciones["compresion"]
            except KeyError:
                """No había compresión"""
            numero_ediciones -= 1
            if numero_ediciones < 6:
                self.agregarEdicionButton.setText('+')
                self.agregarEdicionButton.setStatusTip("Añadir retoque")
        elif itemFormato == "Cancelar ✗":
            self.listaFormato.hide()
        else:
            self.listaFormato.hide()
            self.ventana_formato_compresion()
        
        print(diccionario_ediciones)

    def configurar_tamanho(self):
        self.barraProgreso.hide()
        global numero_ediciones
        itemTamanho = self.listaTamanho.currentItem().text()

        if itemTamanho == "Eliminar edición":
            self.tamanhoButton.setText("Tamaño")
            self.tamanhoButton.hide()
            self.horizontalLayoutEdiciones.removeWidget(self.tamanhoButton)
            self.listaTamanho.setCurrentRow(-1) #Elige una fila de fuera y se des-selecciona
            self.listaTamanho.hide()
            del diccionario_ediciones["tamaño"]
            horizontalLayoutEdiciones.invalidate()
            numero_ediciones -= 1
            if numero_ediciones < 6:
                self.agregarEdicionButton.setText('+')
                self.agregarEdicionButton.setStatusTip("Añadir retoque")
        elif itemTamanho == "Cancelar ✗":
            self.listaTamanho.hide()
        else:
            self.listaTamanho.hide()
            self.ventana_redimensionar()
        
        print(diccionario_ediciones)

    def configurar_contraste(self):
        self.barraProgreso.hide()
        global numero_ediciones
        itemContraste = self.listaContraste.currentItem().text()

        if itemContraste == "Eliminar edición":
            self.contrasteButton.setText("Contraste")
            self.contrasteButton.hide()
            self.horizontalLayoutEdiciones.removeWidget(self.contrasteButton)
            self.listaContraste.setCurrentRow(-1) #Elige una fila de fuera y se des-selecciona
            self.listaContraste.hide()
            del diccionario_ediciones["contraste"]
            horizontalLayoutEdiciones.invalidate()
            numero_ediciones -= 1
            if numero_ediciones < 6:
                self.agregarEdicionButton.setText('+')
                self.agregarEdicionButton.setStatusTip("Añadir retoque")
        elif itemContraste == "Cancelar ✗":
            self.listaContraste.hide()
        else:
            self.listaContraste.hide()
            self.ventana_contraste()
        
        print(diccionario_ediciones)

    def configurar_rotacion(self):
        self.barraProgreso.hide()
        global numero_ediciones
        itemRotacion = self.listaRotar.currentItem().text()

        if itemRotacion == "Eliminar edición":
            self.rotarButton.setText("Rotación")
            self.rotarButton.hide()
            self.horizontalLayoutEdiciones.removeWidget(self.rotarButton)
            self.listaRotar.setCurrentRow(-1) #Elige una fila de fuera y se des-selecciona
            self.listaRotar.hide()
            del diccionario_ediciones["rotar"]
            horizontalLayoutEdiciones.invalidate()
            numero_ediciones -= 1
            if numero_ediciones < 6:
                self.agregarEdicionButton.setText('+')
                self.agregarEdicionButton.setStatusTip("Añadir retoque")
        elif itemRotacion == "Cancelar ✗":
            self.listaRotar.hide()
        else:
            self.listaRotar.hide()
            print("Vas a editar la rotación")
            self.ventana_rotar()

        print(diccionario_ediciones)

    def configurar_recorte(self):
        self.barraProgreso.hide()
        global numero_ediciones
        itemRecorte = self.listaRecortar.currentItem().text()

        if itemRecorte == "Eliminar edición":
            self.recortarButton.setText("Recortar")
            self.recortarButton.hide()
            self.horizontalLayoutEdiciones.removeWidget(self.recortarButton)
            self.listaRecortar.setCurrentRow(-1) #Elige una fila de fuera y se des-selecciona
            self.listaRecortar.hide()
            del diccionario_ediciones["recortar"]
            horizontalLayoutEdiciones.invalidate()
            numero_ediciones -= 1
            if numero_ediciones < 6:
                self.agregarEdicionButton.setText('+')
                self.agregarEdicionButton.setStatusTip("Añadir retoque")
        elif itemRecorte == "Cancelar ✗":
            self.listaRecortar.hide()
        else:
            self.listaRecortar.hide()
            self.ventana_recortar()
        
        print(diccionario_ediciones)

    def configurar_marca_agua(self):
        self.barraProgreso.hide()
        global numero_ediciones
        itemMarcaAgua = self.listaMarcaAgua.currentItem().text()

        if itemMarcaAgua == "Eliminar edición":
            self.marcaAguaButton.setText("Marca\nde agua")
            self.marcaAguaButton.hide()
            self.horizontalLayoutEdiciones.removeWidget(self.marcaAguaButton)
            self.listaMarcaAgua.setCurrentRow(-1) #Elige una fila de fuera y se des-selecciona
            self.listaMarcaAgua.hide()
            del diccionario_ediciones["marca de agua"]
            horizontalLayoutEdiciones.invalidate()
            numero_ediciones -= 1
            if numero_ediciones < 6:
                self.agregarEdicionButton.setText('+')
                self.agregarEdicionButton.setStatusTip("Añadir retoque")
        elif itemMarcaAgua == "Cancelar ✗":
            self.listaMarcaAgua.hide()
        else:
            self.listaMarcaAgua.hide()
            self.ventana_marca_agua()

        print(diccionario_ediciones)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Clipyq"))
        __sortingEnabled = self.listaConversiones.isSortingEnabled()
        self.listaConversiones.setSortingEnabled(False)
        item1 = self.listaConversiones.item(0)
        item1.setText(_translate("MainWindow", "Aceptar ✔✔✔"))
        item2 = self.listaConversiones.item(1)
        item2.setText(_translate("MainWindow", "Formato"))
        item3 = self.listaConversiones.item(2)
        item3.setText(_translate("MainWindow", "Tamaño"))
        item4 = self.listaConversiones.item(3)
        item4.setText(_translate("MainWindow", "Contraste"))
        item5 = self.listaConversiones.item(4)
        item5.setText(_translate("MainWindow", "Rotar"))
        item6 = self.listaConversiones.item(5)
        item6.setText(_translate("MainWindow", "Recortar"))
        item7 = self.listaConversiones.item(6)
        item7.setText(_translate("MainWindow", "Marca de agua"))
        item8 = self.listaConversiones.item(7)
        item8.setText(_translate("MainWindow", "Cancelar ✗✗✗"))
        self.listaConversiones.setSortingEnabled(__sortingEnabled)
        item9 = self.listaFormato.item(0)
        item9.setText(_translate("MainWindow", "Editar"))
        item10 = self.listaFormato.item(1)
        item10.setText(_translate("MainWindow", "Eliminar edición"))
        item11 = self.listaFormato.item(2)
        item11.setText(_translate("MainWindow", "Cancelar ✗"))
        item12 = self.listaTamanho.item(0)
        item12.setText(_translate("MainWindow", "Editar"))
        item13 = self.listaTamanho.item(1)
        item13.setText(_translate("MainWindow", "Eliminar edición"))
        item14 = self.listaTamanho.item(2)
        item14.setText(_translate("MainWindow", "Cancelar ✗"))
        item15 = self.listaContraste.item(0)
        item15.setText(_translate("MainWindow", "Editar"))
        item16 = self.listaContraste.item(1)
        item16.setText(_translate("MainWindow", "Eliminar edición"))
        item17 = self.listaContraste.item(2)
        item17.setText(_translate("MainWindow", "Cancelar ✗"))
        item18 = self.listaRotar.item(0)
        item18.setText(_translate("MainWindow", "Editar"))
        item19 = self.listaRotar.item(1)
        item19.setText(_translate("MainWindow", "Eliminar edición"))
        item20 = self.listaRotar.item(2)
        item20.setText(_translate("MainWindow", "Cancelar ✗"))
        item21 = self.listaRecortar.item(0)
        item21.setText(_translate("MainWindow", "Editar"))
        item22 = self.listaRecortar.item(1)
        item22.setText(_translate("MainWindow", "Eliminar edición"))
        item23 = self.listaRecortar.item(2)
        item23.setText(_translate("MainWindow", "Cancelar ✗"))
        item24 = self.listaMarcaAgua.item(0)
        item24.setText(_translate("MainWindow", "Editar"))
        item25 = self.listaMarcaAgua.item(1)
        item25.setText(_translate("MainWindow", "Eliminar edición"))
        item26 = self.listaMarcaAgua.item(2)
        item26.setText(_translate("MainWindow", "Cancelar ✗"))
        item27 = self.listaAgregarImagenes.item(0)
        item27.setText(_translate("MainWindow", "Agregar carpeta"))
        item28 = self.listaAgregarImagenes.item(1)
        item28.setText(_translate("MainWindow", "Agregar imagen individual"))
        item29 = self.listaAgregarImagenes.item(2)
        item29.setText(_translate("MainWindow", "Cancelar ✗"))
        item30 = self.listaEliminarImagenes.item(0)
        item30.setText(_translate("MainWindow", "Eliminar todas las imágenes"))
        item31 = self.listaEliminarImagenes.item(1)
        item31.setText(_translate("MainWindow", "Eliminar imágenes seleccionadas"))
        item32 = self.listaEliminarImagenes.item(2)
        item32.setText(_translate("MainWindow", "Cancelar ✗"))
        self.restablecerButton.setText(_translate("MainWindow", "Reiniciar"))
        self.restablecerButton.setStatusTip(_translate("MainWindow", "Poner a cero todas las conversiones"))
        self.aplicarButton.setText(_translate("MainWindow", "APLICAR"))
        self.aplicarButton.setStatusTip(_translate("MainWindow", "Iniciar proceso de conversión"))
        self.carpetaButton.setText(_translate("MainWindow", "Carpeta\ndestino"))
        self.carpetaButton.setStatusTip(_translate("MainWindow", "Elegir carpeta de destino diferente"))
        self.salirButton.setText(_translate("MainWindow", "Salir"))
        self.salirButton.setStatusTip(_translate("MainWindow", "Salir de la app"))
        self.labelArchivosEntrada.setText(_translate("MainWindow", " Archivos de entrada:"))
        self.agregarImagenesButton.setText(_translate("MainWindow", "Añadir imágenes"))
        self.agregarImagenesButton.setStatusTip(_translate("MainWindow", "Agregar imágenes a la lista de conversión"))
        self.eliminarImagenesButton.setText(_translate("MainWindow", "Eliminar imágenes"))
        self.eliminarImagenesButton.setStatusTip(_translate("MainWindow", "Eliminar imágenes de la lista de conversión"))
        self.marcaAguaButton.setText(_translate("MainWindow", "Marca\nde agua"))
        self.recortarButton.setText(_translate("MainWindow", "Recortar"))
        self.rotarButton.setText(_translate("MainWindow", "Rotar"))
        self.contrasteButton.setText(_translate("MainWindow", "Contraste"))
        self.tamanhoButton.setText(_translate("MainWindow", "Tamaño"))
        self.formatoButton.setText(_translate("MainWindow", "Formato"))
        self.formatoButton.setStatusTip(_translate("MainWindow", "Añadir/Editar/Eliminar formato de compresión"))
        self.agregarEdicionButton.setStatusTip(_translate("MainWindow", "Añadir retoque"))
        self.agregarEdicionButton.setText(_translate("MainWindow", "+"))

class Ui_FormatoCompresion(Ui_MainWindow, object):
    def setupUi(self, FormatoCompresion):
        FormatoCompresion.setObjectName("FormatoCompresion")
        FormatoCompresion.setFixedSize(331, 199)
        self.centralwidget = QtWidgets.QWidget(FormatoCompresion)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 20, 273, 182))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayoutFormato = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayoutFormato.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutFormato.setObjectName("gridLayoutFormato")
        self.spinBoxPorcentageFormato = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBoxPorcentageFormato.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBoxPorcentageFormato.setPrefix("")
        self.spinBoxPorcentageFormato.setMinimum(1)
        self.spinBoxPorcentageFormato.setMaximum(100)
        self.spinBoxPorcentageFormato.setProperty("value", 90)
        self.spinBoxPorcentageFormato.setObjectName("spinBoxPorcentageFormato")
        self.spinBoxPorcentageFormato.setEnabled(False)
        self.spinBoxPorcentageFormato.valueChanged.connect(self.actualizar_valor_formato)
        self.spinBoxPorcentageFormato.setSuffix("%")
        self.gridLayoutFormato.addWidget(self.spinBoxPorcentageFormato, 3, 1, 1, 1)
        self.horizontalSliderFormato = QtWidgets.QSlider(self.gridLayoutWidget)
        self.horizontalSliderFormato.setProperty("value", 90)
        self.horizontalSliderFormato.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderFormato.setObjectName("horizontalSliderFormato")
        self.horizontalSliderFormato.setEnabled(False)
        self.horizontalSliderFormato.valueChanged.connect(self.actualizar_valor_formato)
        self.gridLayoutFormato.addWidget(self.horizontalSliderFormato, 3, 0, 1, 1)
        self.horizontalLayoutBotonesFormato = QtWidgets.QHBoxLayout()
        self.horizontalLayoutBotonesFormato.setObjectName("horizontalLayoutBotonesFormato")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayoutBotonesFormato.addItem(spacerItem)
        self.buttonBoxFormato = QtWidgets.QDialogButtonBox(self.gridLayoutWidget)
        self.buttonBoxFormato.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBoxFormato.accepted.connect(self.aceptar_formato)
        self.buttonBoxFormato.rejected.connect(self.cancelar_formato)
        self.buttonBoxFormato.setObjectName("buttonBoxFormato")
        self.horizontalLayoutBotonesFormato.addWidget(self.buttonBoxFormato)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayoutBotonesFormato.addItem(spacerItem1)
        self.gridLayoutFormato.addLayout(self.horizontalLayoutBotonesFormato, 4, 0, 1, 3)
        self.comboBoxFormato = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBoxFormato.currentIndexChanged.connect(self.tipo_compresion)
        self.comboBoxFormato.setObjectName("comboBoxFormato")
        self.comboBoxFormato.addItem("")
        self.comboBoxFormato.addItem("")
        self.comboBoxFormato.addItem("")
        self.comboBoxFormato.addItem("")
        self.comboBoxFormato.addItem("")
        self.comboBoxFormato.addItem("")
        self.comboBoxFormato.addItem("")
        self.gridLayoutFormato.addWidget(self.comboBoxFormato, 0, 0, 1, 3)
        self.horizontalLayoutSinPerdida = QtWidgets.QHBoxLayout()
        self.horizontalLayoutSinPerdida.setObjectName("horizontalLayoutSinPerdida")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayoutSinPerdida.addItem(spacerItem2)
        self.checkBoxSinPerdida = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.checkBoxSinPerdida.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBoxSinPerdida.setAutoFillBackground(False)
        self.checkBoxSinPerdida.setChecked(True)
        self.checkBoxSinPerdida.setToolTip("Sólo para PNG, JPEG y GIF")
        self.checkBoxSinPerdida.setObjectName("checkBoxSinPerdida")
        self.checkBoxSinPerdida.stateChanged.connect(self.compresion)
        self.horizontalLayoutSinPerdida.addWidget(self.checkBoxSinPerdida)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayoutSinPerdida.addItem(spacerItem3)
        self.gridLayoutFormato.addLayout(self.horizontalLayoutSinPerdida, 1, 0, 1, 3)
        FormatoCompresion.setCentralWidget(self.centralwidget)

        self.retranslateUi(FormatoCompresion)
        QtCore.QMetaObject.connectSlotsByName(FormatoCompresion)
        self.FormatoCompresion = FormatoCompresion
    
    def aceptar_formato(self):
        self.FormatoCompresion.close()
        abre_parentesis = self.comboBoxFormato.currentText().rfind("(") + 1
        cierra_parentesis = self.comboBoxFormato.currentText().rfind(")")
        formato_conversion = self.comboBoxFormato.currentText()[abre_parentesis:cierra_parentesis]
        if self.checkBoxSinPerdida.isChecked():
            diccionario_ediciones["formato"]=formato_conversion
        else:
            diccionario_ediciones["formato"]=formato_conversion
            if formato_conversion == ".gif":
                diccionario_ediciones["compresion"] = "-fuzz", str(self.spinBoxPorcentageFormato.value()) + "%" , "-layers", "Optimize"
            elif formato_conversion == ".jpeg":
                diccionario_ediciones["compresion"] = "-quality", str(self.spinBoxPorcentageFormato.value())
            elif formato_conversion == ".png":
                diccionario_ediciones["compresion"] = "-depth", str(self.spinBoxPorcentageFormato.value())
            else:
                mensaje_informacion = QMessageBox()
                mensaje_informacion.setIcon(QMessageBox.Information)
                mensaje_informacion.setWindowTitle("Compresión")
                mensaje_informacion.setText('<b>Este formato no se comprimirá</b>')
                mensaje_informacion.setInformativeText("<p style=\"margin-right:25px\">Los formatos compatibles con la función de compresión son GIF, PNG o JPEG.")
                mensaje_informacion.exec_()
        try:
            if self.comboBoxFormato.currentText() == "Joint Photographic Experts Group (.jpeg)": 
                texto_formato = "Formato:\n"+ str(diccionario_ediciones["formato"]) + "\n" + str(diccionario_ediciones["compresion"][1] + "%")
            elif self.comboBoxFormato.currentText() == "Graphics Interchange Format (.gif)":
                texto_formato = "Formato:\n"+ str(diccionario_ediciones["formato"]) + "\n" + str(diccionario_ediciones["compresion"][1])
            elif self.comboBoxFormato.currentText() == "Portable Network Graphics (.png)":
                texto_formato = "Formato:\n"+ str(diccionario_ediciones["formato"]) + "\n" + str(diccionario_ediciones["compresion"][1] + "bits")
            else: 
                texto_formato = "Formato:\n"+ str(diccionario_ediciones["formato"])
            formatoButton.setText(texto_formato)
        except KeyError:
            formatoButton.setText("Formato:\n"+diccionario_ediciones["formato"])
        print(diccionario_ediciones)

    def cancelar_formato(self):
        self.FormatoCompresion.close()
        if diccionario_ediciones["formato"] == []:
            del diccionario_ediciones["formato"]
            formatoButton.hide()
            horizontalLayoutEdiciones.removeWidget(formatoButton)
            horizontalLayoutEdiciones.invalidate()
            global numero_ediciones
            numero_ediciones -= 1
        print(diccionario_ediciones)
    
    def actualizar_valor_formato(self, valor):
        # Si la señal proviene del QSpinBox, actualizar el valor del QSlider
        if self.spinBoxPorcentageFormato.valueChanged:
            self.horizontalSliderFormato.setValue(valor)
        # Si la señal proviene del QSlider, actualizar el valor del QSpinBox
        if self.horizontalSliderFormato.valueChanged:
            self.spinBoxPorcentageFormato.setValue(valor)
    
    def compresion(self):
        if self.checkBoxSinPerdida.isChecked():
            self.horizontalSliderFormato.setEnabled(False)
            self.spinBoxPorcentageFormato.setEnabled(False)
        else:
            if self.comboBoxFormato.currentText() != "WebP (.webp)" and self.comboBoxFormato.currentText() != "Bits Maps Protocole (.bmp)" and self.comboBoxFormato.currentText() != "Tagged Image File Format (.tiff)" and self.comboBoxFormato.currentText() != "ICO (.ico)":
                self.horizontalSliderFormato.setEnabled(True)
                self.spinBoxPorcentageFormato.setEnabled(True)
        
    def tipo_compresion(self):
        if self.comboBoxFormato.currentText() == "Joint Photographic Experts Group (.jpeg)" or self.comboBoxFormato.currentText() == "Graphics Interchange Format (.gif)" :
            self.spinBoxPorcentageFormato.setSuffix("%")
            self.spinBoxPorcentageFormato.setMinimum(1)
            self.spinBoxPorcentageFormato.setMaximum(100)
            self.horizontalSliderFormato.setMaximum(100)
            self.spinBoxPorcentageFormato.setValue(90)
            self.horizontalSliderFormato.setValue(90)
        elif self.comboBoxFormato.currentText() == "Portable Network Graphics (.png)":
            self.spinBoxPorcentageFormato.setSuffix("bit")
            self.spinBoxPorcentageFormato.setMinimum(1)
            self.spinBoxPorcentageFormato.setMaximum(16)
            self.horizontalSliderFormato.setMaximum(16)
            self.spinBoxPorcentageFormato.setValue(12)
            self.horizontalSliderFormato.setValue(12)
        else:
            self.spinBoxPorcentageFormato.setSuffix("%")
            self.spinBoxPorcentageFormato.setEnabled(False)
            self.horizontalSliderFormato.setEnabled(False)
            self.spinBoxPorcentageFormato.setMinimum(1)
            self.spinBoxPorcentageFormato.setMaximum(100)
            



    def retranslateUi(self, FormatoCompresion):
        _translate = QtCore.QCoreApplication.translate
        FormatoCompresion.setWindowTitle(_translate("FormatoCompresion", "Formato de Compresión"))
        self.comboBoxFormato.setItemText(0, _translate("FormatoCompresion", "Joint Photographic Experts Group (.jpeg)"))
        self.comboBoxFormato.setItemText(1, _translate("FormatoCompresion", "Portable Network Graphics (.png)"))
        self.comboBoxFormato.setItemText(2, _translate("FormatoCompresion", "WebP (.webp)"))
        self.comboBoxFormato.setItemText(3, _translate("FormatoCompresion", "Bits Maps Protocole (.bmp)"))
        self.comboBoxFormato.setItemText(4, _translate("FormatoCompresion", "Graphics Interchange Format (.gif)"))
        self.comboBoxFormato.setItemText(5, _translate("FormatoCompresion", "Tagged Image File Format (.tiff)"))
        self.comboBoxFormato.setItemText(6, _translate("FormatoCompresion", "ICO (.ico)"))
        self.checkBoxSinPerdida.setText(_translate("FormatoCompresion", "Sin pérdida"))

class Ui_Redimensionar(Ui_MainWindow, object):
    def setupUi(self, Redimensionar):
        Redimensionar.setObjectName("Redimensionar")
        Redimensionar.setFixedSize(253, 236)
        self.centralwidget = QtWidgets.QWidget(Redimensionar)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(30, 30, 201, 131))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayoutRedimensionar = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayoutRedimensionar.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutRedimensionar.setObjectName("gridLayoutRedimensionar")
        self.spinBoxAltura = QtWidgets.QSpinBox(self.gridLayoutWidget_2)
        self.spinBoxAltura.setMaximumSize(QtCore.QSize(80, 16777215))
        #self.spinBoxAltura.setAccessibleName("")
        self.spinBoxAltura.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBoxAltura.setMaximum(99999)
        self.spinBoxAltura.setValue(1080)
        self.spinBoxAltura.setSuffix(" px")
        self.spinBoxAltura.valueChanged.connect(lambda: self.modificar_tamanho(parte="altura"))
        self.spinBoxAltura.setObjectName("spinBoxAltura")
        self.gridLayoutRedimensionar.addWidget(self.spinBoxAltura, 1, 2, 1, 1)
        self.horizontalLayoutProporcion = QtWidgets.QHBoxLayout()
        self.horizontalLayoutProporcion.setObjectName("horizontalLayoutProporcion")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayoutProporcion.addItem(spacerItem)
        self.checkBoxProporcion = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.checkBoxProporcion.setChecked(True)
        self.checkBoxProporcion.setObjectName("checkBoxProporcion")
        self.horizontalLayoutProporcion.addWidget(self.checkBoxProporcion)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayoutProporcion.addItem(spacerItem1)
        self.gridLayoutRedimensionar.addLayout(self.horizontalLayoutProporcion, 3, 0, 1, 3)
        self.labelAnchura = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.labelAnchura.setFont(font)
        self.labelAnchura.setAlignment(QtCore.Qt.AlignCenter)
        self.labelAnchura.setObjectName("labelAnchura")
        self.gridLayoutRedimensionar.addWidget(self.labelAnchura, 0, 0, 1, 1)
        self.labelX = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.labelX.setMaximumSize(QtCore.QSize(10, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.labelX.setFont(font)
        #self.labelX.setAccessibleName("")
        self.labelX.setAlignment(QtCore.Qt.AlignCenter)
        self.labelX.setText("x")
        self.labelX.setObjectName("labelX")
        self.gridLayoutRedimensionar.addWidget(self.labelX, 1, 1, 1, 1)
        self.labelAltura = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.labelAltura.setFont(font)
        self.labelAltura.setAlignment(QtCore.Qt.AlignCenter)
        self.labelAltura.setObjectName("labelAltura")
        self.gridLayoutRedimensionar.addWidget(self.labelAltura, 0, 2, 1, 1)
        self.horizontalLayoutTipoRedimension = QtWidgets.QHBoxLayout()
        self.horizontalLayoutTipoRedimension.setObjectName("horizontalLayoutTipoRedimension")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayoutTipoRedimension.addItem(spacerItem2)
        self.radioPixeles = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        #self.radioPixeles.setAccessibleName("")
        self.radioPixeles.setText("px")
        self.radioPixeles.setChecked(True)
        self.radioPixeles.toggled.connect(self.radios_tamanho)
        self.radioPixeles.setObjectName("radioPixels")
        self.horizontalLayoutTipoRedimension.addWidget(self.radioPixeles)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayoutTipoRedimension.addItem(spacerItem3)
        self.radioPorcentaje = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        #self.radioPorcentaje.setAccessibleName("")
        self.radioPorcentaje.setText("%")
        self.radioPorcentaje.toggled.connect(self.radios_tamanho)
        self.radioPorcentaje.setObjectName("radioPorcentaje")
        self.horizontalLayoutTipoRedimension.addWidget(self.radioPorcentaje)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayoutTipoRedimension.addItem(spacerItem4)
        self.gridLayoutRedimensionar.addLayout(self.horizontalLayoutTipoRedimension, 2, 0, 1, 3)
        self.spinBoxAnchura = QtWidgets.QSpinBox(self.gridLayoutWidget_2)
        self.spinBoxAnchura.setMaximumSize(QtCore.QSize(80, 16777215))
        #self.spinBoxAnchura.setAccessibleName("")
        self.spinBoxAnchura.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBoxAnchura.setSuffix(" px")
        self.spinBoxAnchura.setMaximum(99999)
        self.spinBoxAnchura.setValue(1920)
        self.spinBoxAnchura.valueChanged.connect(lambda: self.modificar_tamanho(parte="anchura"))
        self.spinBoxAnchura.setObjectName("spinBoxAnchura")
        self.gridLayoutRedimensionar.addWidget(self.spinBoxAnchura, 1, 0, 1, 1)
        self.buttonBoxRedimensionar = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.buttonBoxRedimensionar.setGeometry(QtCore.QRect(40, 180, 182, 34))
        self.buttonBoxRedimensionar.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBoxRedimensionar.setObjectName("buttonBoxRedimensionar")
        self.buttonBoxRedimensionar.accepted.connect(self.aceptar_tamanho)
        self.buttonBoxRedimensionar.rejected.connect(self.cancelar_tamanho)
        Redimensionar.setCentralWidget(self.centralwidget)

        self.retranslateUi(Redimensionar)
        QtCore.QMetaObject.connectSlotsByName(Redimensionar)
        self.Redimensionar = Redimensionar

        self.anchura_base = True

    def modificar_tamanho(self, parte):  
        anchura = self.spinBoxAnchura.value()
        altura = self.spinBoxAltura.value()
        if self.checkBoxProporcion.isChecked():
            if self.radioPorcentaje.isChecked():
                if parte == "anchura":
                    self.spinBoxAltura.setValue(anchura)
                elif parte == "altura":
                    self.spinBoxAnchura.setValue(altura)
            else:
                anchura = 1920
                altura = 1080
                if parte == "anchura":
                    self.anchura_base = True
                    self.spinBoxAnchura.setStyleSheet("text-decoration: underline;")
                    self.spinBoxAltura.setStyleSheet("text-decoration: none")
                    
                else: 
                    self.anchura_base = False
                    self.spinBoxAltura.setStyleSheet("text-decoration: underline")
                    self.spinBoxAnchura.setStyleSheet("text-decoration: none")
                    

    
    def aceptar_tamanho(self):
        self.Redimensionar.close()
        if self.radioPorcentaje.isChecked():
            diccionario_ediciones["tamaño"] = "-resize", str(self.spinBoxAnchura.value()) + "%x" + str(self.spinBoxAltura.value()) + "%"
            if self.checkBoxProporcion.isChecked():
                tamanhoButton.setText("Tamaño:\n"+str(self.spinBoxAnchura.value())+ "%")
            else:
                tamanhoButton.setText("Tamaño:\n"+str(self.spinBoxAnchura.value())+ "%x" +str(self.spinBoxAltura.value())+"%")
        else:
            if self.checkBoxProporcion.isChecked():
                if self.anchura_base == True:
                    diccionario_ediciones["tamaño"] = "-resize", str(self.spinBoxAnchura.value())
                    tamanhoButton.setText("Tamaño:\n"+str(self.spinBoxAnchura.value())+ "px\nAncho")
                else:
                    diccionario_ediciones["tamaño"] = "-resize", "x" + str(self.spinBoxAltura.value())
                    tamanhoButton.setText("Tamaño:\n"+str(self.spinBoxAltura.value())+ "px\nAlto")
            else:
                diccionario_ediciones["tamaño"] = "-resize", str(self.spinBoxAnchura.value()) + "x" + str(self.spinBoxAltura.value()) + "!"
                tamanhoButton.setText("Tamaño:\n"+str(self.spinBoxAnchura.value())+ "x" +str(self.spinBoxAltura.value()))
        print(diccionario_ediciones)
    
    def radios_tamanho(self):
        if self.radioPixeles.isChecked():
            self.spinBoxAltura.setValue(1080)
            self.spinBoxAltura.setSuffix(" px")
            self.spinBoxAnchura.setValue(1920)
            self.spinBoxAnchura.setSuffix(" px")
            self.spinBoxAltura.setMaximum(99999)
            self.spinBoxAnchura.setMaximum(99999)
        else:
            self.spinBoxAltura.setValue(100)
            self.spinBoxAltura.setSuffix(" %")
            self.spinBoxAnchura.setValue(100)
            self.spinBoxAnchura.setSuffix(" %")
            self.spinBoxAltura.setMaximum(1000)
            self.spinBoxAnchura.setMaximum(1000)
        
    def cancelar_tamanho(self):
        self.Redimensionar.close()
        if diccionario_ediciones["tamaño"] == []:
            del diccionario_ediciones["tamaño"]
            tamanhoButton.hide()
            horizontalLayoutEdiciones.removeWidget(tamanhoButton)
            horizontalLayoutEdiciones.invalidate()
            global numero_ediciones
            numero_ediciones -= 1
        print(diccionario_ediciones)


    def retranslateUi(self, Redimensionar):
        _translate = QtCore.QCoreApplication.translate
        Redimensionar.setWindowTitle(_translate("Redimensionar", "Redimensionar"))
        self.checkBoxProporcion.setText(_translate("Redimensionar", "Mantener proporción"))
        self.labelAnchura.setText(_translate("Redimensionar", "Anchura"))
        self.labelAltura.setText(_translate("Redimensionar", "Altura"))
        
class Ui_Contraste(Ui_MainWindow, object):
    def setupUi(self, Contraste):
        Contraste.setObjectName("Contraste")
        Contraste.setFixedSize(414, 234)
        self.centralwidget = QtWidgets.QWidget(Contraste)
        self.centralwidget.setObjectName("centralwidget")
        self.labelContraste = QtWidgets.QLabel(self.centralwidget)
        self.labelContraste.setGeometry(QtCore.QRect(40, 40, 101, 18))
        self.labelContraste.setMinimumSize(QtCore.QSize(50, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.labelContraste.setFont(font)
        self.labelContraste.setObjectName("labelContraste")
        self.horizontalSliderContraste = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSliderContraste.setGeometry(QtCore.QRect(160, 40, 200, 20))
        self.horizontalSliderContraste.setMinimumSize(QtCore.QSize(100, 0))
        #self.horizontalSliderContraste.setAccessibleName("")
        #self.horizontalSliderContraste.setAccessibleDescription("")
        self.horizontalSliderContraste.setMinimum(-50)
        self.horizontalSliderContraste.setMaximum(50)
        self.horizontalSliderContraste.setSingleStep(0)
        self.horizontalSliderContraste.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderContraste.valueChanged.connect(self.actualizar_valor_contraste)
        self.horizontalSliderContraste.setObjectName("horizontalSliderContraste")
        self.checkBoxBlancoNegro = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxBlancoNegro.setGeometry(QtCore.QRect(40, 130, 121, 22))
        self.checkBoxBlancoNegro.setObjectName("checkBoxBlancoNegro")
        self.buttonBoxContraste = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.buttonBoxContraste.setGeometry(QtCore.QRect(120, 180, 182, 34))
        self.buttonBoxContraste.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBoxContraste.accepted.connect(self.aceptar_contraste)
        self.buttonBoxContraste.rejected.connect(self.cancelar_contraste)
        self.buttonBoxContraste.setObjectName("buttonBoxContraste")
        self.labelBrillo = QtWidgets.QLabel(self.centralwidget)
        self.labelBrillo.setGeometry(QtCore.QRect(40, 90, 56, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.labelBrillo.setFont(font)
        self.labelBrillo.setObjectName("labelBrillo")
        self.horizontalSliderBrillo = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSliderBrillo.setGeometry(QtCore.QRect(160, 90, 200, 20))
        #self.horizontalSliderBrillo.setAccessibleName("")
        #self.horizontalSliderBrillo.setAccessibleDescription("")
        self.horizontalSliderBrillo.setMinimum(-50)
        self.horizontalSliderBrillo.setMaximum(50)
        self.horizontalSliderBrillo.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderBrillo.valueChanged.connect(self.actualizar_valor_brillo)
        self.horizontalSliderBrillo.setObjectName("horizontalSliderBrillo")
        self.labelValorContraste = QtWidgets.QLabel(self.centralwidget)
        self.labelValorContraste.setGeometry(QtCore.QRect(256, 20, 31, 18))
        #self.labelValorContraste.setAccessibleName("")
        #self.labelValorContraste.setAccessibleDescription("")
        self.labelValorContraste.setText("0")
        self.labelValorContraste.setObjectName("labelValorContraste")
        self.labelValorBrillo = QtWidgets.QLabel(self.centralwidget)
        self.labelValorBrillo.setGeometry(QtCore.QRect(256, 70, 31, 18))
        #self.labelValorBrillo.setAccessibleName("")
        #self.labelValorBrillo.setAccessibleDescription("")
        self.labelValorBrillo.setText("0")
        self.labelValorBrillo.setObjectName("labelValorBrillo")
        Contraste.setCentralWidget(self.centralwidget)

        self.retranslateUi(Contraste)
        QtCore.QMetaObject.connectSlotsByName(Contraste)
        self.Contraste = Contraste

    
    def cancelar_contraste(self):
        self.Contraste.close()
        if diccionario_ediciones["contraste"] == []:
            del diccionario_ediciones["contraste"]
            contrasteButton.hide()
            horizontalLayoutEdiciones.removeWidget(contrasteButton)
            horizontalLayoutEdiciones.invalidate()
            global numero_ediciones
            numero_ediciones -= 1
        print(diccionario_ediciones)
        
    
    def aceptar_contraste(self):
        self.Contraste.close()
        if self.checkBoxBlancoNegro.isChecked():
            diccionario_ediciones["contraste"] = "-colorspace", "Gray", "-brightness-contrast", str(self.horizontalSliderBrillo.value()) + "x" + str(self.horizontalSliderContraste.value())
            if self.horizontalSliderBrillo.value() != 0 and self.horizontalSliderContraste.value() != 0:
                contrasteButton.setText("Contraste:\n" + str(self.horizontalSliderContraste.value()) + "\nByN\nBrillo:\n" + str(self.horizontalSliderBrillo.value()))
            elif self.horizontalSliderBrillo.value() == 0 and self.horizontalSliderContraste.value() != 0:
                contrasteButton.setText("Contraste:\n" + str(self.horizontalSliderContraste.value()) + "\nByN")
            elif self.horizontalSliderBrillo.value() != 0 and self.horizontalSliderContraste.value() == 0:
                contrasteButton.setText("Brillo:\n" + str(self.horizontalSliderBrillo.value()) + "\nByN")
            else: 
                contrasteButton.setText("Contraste:\nByN")
        else:
            diccionario_ediciones["contraste"] = "-brightness-contrast", str(self.horizontalSliderBrillo.value()) + "x" + str(self.horizontalSliderContraste.value())
            if self.horizontalSliderBrillo.value() != 0 and self.horizontalSliderContraste.value() != 0:
                contrasteButton.setText("Contraste:\n" + str(self.horizontalSliderContraste.value()) + "\nBrillo:\n" + str(self.horizontalSliderBrillo.value()))
            elif self.horizontalSliderBrillo.value() == 0 and self.horizontalSliderContraste.value() != 0:
                contrasteButton.setText("Contraste:\n" + str(self.horizontalSliderContraste.value()))
            elif self.horizontalSliderBrillo.value() != 0 and self.horizontalSliderContraste.value() == 0:
                contrasteButton.setText("Brillo:\n" + str(self.horizontalSliderBrillo.value()))
            else:
                contrasteButton.hide()
                del diccionario_ediciones["contraste"]
                horizontalLayoutEdiciones.removeWidget(contrasteButton)
                horizontalLayoutEdiciones.invalidate()
                global numero_ediciones
                numero_ediciones -= 1
        print(diccionario_ediciones)

    

    def actualizar_valor_contraste(self):
        if self.horizontalSliderContraste.valueChanged:
            self.labelValorContraste.setText(str(self.horizontalSliderContraste.value()))
            if self.horizontalSliderContraste.value() > -10 and self.horizontalSliderContraste.value() < 10:
                posicion = (self.horizontalSliderContraste.value() * 2) * 0.93 + 256
            else:
                posicion = (self.horizontalSliderContraste.value() * 2) * 0.93 + 251
            self.labelValorContraste.setGeometry(QtCore.QRect(int(posicion), 20, 31,18))


    def actualizar_valor_brillo(self, valor):
        if self.horizontalSliderBrillo.valueChanged:
            self.labelValorBrillo.setText(str(self.horizontalSliderBrillo.value()))
            if self.horizontalSliderBrillo.value() > -10 and self.horizontalSliderBrillo.value() < 10:
                posicion = (self.horizontalSliderBrillo.value() * 2) * 0.93 + 256
            else:
                posicion = (self.horizontalSliderBrillo.value() * 2) * 0.93 + 251
            self.labelValorBrillo.setGeometry(QtCore.QRect(int(posicion), 70, 31,18))

    

    def retranslateUi(self, Contraste):
        _translate = QtCore.QCoreApplication.translate
        Contraste.setWindowTitle(_translate("Contraste", "Contraste"))
        self.labelContraste.setText(_translate("Contraste", "Contraste:"))
        self.checkBoxBlancoNegro.setText(_translate("Contraste", "Blanco y negro"))
        self.labelBrillo.setText(_translate("Contraste", "Brillo:"))
        
class Ui_Rotar(Ui_MainWindow, object):
    def setupUi(self, Rotar):
        Rotar.setObjectName("Rotar")
        Rotar.setFixedSize(279, 178)
        self.centralwidget = QtWidgets.QWidget(Rotar)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(50, 20, 192, 92))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayoutRotar = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayoutRotar.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutRotar.setObjectName("gridLayoutRotar")
        self.labelVolteo = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.labelVolteo.setFont(font)
        self.labelVolteo.setObjectName("labelVolteo")
        self.gridLayoutRotar.addWidget(self.labelVolteo, 0, 0, 1, 1)
        self.verticalLayoutVolteo = QtWidgets.QVBoxLayout()
        self.verticalLayoutVolteo.setObjectName("verticalLayoutVolteo")
        self.checkBoxVolteoHorizontal = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.checkBoxVolteoHorizontal.setObjectName("checkBoxVolteoHorizontal")
        self.verticalLayoutVolteo.addWidget(self.checkBoxVolteoHorizontal)
        self.checkBoxVolteoVertical = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.checkBoxVolteoVertical.setObjectName("checkBoxVolteoVertical")
        self.verticalLayoutVolteo.addWidget(self.checkBoxVolteoVertical)
        self.gridLayoutRotar.addLayout(self.verticalLayoutVolteo, 0, 1, 1, 1)
        self.labelRotacion = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.labelRotacion.setFont(font)
        self.labelRotacion.setObjectName("labelRotacion")
        self.gridLayoutRotar.addWidget(self.labelRotacion, 1, 0, 1, 1)
        self.comboBoxRotacion = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBoxRotacion.setMaximumSize(QtCore.QSize(55, 16777215))
        #self.comboBoxRotacion.setAccessibleDescription("")
        self.comboBoxRotacion.setStyleSheet("")
        self.comboBoxRotacion.setCurrentText("0")
        self.comboBoxRotacion.setObjectName("comboBoxRotacion")
        self.comboBoxRotacion.addItem("")
        self.comboBoxRotacion.addItem("")
        self.comboBoxRotacion.addItem("")
        self.comboBoxRotacion.addItem("")
        self.comboBoxRotacion.setItemText(0, "0")
        self.comboBoxRotacion.setItemText(1, "90")
        self.comboBoxRotacion.setItemText(2, "180")
        self.comboBoxRotacion.setItemText(3, "270")
        self.gridLayoutRotar.addWidget(self.comboBoxRotacion, 1, 1, 1, 1)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 120, 281, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayoutButtonBoxRotar = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayoutButtonBoxRotar.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayoutButtonBoxRotar.setObjectName("horizontalLayoutButtonBoxRotar")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayoutButtonBoxRotar.addItem(spacerItem)
        self.buttonBoxRotar = QtWidgets.QDialogButtonBox(self.horizontalLayoutWidget)
        self.buttonBoxRotar.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBoxRotar.accepted.connect(self.aceptar_rotacion)
        self.buttonBoxRotar.rejected.connect(self.cancelar_rotacion)
        self.buttonBoxRotar.setObjectName("buttonBoxRotar")
        self.horizontalLayoutButtonBoxRotar.addWidget(self.buttonBoxRotar)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayoutButtonBoxRotar.addItem(spacerItem1)
        Rotar.setCentralWidget(self.centralwidget)

        self.retranslateUi(Rotar)
        QtCore.QMetaObject.connectSlotsByName(Rotar)
        self.Rotar = Rotar
    
    def aceptar_rotacion(self):
        self.Rotar.close()
        if self.checkBoxVolteoHorizontal.isChecked() and self.checkBoxVolteoVertical.isChecked() and self.comboBoxRotacion.currentText() == "0":
            diccionario_ediciones["rotar"] = "-flop", "-flip"
            rotarButton.setText("Volteo:\nHorizontal\nVertical")
        elif self.checkBoxVolteoHorizontal.isChecked() and self.comboBoxRotacion.currentText() == "0":
            diccionario_ediciones["rotar"] = "-flop", #Coma para que sea tupla
            rotarButton.setText("Volteo:\nHorizontal")
        elif self.checkBoxVolteoVertical.isChecked() and self.comboBoxRotacion.currentText() == "0":
            diccionario_ediciones["rotar"] = "-flip",
            rotarButton.setText("Volteo:\nVertical")
        elif self.checkBoxVolteoHorizontal.isChecked() and self.checkBoxVolteoVertical.isChecked() and self.comboBoxRotacion.currentText() != "0":
            diccionario_ediciones["rotar"] = "-flop", "-flip", "-rotate", self.comboBoxRotacion.currentText()
            rotarButton.setText("Volteo:\nHorizontal\nVertical\n\nRotación:\n" + self.comboBoxRotacion.currentText() + "º")
        elif self.checkBoxVolteoHorizontal.isChecked() and self.comboBoxRotacion.currentText() != "0":
            diccionario_ediciones["rotar"] = "-flop", "-rotate", self.comboBoxRotacion.currentText()
            rotarButton.setText("Volteo:\nHorizontal\n\nRotación:\n" + self.comboBoxRotacion.currentText() + "º")
        elif self.checkBoxVolteoVertical.isChecked() and self.comboBoxRotacion.currentText() != "0":
            diccionario_ediciones["rotar"] = "-flip", "-rotate", self.comboBoxRotacion.currentText()
            rotarButton.setText("Volteo:\nVertical\n\nRotación:\n" + self.comboBoxRotacion.currentText() + "º")
        elif self.comboBoxRotacion.currentText() != "0":
            diccionario_ediciones["rotar"] = "-rotate", self.comboBoxRotacion.currentText()
            rotarButton.setText("Rotación:\n" + self.comboBoxRotacion.currentText() + "º")
        else:
            self.Rotar.close()
            del diccionario_ediciones["rotar"]
            rotarButton.hide()
            horizontalLayoutEdiciones.removeWidget(rotarButton)
            horizontalLayoutEdiciones.invalidate()
            global numero_ediciones
            numero_ediciones -= 1
        print(diccionario_ediciones)
    
    def cancelar_rotacion(self):
        self.Rotar.close()
        if diccionario_ediciones["rotar"] == []:
            del diccionario_ediciones["rotar"]
            rotarButton.hide()
            horizontalLayoutEdiciones.removeWidget(rotarButton)
            horizontalLayoutEdiciones.invalidate()
            global numero_ediciones
            numero_ediciones -= 1
        print(diccionario_ediciones)


    def retranslateUi(self, Rotar):
        _translate = QtCore.QCoreApplication.translate
        Rotar.setWindowTitle(_translate("Rotar", "Rotar o reflejar"))
        self.labelVolteo.setText(_translate("Rotar", "Volteo:"))
        self.checkBoxVolteoHorizontal.setText(_translate("Rotar", "Horizontal"))
        self.checkBoxVolteoVertical.setText(_translate("Rotar", "Vertical"))
        self.labelRotacion.setText(_translate("Rotar", "Rotación:"))
        


class Ui_Recortar(Ui_MainWindow, object):
    def setupUi(self, Recortar):
        Recortar.setObjectName("Recortar")
        Recortar.setFixedSize(305, 370)
        self.centralwidget = QtWidgets.QWidget(Recortar)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(40, 40, 223, 107))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayoutDimensiones = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayoutDimensiones.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutDimensiones.setObjectName("gridLayoutDimensiones")
        self.spinBoxAnchura = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBoxAnchura.setMaximumSize(QtCore.QSize(85, 16777215))
        self.spinBoxAnchura.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBoxAnchura.setMaximum(99999)
        self.spinBoxAnchura.setObjectName("spinBoxAnchura")
        self.gridLayoutDimensiones.addWidget(self.spinBoxAnchura, 2, 0, 1, 1)
        self.spinBoxAltura = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBoxAltura.setMaximumSize(QtCore.QSize(85, 16777215))
        self.spinBoxAltura.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBoxAltura.setMaximum(99999)
        self.spinBoxAltura.setObjectName("spinBoxAltura")
        self.gridLayoutDimensiones.addWidget(self.spinBoxAltura, 2, 1, 1, 1)
        self.labelAnchura = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.labelAnchura.setFont(font)
        self.labelAnchura.setAlignment(QtCore.Qt.AlignCenter)
        self.labelAnchura.setObjectName("labelAnchura")
        self.gridLayoutDimensiones.addWidget(self.labelAnchura, 1, 0, 1, 1)
        self.labelAltura = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.labelAltura.setFont(font)
        self.labelAltura.setAlignment(QtCore.Qt.AlignCenter)
        self.labelAltura.setObjectName("labelAltura")
        self.gridLayoutDimensiones.addWidget(self.labelAltura, 1, 1, 1, 1)
        self.labelDimensiones = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.labelDimensiones.setFont(font)
        self.labelDimensiones.setAlignment(QtCore.Qt.AlignCenter)
        self.labelDimensiones.setObjectName("labelDimensiones")
        self.gridLayoutDimensiones.addWidget(self.labelDimensiones, 0, 0, 1, 2)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(40, 170, 221, 107))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayoutCoordenadas = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayoutCoordenadas.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutCoordenadas.setObjectName("gridLayoutCoordenadas")
        self.labelEjeX = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.labelEjeX.setFont(font)
        self.labelEjeX.setAlignment(QtCore.Qt.AlignCenter)
        self.labelEjeX.setObjectName("labelEjeX")
        self.gridLayoutCoordenadas.addWidget(self.labelEjeX, 1, 0, 1, 1)
        self.labelEjeY = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.labelEjeY.setFont(font)
        self.labelEjeY.setAlignment(QtCore.Qt.AlignCenter)
        self.labelEjeY.setObjectName("labelEjeY")
        self.gridLayoutCoordenadas.addWidget(self.labelEjeY, 1, 1, 1, 1)
        self.labelCoordenadas = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.labelCoordenadas.setFont(font)
        self.labelCoordenadas.setAlignment(QtCore.Qt.AlignCenter)
        self.labelCoordenadas.setObjectName("labelCoordenadas")
        self.gridLayoutCoordenadas.addWidget(self.labelCoordenadas, 0, 0, 1, 2)
        self.spinBoxEjeX = QtWidgets.QSpinBox(self.gridLayoutWidget_2)
        self.spinBoxEjeX.setMaximumSize(QtCore.QSize(85, 16777215))
        self.spinBoxEjeX.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBoxEjeX.setMaximum(99999)
        self.spinBoxEjeX.setObjectName("spinBoxEjeX")
        self.gridLayoutCoordenadas.addWidget(self.spinBoxEjeX, 2, 0, 1, 1)
        self.spinBoxEjeY = QtWidgets.QSpinBox(self.gridLayoutWidget_2)
        self.spinBoxEjeY.setMaximumSize(QtCore.QSize(85, 16777215))
        self.spinBoxEjeY.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBoxEjeY.setMaximum(99999)
        self.spinBoxEjeY.setObjectName("spinBoxEjeY")
        self.gridLayoutCoordenadas.addWidget(self.spinBoxEjeY, 2, 1, 1, 1)
        self.buttonBoxRecortar = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.buttonBoxRecortar.setGeometry(QtCore.QRect(61, 300, 182, 34))
        self.buttonBoxRecortar.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBoxRecortar.accepted.connect(self.aceptar_recorte)
        self.buttonBoxRecortar.rejected.connect(self.cancelar_recorte)
        self.buttonBoxRecortar.setObjectName("buttonBoxRecortar")
        Recortar.setCentralWidget(self.centralwidget)

        self.retranslateUi(Recortar)
        QtCore.QMetaObject.connectSlotsByName(Recortar)
        self.Recortar = Recortar


    def aceptar_recorte(self):
        self.Recortar.hide()
        if self.spinBoxAnchura.value() != 0 and self.spinBoxAltura.value() != 0:
            diccionario_ediciones["recortar"] = "-crop", str(self.spinBoxAnchura.value()) + "x" + str(self.spinBoxAltura.value()) + "+" + str(self.spinBoxEjeX.value()) + "+" + str(self.spinBoxEjeY.value()) 
            recortarButton.setText("Tamaño:\n" + str(self.spinBoxAnchura.value()) + "x" + str(self.spinBoxAltura.value()) + "px\n\nDesde:\nEje X: " + str(self.spinBoxEjeX.value()) +"\nEje Y: " + str(self.spinBoxEjeY.value()))
        else:
            self.Recortar.hide()
            del diccionario_ediciones["recortar"]
            recortarButton.hide()
            horizontalLayoutEdiciones.invalidate()
            global numero_ediciones
            numero_ediciones -= 1
        print(diccionario_ediciones)
    
    def cancelar_recorte(self):
        self.Recortar.hide()
        if diccionario_ediciones["recortar"] == []:
            del diccionario_ediciones["recortar"]
            recortarButton.hide()
            horizontalLayoutEdiciones.removeWidget(recortarButton)
            horizontalLayoutEdiciones.invalidate()
            global numero_ediciones
            numero_ediciones -= 1
        print(diccionario_ediciones)
        


    def retranslateUi(self, Recortar):
        _translate = QtCore.QCoreApplication.translate
        Recortar.setWindowTitle(_translate("Recortar", "Recortar"))
        self.labelAnchura.setText(_translate("Recortar", "Anchura"))
        self.labelAltura.setText(_translate("Recortar", "Altura"))
        self.labelDimensiones.setText(_translate("Recortar", "Dimensiones"))
        self.labelEjeX.setText(_translate("Recortar", "Eje X"))
        self.labelEjeY.setText(_translate("Recortar", "Eje Y"))
        self.labelCoordenadas.setText(_translate("Recortar", "Coordenadas"))

class Ui_MarcaAgua(Ui_MainWindow, object):
    def setupUi(self, MarcaAgua):
        MarcaAgua.setObjectName("MarcaAgua")
        MarcaAgua.resize(340, 482)
        self.centralwidget = QtWidgets.QWidget(MarcaAgua)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 20, 282, 257))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayoutMarcaAgua = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayoutMarcaAgua.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutMarcaAgua.setObjectName("gridLayoutMarcaAgua")
        self.pushButtonCentro = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(60)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonCentro.setFont(font)
        self.pushButtonCentro.setCheckable(True)
        self.pushButtonCentro.clicked.connect(lambda: self.marcar_boton(posicion="centro"))
        self.pushButtonCentro.setText("·")
        self.pushButtonCentro.setObjectName("pushButtonCentro")
        self.gridLayoutMarcaAgua.addWidget(self.pushButtonCentro, 2, 1, 1, 1)
        self.pushButtonAbajoDerecha = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonAbajoDerecha.setFont(font)
        self.pushButtonAbajoDerecha.setCheckable(True)
        self.pushButtonAbajoDerecha.clicked.connect(lambda: self.marcar_boton(posicion="abajo-derecha"))
        self.pushButtonAbajoDerecha.setText("↘")
        self.pushButtonAbajoDerecha.setObjectName("pushButtonAbajoDerecha")
        self.gridLayoutMarcaAgua.addWidget(self.pushButtonAbajoDerecha, 3, 2, 1, 1)
        self.pushButtonArribaDerecha = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonArribaDerecha.setFont(font)
        self.pushButtonArribaDerecha.setCheckable(True)
        self.pushButtonArribaDerecha.clicked.connect(lambda: self.marcar_boton(posicion="arriba-derecha"))
        self.pushButtonArribaDerecha.setText("↗")
        self.pushButtonArribaDerecha.setObjectName("pushButtonArribaDerecha")
        self.gridLayoutMarcaAgua.addWidget(self.pushButtonArribaDerecha, 1, 2, 1, 1)
        self.pushButtonArribaIzquierda = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonArribaIzquierda.setFont(font)
        self.pushButtonArribaIzquierda.setCheckable(True)
        self.pushButtonArribaIzquierda.clicked.connect(lambda: self.marcar_boton(posicion="arriba-izquierda"))
        self.pushButtonArribaIzquierda.setText("↖")
        self.pushButtonArribaIzquierda.setObjectName("pushButtonArribaIzquierda")
        self.gridLayoutMarcaAgua.addWidget(self.pushButtonArribaIzquierda, 1, 0, 1, 1)
        self.pushButtonAbajoIzquierda = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonAbajoIzquierda.setFont(font)
        self.pushButtonAbajoIzquierda.setCheckable(True)
        self.pushButtonAbajoIzquierda.clicked.connect(lambda: self.marcar_boton(posicion="abajo-izquierda"))
        self.pushButtonAbajoIzquierda.setText("↙")
        self.pushButtonAbajoIzquierda.setObjectName("pushButtonAbajoIzquierda")
        self.gridLayoutMarcaAgua.addWidget(self.pushButtonAbajoIzquierda, 3, 0, 1, 1)
        self.pushButtonAbajo = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonAbajo.setFont(font)
        self.pushButtonAbajo.setCheckable(True)
        self.pushButtonAbajo.clicked.connect(lambda: self.marcar_boton(posicion="abajo"))
        self.pushButtonAbajo.setText("↓")
        self.pushButtonAbajo.setObjectName("pushButtonAbajo")
        self.gridLayoutMarcaAgua.addWidget(self.pushButtonAbajo, 3, 1, 1, 1)
        self.labelMarcaAgua = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.labelMarcaAgua.setFont(font)
        self.labelMarcaAgua.setAlignment(QtCore.Qt.AlignCenter)
        self.labelMarcaAgua.setObjectName("labelMarcaAgua")
        self.gridLayoutMarcaAgua.addWidget(self.labelMarcaAgua, 0, 0, 1, 3)
        self.pushButtonDerecha = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonDerecha.setFont(font)
        self.pushButtonDerecha.setCheckable(True)
        self.pushButtonDerecha.clicked.connect(lambda: self.marcar_boton(posicion="derecha"))
        self.pushButtonDerecha.setText("→")
        self.pushButtonDerecha.setObjectName("pushButtonDerecha")
        self.gridLayoutMarcaAgua.addWidget(self.pushButtonDerecha, 2, 2, 1, 1)
        self.pushButtonArriba = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonArriba.setFont(font)
        self.pushButtonArriba.setCheckable(True)
        self.pushButtonArriba.clicked.connect(lambda: self.marcar_boton(posicion="arriba"))
        self.pushButtonArriba.setText("↑")
        self.pushButtonArriba.setObjectName("pushButtonArriba")
        self.gridLayoutMarcaAgua.addWidget(self.pushButtonArriba, 1, 1, 1, 1)
        self.pushButtonIzquierda = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonIzquierda.setFont(font)
        self.pushButtonIzquierda.setCheckable(True)
        self.pushButtonIzquierda.clicked.connect(lambda: self.marcar_boton(posicion="izquierda"))
        self.pushButtonIzquierda.setText("←")
        self.pushButtonIzquierda.setObjectName("pushButtonIzquierda")
        self.gridLayoutMarcaAgua.addWidget(self.pushButtonIzquierda, 2, 0, 1, 1)
        self.pushButtonImagen = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButtonImagen.clicked.connect(self.agregar_imagen_marca_agua)
        self.pushButtonImagen.setObjectName("pushButtonImagen")
        self.gridLayoutMarcaAgua.addWidget(self.pushButtonImagen, 4, 1, 1, 1)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(40, 300, 263, 67))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayoutPosicion = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayoutPosicion.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutPosicion.setObjectName("gridLayoutPosicion")
        self.labelPosicion = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.labelPosicion.setMaximumSize(QtCore.QSize(83, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.labelPosicion.setFont(font)
        self.labelPosicion.setObjectName("labelPosicion")
        self.gridLayoutPosicion.addWidget(self.labelPosicion, 1, 0, 1, 1)
        self.spinBoxEjeX = QtWidgets.QSpinBox(self.gridLayoutWidget_2)
        self.spinBoxEjeX.setMaximumSize(QtCore.QSize(70, 16777215))
        self.spinBoxEjeX.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBoxEjeX.setSuffix(" px")
        self.spinBoxEjeX.setMinimum(-500)
        self.spinBoxEjeX.setMaximum(500)
        self.spinBoxEjeX.setObjectName("spinBoxEjeX")
        self.gridLayoutPosicion.addWidget(self.spinBoxEjeX, 1, 1, 1, 1)
        self.spinBoxEjeY = QtWidgets.QSpinBox(self.gridLayoutWidget_2)
        self.spinBoxEjeY.setMaximumSize(QtCore.QSize(70, 16777215))
        self.spinBoxEjeY.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBoxEjeY.setSuffix(" px")
        self.spinBoxEjeY.setMinimum(-500)
        self.spinBoxEjeY.setMaximum(500)
        self.spinBoxEjeY.setObjectName("spinBoxEjeY")
        self.gridLayoutPosicion.addWidget(self.spinBoxEjeY, 1, 2, 1, 1)
        self.labelEjeX = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.labelEjeX.setFont(font)
        self.labelEjeX.setAlignment(QtCore.Qt.AlignCenter)
        self.labelEjeX.setObjectName("labelEjeX")
        self.gridLayoutPosicion.addWidget(self.labelEjeX, 0, 1, 1, 1)
        self.labelEjeY = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelEjeY.setFont(font)
        self.labelEjeY.setAlignment(QtCore.Qt.AlignCenter)
        self.labelEjeY.setObjectName("labelEjeY")
        self.gridLayoutPosicion.addWidget(self.labelEjeY, 0, 2, 1, 1)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(50, 370, 160, 34))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayoutOpacidad = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayoutOpacidad.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayoutOpacidad.setObjectName("horizontalLayoutOpacidad")
        self.checkBoxOpacidad = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.checkBoxOpacidad.stateChanged.connect(self.activar_opacidad)
        self.checkBoxOpacidad.setObjectName("checkBoxOpacidad")
        self.horizontalLayoutOpacidad.addWidget(self.checkBoxOpacidad)
        self.spinBoxOpacidad = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        self.spinBoxOpacidad.setMinimumSize(QtCore.QSize(65, 0))
        self.spinBoxOpacidad.setMaximumSize(QtCore.QSize(65, 16777215))
        self.spinBoxOpacidad.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBoxOpacidad.setEnabled(False)
        self.spinBoxOpacidad.setSuffix(" %")
        self.spinBoxOpacidad.setMaximum(100)
        self.spinBoxOpacidad.setProperty("value", 100)
        self.spinBoxOpacidad.setObjectName("spinBoxOpacidad")
        self.horizontalLayoutOpacidad.addWidget(self.spinBoxOpacidad)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 420, 341, 41))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayoutButtonBoxMarcaAgua = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayoutButtonBoxMarcaAgua.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayoutButtonBoxMarcaAgua.setObjectName("horizontalLayoutButtonBoxMarcaAgua")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayoutButtonBoxMarcaAgua.addItem(spacerItem)
        self.buttonBoxMarcaAgua = QtWidgets.QDialogButtonBox(self.horizontalLayoutWidget_2)
        self.buttonBoxMarcaAgua.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBoxMarcaAgua.accepted.connect(self.aceptar_marca_agua)
        self.buttonBoxMarcaAgua.rejected.connect(self.cancelar_marca_agua)
        self.buttonBoxMarcaAgua.setObjectName("buttonBoxMarcaAgua")
        self.horizontalLayoutButtonBoxMarcaAgua.addWidget(self.buttonBoxMarcaAgua)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayoutButtonBoxMarcaAgua.addItem(spacerItem1)
        MarcaAgua.setCentralWidget(self.centralwidget)

        self.retranslateUi(MarcaAgua)
        QtCore.QMetaObject.connectSlotsByName(MarcaAgua)
        self.MarcaAgua = MarcaAgua


        global imagen_marca_agua
        imagen_marca_agua = None

    def agregar_imagen_marca_agua(self):
        home_dir = str(Path.home())
        dialogo_archivo = QFileDialog()
        dialogo_archivo.setDirectory(home_dir)
        self.nombre_archivo = dialogo_archivo.getOpenFileName()
        global imagen_marca_agua
        imagen_marca_agua = self.nombre_archivo[0]
    
    def aceptar_marca_agua(self):
        print("La ruta a la imagen sería", imagen_marca_agua)
        if imagen_marca_agua != None:
            self.MarcaAgua.hide()

            if self.spinBoxEjeX.value() < 0:
                ejex = "-" + str(self.spinBoxEjeX.value())
            else:
                ejex = "+" + str(self.spinBoxEjeX.value())
            if self.spinBoxEjeY.value() < 0:
                ejey = "-" + str(self.spinBoxEjeY.value())
            else:
                ejey = "+" + str(self.spinBoxEjeY.value())

            opacidad = self.spinBoxOpacidad.value()

            if self.pushButtonArribaIzquierda.isChecked():
                posicion = "northwest"
                marcaAguaButton.setText("Marca de\nagua\n\n↖ " +ejex+ejey+ "\nOpacidad:\n" + str(self.spinBoxOpacidad.value()) + "%")
            elif self.pushButtonArriba.isChecked():
                posicion = "north"
                marcaAguaButton.setText("Marca de\nagua\n\n↑ " +ejex+ejey+ "\nOpacidad:\n" + str(self.spinBoxOpacidad.value()) + "%")
            elif self.pushButtonArribaDerecha.isChecked():
                posicion = "northeast"
                marcaAguaButton.setText("Marca de\nagua\n\n↗ " +ejex+ejey+ "\nOpacidad:\n" + str(self.spinBoxOpacidad.value()) + "%")
            elif self.pushButtonIzquierda.isChecked():
                posicion = "west"
                marcaAguaButton.setText("Marca de\nagua\n\n← " +ejex+ejey+ "\nOpacidad:\n" + str(self.spinBoxOpacidad.value()) + "%")
            elif self.pushButtonCentro.isChecked():
                posicion = "center"
                marcaAguaButton.setText("Marca de\nagua\n\n⊙ " +ejex+ejey+ "\nOpacidad:\n" + str(self.spinBoxOpacidad.value()) + "%")
            elif self.pushButtonDerecha.isChecked():
                posicion = "east"
                marcaAguaButton.setText("Marca de\nagua\n\n→ " +ejex+ejey+ "\nOpacidad:\n" + str(self.spinBoxOpacidad.value()) + "%")
            elif self.pushButtonAbajoIzquierda.isChecked():
                posicion = "southwest"
                marcaAguaButton.setText("Marca de\nagua\n\n↙ " +ejex+ejey+ "\nOpacidad:\n" + str(self.spinBoxOpacidad.value()) + "%")
            elif self.pushButtonAbajo.isChecked():
                posicion = "south"
                marcaAguaButton.setText("Marca de\nagua\n\n↓ " +ejex+ejey+ "\nOpacidad:\n" + str(self.spinBoxOpacidad.value()) + "%")
            else:
                posicion = "southeast"
                marcaAguaButton.setText("Marca de\nagua\n\n↘ " +ejex+ejey+ "\nOpacidad:\n" + str(self.spinBoxOpacidad.value()) + "%")
            diccionario_ediciones["marca de agua"] = imagen_marca_agua, "-gravity", posicion, "-geometry", ejex+ejey,"-compose", "dissolve", "-define", "compose:args=" + str(opacidad) + "x100", "-composite"
            print(diccionario_ediciones)
        else:
            print("hola")
            mensaje_informacion = QMessageBox()
            mensaje_informacion.setIcon(QMessageBox.Warning)
            mensaje_informacion.setWindowTitle("Marca de Agua")
            mensaje_informacion.setText('<b>Sin imagen</b>')
            mensaje_informacion.setInformativeText("<p style=\"margin-right:25px\">No se ha seleccionado ninguna imagen para usarla como marca de agua.")
            mensaje_informacion.exec_()
            

    
    def cancelar_marca_agua(self):
        self.MarcaAgua.hide()
        if diccionario_ediciones["marca de agua"] == []:
            del diccionario_ediciones["marca de agua"]
            marcaAguaButton.hide()
            horizontalLayoutEdiciones.removeWidget(marcaAguaButton)
            horizontalLayoutEdiciones.invalidate()
            global numero_ediciones
            numero_ediciones -= 1
        print(diccionario_ediciones)

    def activar_opacidad(self):
        if self.checkBoxOpacidad.isChecked():
            self.spinBoxOpacidad.setEnabled(True)
        else:
            self.spinBoxOpacidad.setEnabled(False)
            self.spinBoxOpacidad.setValue(100)


            
    
    def marcar_boton(self, posicion):
        botones = self.pushButtonArribaIzquierda, self.pushButtonArriba, self.pushButtonArribaDerecha, self.pushButtonIzquierda, self.pushButtonCentro, self.pushButtonDerecha, self.pushButtonAbajoIzquierda, self.pushButtonAbajo, self.pushButtonAbajoDerecha
        for boton in botones:
            if boton.isChecked():
                boton.setChecked(False)
        
        if posicion == "arriba-izquierda":
            self.pushButtonArribaIzquierda.setChecked(True)
        elif posicion == "arriba":
            self.pushButtonArriba.setChecked(True)
        elif posicion == "arriba-derecha":
            self.pushButtonArribaDerecha.setChecked(True)
        elif posicion == "izquierda":
            self.pushButtonIzquierda.setChecked(True)
        elif posicion == "centro":
            self.pushButtonCentro.setChecked(True)
        elif posicion == "derecha":
            self.pushButtonDerecha.setChecked(True)
        elif posicion == "abajo-izquierda":
            self.pushButtonAbajoIzquierda.setChecked(True)
        elif posicion == "abajo":
            self.pushButtonAbajo.setChecked(True)
        else:
            self.pushButtonAbajoDerecha.setChecked(True)

    def retranslateUi(self, MarcaAgua):
        _translate = QtCore.QCoreApplication.translate
        MarcaAgua.setWindowTitle(_translate("MarcaAgua", "MarcaAgua"))
        self.labelMarcaAgua.setText(_translate("MarcaAgua", "Marca de Agua"))
        self.pushButtonImagen.setText(_translate("MarcaAgua", "Imagen"))
        self.labelPosicion.setText(_translate("MarcaAgua", "Posición:"))
        self.labelEjeX.setText(_translate("MarcaAgua", "Eje X"))
        self.labelEjeY.setText(_translate("MarcaAgua", "Eje Y"))
        self.checkBoxOpacidad.setText(_translate("MarcaAgua", "Opacidad"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
