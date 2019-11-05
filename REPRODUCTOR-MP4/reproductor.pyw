import os
import sys
import webbrowser
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtWidgets import *
import time
import glob
from pathlib import Path
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'VideoPL'
        self.initUI()
        
    def initUI(self):
        #Ventana
        self.resize(800,600)
        self.setWindowIcon(QIcon("ICON.ico"))
        self.setWindowTitle(self.title)
        
        #LAYOUT
        controlLayout = QGridLayout()
        forma=QVBoxLayout()

        #BARRA HERRAMIENTAS
        menubar = QMenuBar(self)
        menubar.setGeometry(QRect(0, 0, 800, 28))
        font1 = QFont()
        font1.setFamily("Yu Gothic Light")
        font1.setPointSize(10)
        menubar.setFont(font1)
        forma.setMenuBar(menubar)

        #BARRA HERRAMIENTAS:ARCHIVO
        font2 = QFont()
        font2.setFamily("Yu Gothic Light")
        font2.setPointSize(9)
        menuArchivo = menubar.addMenu('Archivo')     
        menuArchivo.setFont(font2)
        
        #BARRA HERRAMIENTAS:AUDIO
        menuAudio= menubar.addMenu("Video")
        menuAudio.setFont(font2)
        
        
        #BARRA HERRAMIENTAS:OPINAR
        menuOpinar=menubar.addMenu("Opinar")
        menuOpinar.setFont(font2)
        
        #BARRA HERRAMIENTAS:AYUDA
        menuAyuda=menubar.addMenu("Ayuda")
        menuAyuda.setFont(font2)     
           
        
        #SLIDER
        Slider=QSlider(Qt.Horizontal)
        Slider.setEnabled(False)
        Slider.setMouseTracking(True)
        Slider.setCursor(QCursor(Qt.PointingHandCursor))
        Slider.setStyleSheet("""QSlider::groove:horizontal {border: 1px solid #999999;height: 8px; /* the groove expands to the size of the slider by default. by giving it a height, it has a fixed size */background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);margin: 2px 0;}QSlider::handle:horizontal {background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);border: 1px solid #5c5c5c;width: 18px;margin: -2px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */border-radius: 3px;}""")
         
        #TIEMPO
        Recorrido=QLabel("--:--",self)
        Total=QLabel("--:--",self)
        
        #VOLUMEN
        volumen=QSlider(Qt.Horizontal)
        volumen.setEnabled(False)
        volumen.setMouseTracking(True)
        volumen.setCursor(QCursor(Qt.PointingHandCursor))
        volumen.setRange(0,100)
        volumen.setValue(50)
        volumen.setFixedWidth(100)
        volumen.setSingleStep(20)
        volumen.setStyleSheet("""QSlider::groove:horizontal {border: 1px solid #bbb;background: white;height: 10px;border-radius: 4px;}QSlider::sub-page:horizontal {background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,stop: 0 #66e, stop: 1 #bbf);background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,stop: 0 #bbf, stop: 1 #55f);border: 1px solid #777;height: 10px;border-radius: 4px;}QSlider::add-page:horizontal {background: #fff;border: 1px solid #777;height: 10px;border-radius: 4px;}QSlider::handle:horizontal {background: qlineargradient(x1:0, y1:0, x2:1, y2:1,stop:0 #eee, stop:1 #ccc);border: 1px solid #777;
width: 13px;
margin-top: -2px;
margin-bottom: -2px;
border-radius: 4px;
}

QSlider::handle:horizontal:hover {
background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
    stop:0 #fff, stop:1 #ddd);
border: 1px solid #444;
border-radius: 4px;
}

QSlider::sub-page:horizontal:disabled {
background: #bbb;
border-color: #999;
}

QSlider::add-page:horizontal:disabled {
background: #eee;
border-color: #999;
}

QSlider::handle:horizontal:disabled {
background: #eee;
border: 1px solid #aaa;
border-radius: 4px;
}""")
                
        #MEDIAPLAYER
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget(self)
        self.videoWidget.setAutoFillBackground(True)
        pal = self.videoWidget.palette()
        pal.setColor(self.backgroundRole(), Qt.black)
        
        self.videoWidget.setPalette(pal)
        
        #BOTONES
        Boton=QPushButton(QIcon("play.png"),"",self)
        Boton.setEnabled(False)
        Boton.setFixedWidth(35)
        Boton.setFixedHeight(35)
        Boton.setShortcut(Qt.Key_Space)
        Boton.setStyleSheet("""QPushButton {color: #FFFFFF;border: 1px solid #555;border-radius: 17px;padding: 5px;background: qradialgradient(cx: 0.3, cy: -0.4,radius: 1.35, stop: 0 #fff, stop: 1 #888);min-width: 10px;}QPushButton:hover {background: qradialgradient(cx: 0.3, cy: -0.4,radius: 1.35, stop: 0 #fff, stop: 1 #bbb);}QPushButton:pressed {background: qradialgradient(cx: 0.4, cy: -0.1,radius: 1.35, stop: 0 #fff, stop: 1 #ddd);}""")
        Stop=QPushButton(QIcon("stop.png"),"",self)
        Stop.setEnabled(False)
        Stop.setFixedWidth(35)
        Stop.setFixedHeight(35)
        Stop.setShortcut(Qt.Key_Enter)
        Stop.setStyleSheet("""QPushButton {color: #FFFFFF;border: 1px solid #555;border-radius: 17px;padding: 5px;background: qradialgradient(cx: 0.3, cy: -0.4,radius: 1.35, stop: 0 #fff, stop: 1 #888);min-width: 10px;}QPushButton:hover {background: qradialgradient(cx: 0.3, cy: -0.4,radius: 1.35, stop: 0 #fff, stop: 1 #bbb);}QPushButton:pressed {background: qradialgradient(cx: 0.4, cy: -0.1,radius: 1.35, stop: 0 #fff, stop: 1 #ddd);}""")
        forma.setContentsMargins(0,0,0,10)
        controlLayout.setContentsMargins(0,0,0,0)
        forma.addWidget(self.videoWidget)
        controlLayout.addWidget(Boton,1,1)
        controlLayout.addWidget(Stop,1,2)
        controlLayout.addWidget(Recorrido,1,3)
        controlLayout.addWidget(Slider,1,4)
        controlLayout.addWidget(Total,1,5)
        controlLayout.addWidget(volumen,1,6)
        forma.addLayout(controlLayout)
        self.setLayout(forma)
        
        #Playlist
        playlist=QMediaPlaylist(self.mediaPlayer)
        
        #FUNCIONES
        def play():
            if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
                self.mediaPlayer.pause()
            else:
                self.mediaPlayer.play()
        Boton.clicked.connect(play)
        
        def state():
            if self.mediaPlayer.state()== QMediaPlayer.PlayingState:
                Boton.setIcon(QIcon("pause.png"))
            else:
                Boton.setIcon(QIcon("play.png"))
        
        def duracion(duracion):
            Slider.setRange(0,duracion)
            s= duracion // 1000
            tm, ts = divmod(s, 60)
            tm, ts = int(tm), int(ts)
            Total.setText(f"{tm:02}:{ts:02}")
        def posicion(posicion):
            Slider.setValue(posicion)
            p= posicion // 1000
            tm, ts = divmod(p, 60)
            tm, ts = int(tm), int(ts)
            Recorrido.setText(f"{tm:02}:{ts:02}")
        
        def movimiento(movimiento):
            self.mediaPlayer.setPosition(movimiento)
        
        def volume(volume):
            self.mediaPlayer.setVolume(volume)
        
        def volume2():
            self.mediaPlayer.setVolume(10)
            
        def stop():
            self.mediaPlayer.stop()
            
        #ARCHIVO:ABRIR
        Abrir = QAction('Abrir', self)         
        Abrir.setIcon(QIcon("ABRIR.png"))
        Abrir.setShortcut("Ctrl+O")
        Abrir.setShortcutContext(Qt.WindowShortcut)
        Abrir.setPriority(QAction.NormalPriority)
        menuArchivo.addAction(Abrir)
        
 
        
        def abrir():
            archivo, _=QFileDialog.getOpenFileName(None, ("Selecciona los medios"),
                                                  os.getcwd(),
                                                  ("Video Files (*.avi *.mp4 *.mkv);;Audio Files (*.mp3 *.aac)"))
            if archivo!="":
                self.mediaPlayer.setVideoOutput(self.videoWidget)
                self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(archivo)))
                self.mediaPlayer.stateChanged.connect(state)
                self.mediaPlayer.durationChanged.connect(duracion)
                self.mediaPlayer.positionChanged.connect(posicion)
                volumen.sliderMoved.connect(volume)
                volumen.sliderPressed.connect(volume2)
                Slider.sliderMoved.connect(movimiento)
                if self.mediaPlayer.NoMedia==True:
                    Boton.setEnabled(True)
                    Stop.setEnabled(True)
                    Slider.setEnabled(True)
                    volumen.setEnabled(True)
                self.setWindowTitle(Path(archivo).resolve().stem + " - VideoPL")
        Stop.clicked.connect(stop)     
        Abrir.triggered.connect(abrir)
        
        #ARCHIVO:ABRIR_CARPETA
        Abrir_carpeta = QAction("Abrir carpeta",self)
        Abrir_carpeta.setIcon(QIcon("CARPETA.png"))
        Abrir_carpeta.setShortcut("Ctrl+Alt+O")
        
        def CARPETA():
            Directorio=QFileDialog.getExistingDirectory(None,"Seleccion los medios",None,QFileDialog.ShowDirsOnly)
            extensiones = ["*.mp3",'*.mp4', '*.avi', '*.mkv']
            archivos = [f for ext in extensiones for f in glob.glob(os.path.join(Directorio, ext))]
            playlist.setCurrentIndex(0)
            def p():                
                    ss=Path(archivos[playlist.currentIndex()]).resolve().stem + " - VideoPL"
                    self.setWindowTitle(ss)        
            #Anterior
            Anterior=QAction("Anterior",self)
            Anterior.setIcon(QIcon("Anterior.png"))
            Anterior.setShortcut("-")
            Anterior.setEnabled(False)
 
            
            #Siguiente
            Siguiente = QAction("Siguiente",self)
            Siguiente.setIcon(QIcon("siguiente.png"))
            menuAudio.addAction(Siguiente)
            menuAudio.addAction(Anterior)
            Siguiente.setShortcut("+")
            Siguiente.setEnabled(False)
            def Siguiente_next():
                playlist.next()
                p()
                self.mediaPlayer.play()
            
            def Anterior_previous():
                playlist.previous()
                p()
                self.mediaPlayer.play()
            for f in archivos:
                self.mediaPlayer.setVideoOutput(self.videoWidget)
                playlist.addMedia(QMediaContent(QUrl.fromLocalFile(f)))
                playlist.setPlaybackMode(QMediaPlaylist.Sequential)
                self.mediaPlayer.setPlaylist(playlist)
                p()
                self.mediaPlayer.stateChanged.connect(state)
                self.mediaPlayer.durationChanged.connect(duracion)
                self.mediaPlayer.positionChanged.connect(posicion)
                volumen.sliderMoved.connect(volume)
                Boton.setEnabled(True)
                Stop.setEnabled(True)
                Slider.setEnabled(True)
                Siguiente.setEnabled(True)
                Anterior.setEnabled(True)
                volumen.setEnabled(True)
                Slider.sliderMoved.connect(movimiento)
                Stop.clicked.connect(stop)
                        
                        
            Siguiente.triggered.connect(Siguiente_next)
            Anterior.triggered.connect(Anterior_previous)   

        Abrir_carpeta.triggered.connect(CARPETA)
        menuArchivo.addAction(Abrir_carpeta)
        
        #AÑADO UN SEPARADOR
        menuArchivo.addSeparator()
        
        #ARCHIVO:SALIR
        Salir = QAction("Salir",self)
        Salir.setIcon(QIcon("salir.png"))
        Salir.setMenuRole(QAction.TextHeuristicRole)
        Salir.setShortcut("Ctrl+Q")
        def SALIR():
           sys.exit()
        Salir.triggered.connect(SALIR)
        menuArchivo.addAction(Salir)

        #OPINAR:OPINAR
        Opinar=QAction("Opinar",self)
        Opinar.setIcon(QIcon("Opinion.ico"))
        menuOpinar.addAction(Opinar)
        
        
        def OPINAR():
            Top = QDialog()
            Top.setBaseSize(200,200)
            Top.setStyleSheet("color: white;"
                        "background-color: grey;"
                        "selection-color: blue;"
                        "selection-background-color:blue")
            #Botones
            uno = QRadioButton(Top)
            uno.setText("Perfecto")
            dos=QRadioButton(Top)
            dos.setText("Bastante Bien")
            tres=QRadioButton(Top)
            tres.setText("Bien")
            cuatro=QRadioButton(Top)
            cuatro.setText("Mejorable")
            cinco=QRadioButton(Top)
            cinco.setText("Pesimo")
            def chequeo():
                if uno.isChecked():
                    webbrowser.open("https://www.memegenerator.es/meme/14339155")
                elif dos.isChecked():
                    webbrowser.open("https://cesminialmacenes.es/ayudanos-a-mejorar/")
                elif tres.isChecked():
                    webbrowser.open("https://tenor.com/view/onepunchman-ok-saitama-gif-4973579")
                elif cuatro.isChecked():
                    webbrowser.open("https://www.memegenerator.es/meme/1538901")
                elif cinco.isChecked():
                    webbrowser.open("https://www.memegenerator.es/meme/29233724")
                
            
            #Enviar
            Enviar=QPushButton(QIcon("ENVIAR.png"),"",Top)
            Enviar.setFixedSize(40,37)
            Enviar.clicked.connect(chequeo)
            
            Top.setWindowTitle("Opinion")
            Top.setWindowIcon(QIcon("opinion.png"))
            Top.setWindowModality(Qt.ApplicationModal)
            
            #Layout
            Layout=QGridLayout()
            Layout.addWidget(uno)
            Layout.addWidget(dos)
            Layout.addWidget(tres)
            Layout.addWidget(cuatro)
            Layout.addWidget(cinco)
            Layout.addWidget(Enviar,5,1)
            Top.setLayout(Layout)
            Top.exec_()
            
        Opinar.triggered.connect(OPINAR)
        
        #AYUDA:AYUDA
        Ayuda=QAction("Ayuda",self)
        Ayuda.setIcon(QIcon("ayuda.png"))
        menuAyuda.addAction(Ayuda)
        Ayuda.setShortcut("F1")
        def Help():
            Ventana = QDialog()
            Ventana.setFixedSize(500,500)
            Ventana.setWindowTitle('Ayuda')
            Ventana.setWindowIcon(QIcon("Help.png"))
            Texto=QTextEdit(Ventana)
            Texto.move(10,10)
            Texto.resize(470,470)
            Texto.setText("Bienvenido a la ayuda de VideoPL")
            Texto.setAcceptRichText(True)
            Fuente=QFont("Code Bold",15)
            Fuente.setBold(True)
            Texto.setFont(Fuente)
            Texto.setAlignment(Qt.AlignCenter)
            Texto.setCurrentFont(QFont("Consolas",10))
            Texto.append("Para el correcto funcionamiento del reproductor se deben instalar los codecs K-Lite tal y como pone en el apartado acerca de, para el resto de problemas consulte a google :).")
            Texto.append("Gracias por usar mi reproductor")
            Texto.setReadOnly(True)
            Ventana.exec_()
        Ayuda.triggered.connect(Help)
        
        #AYUDA:BUSCAR ACTUALIZACIONES
        Actualizaciones=QAction("Buscar actualizaciones",self)
        Actualizaciones.setIcon(QIcon("actualizar.png"))
        menuAyuda.addAction(Actualizaciones)
        def Buscar():
            Ventana = QDialog()
            Ventana.setGeometry(600,500,500,50)
            Ventana.setWindowTitle('Buscar Actualizaciones')
            Ventana.setWindowIcon(QIcon("buscar.png"))
            progreso = QProgressBar(Ventana)
            progreso.setGeometry(75, 70, 400, 20)
            empezar=QPushButton("Empezar",Ventana)
            def empezar_progreso():
                Ventana.setWindowTitle("Buscando actualizaciones...")
                progreso.setRange(0,0)
                time.sleep(1)
                Mensaje=QMessageBox.critical(Ventana, 'Resultado', "No se encontraron actualizaciones", QMessageBox.Ok)
                Ventana.close()
            empezar.clicked.connect(empezar_progreso)
            layouts=QHBoxLayout()
            layouts.addWidget(empezar)
            layouts.addWidget(progreso)
            Ventana.setLayout(layouts)
            Ventana.exec_()
        menuAyuda.addSeparator()
        Actualizaciones.triggered.connect(Buscar)
        
        #AYUDA:ACERCA_DE
        Acerca=QAction("Acerca de ",self)
        Acerca.setIcon(QIcon("acerca.png"))
        menuAyuda.addAction(Acerca)
        Acerca.setShortcut("Shift+F1")
        
        def acerca():
            Ventana = QDialog()
            Label=QLabel()
            Label.setPixmap(QPixmap("ICON.png"))
            Label.setAlignment(Qt.AlignCenter)
            Layouts=QFormLayout()
            Ventana.setGeometry(600,300,300,350)
            Ventana.setWindowTitle('Acerca de')
            Ventana.setWindowIcon(QIcon("about.png"))
            Ventana.setLayout(Layouts)
            Texto=QLabel("VideoPL")
            Texto.setFont(QFont("Montserrat ExtraBold",20))
            Texto2=QLabel("Este reproductor esta hecho con la mejor calidad posible, si alguno encuentra algun error o algo a mejorar sientase libre de hacerlo.")
            Texto3=QLabel("Es gratuito y de codigo abierto debido a las numerosas personas que contribuiran en este proyecto")
            Texto4=QLabel("Lee los formatos tanto de video como de audio mas usados")
            Texto5=QLabel("Para el correcto funcionamiento del reproductor es necesario instalar los siguientes codecs de video:")
            Texto6=QLabel("<a href=\"https://codecguide.com/download_kl.htm\">K-Lite</a>")
            Texto6.setOpenExternalLinks(True)
            Texto.setAlignment(Qt.AlignCenter)
            Texto2.setAlignment(Qt.AlignJustify)
            Texto3.setAlignment(Qt.AlignJustify)
            Texto4.setAlignment(Qt.AlignJustify)
            Texto5.setAlignment(Qt.AlignJustify)
            Texto6.setAlignment(Qt.AlignJustify)
            Layouts.addRow(Texto)
            Layouts.addRow(Texto2)
            Layouts.addRow(Texto3)
            Layouts.addRow(Texto4)
            Layouts.addRow(Texto5)
            Layouts.addRow(Texto6)
            Layouts.addRow(Label)
            Ventana.exec_()
        Acerca.triggered.connect(acerca)
        self.show()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())