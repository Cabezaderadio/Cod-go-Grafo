import pandas as pd #dataframe
import networkx as nx #usada para la creación del grafo de una forma más sencilla
import matplotlib.pyplot as plt #ESTA LIBRERIA ES PARA LA CREACIÓN DE UN GRAFICO, SE USANN LABEL X,Y PARA LOS EJES Y OTRA PARA LOS TITULOS DEL GRAFICO
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QDesktopWidget
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt # Utiliza PyQt5 para la interfaz gráfica y se comunica con las funciones previamente definidas para mostrar películas recomendadas y manejar las selecciones del usuario.
from random import sample #Utilza para seleccionar 10 elementos aleatorios en la lista "sample". En este caso, movie_names es una lista que contiene los nombres de todas las películas en l_movies, y sample(movie_names, 10) selecciona aleatoriamente
#10 elementos de esa lista sin reemplazo. Estos 10 elementos representarán las películas que se mostrarán en la interfaz gráfica como parte de las recomendaciones.
import sys #usada en la lineas 211-215

#cada libreria se instala con pip (nombre libreria install)

df_movies = pd.read_excel('C:\\Users\\David\\Downloads\\Discretas\\Recomendaciones\\Listado\\Listado.xlsx')#ingresar dirección del excel en la carpeta del computador
g_movies = nx.Graph()#grafo


#creación del nodo
class Movie:

    def __init__(self, Nombre, CategoriaA, CategoriaB, Director, Año, castA, castB):

        self.Nombre = Nombre
        self.CategoriaA = CategoriaA
        self.CategoriaB = CategoriaB
        self.Director = Director
        self.Año = Año
        self.castA = castA
        self.castB = castB

    def imprimir_pelicula(self):

        print("Película:", self.Nombre)
        print("Categoría A:", self.CategoriaA)
        print("Categoría B:", self.CategoriaB)
        print("Director:", self.Director)
        print("Año:", self.Año)
        #

#Dataframe
l_movies = []
for index, row in df_movies.iterrows():

    #DATAFRAME SE USA LIBRERIA PANDA, LAS PALABRAS RESERVADAS AQUÍ SON LAS UTILIZADAS PARA LA CREACIÓN DE LAS COLUMNAS DEL DATAFRAME
    Nombre = row['Nombre']
    CategoriaA = row['CategoriaA']
    CategoriaB = row['CategoriaB']
    Director = row['Director']
    Año = row['Año']
    castA = row['CastA']
    castB = row['CastB']

    #CREACIÓN OBJETO
    movie_instance = Movie(Nombre, CategoriaA, CategoriaB, Director, Año, castA, castB)
    g_movies.add_node(movie_instance)
    l_movies.append(movie_instance)
#


#creación del grafo
for i in range(len(l_movies)): #LEN CONTAR NUMERO DE ELEMENTOS EN LA LISTA L_MOVIES

    current_movie = l_movies[i]

    for j in range(i + 1, len(l_movies)):

        next_movie = l_movies[j]

        weight = 0
        #contar similitudes
        #categorias
        if current_movie.CategoriaA == next_movie.CategoriaA or current_movie.CategoriaA == next_movie.CategoriaB:
            weight += 1
        if current_movie.CategoriaB == next_movie.CategoriaA or current_movie.CategoriaB == next_movie.CategoriaB:
            weight += 1
        #director
        if current_movie.Director == next_movie.Director:
            weight += 1
        #año
        if current_movie.Año == next_movie.Año:
            weight += 1
        #casting
        if current_movie.castA == next_movie.castA or current_movie.castA == next_movie.castB:
            weight += 1
        if current_movie.castB == next_movie.castA or current_movie.castB == next_movie.castB:
            weight += 1

        #aristas agregadas al grado g_movies, las aristas son el número (peso) de similitudes
        if weight == 1:
            g_movies.add_edge(current_movie, next_movie, weight=1)
        elif weight == 2:
            g_movies.add_edge(current_movie, next_movie, weight=2)
        elif weight == 3:
            g_movies.add_edge(current_movie, next_movie, weight=3)
        elif weight == 4:
            g_movies.add_edge(current_movie, next_movie, weight=4)

pos = nx.spring_layout(g_movies)  # Define una disposición para los nodos (puedes ajustar esto según tus preferencias)
labels = {movie: movie.Nombre for movie in l_movies}  # Etiquetas para los nodos

# Dibuja nodos y aristas
nx.draw(g_movies, pos, with_labels=False, font_weight='bold', node_size=50)
nx.draw_networkx_labels(g_movies, pos, labels, font_size=8)

plt.title('Grafo de Películas')
plt.show()


#TOMA DE ENTRADA LA PELICULA Y EL NÚMERO DE RECOMENDACIONES
def obtener_recomendaciones(pelicula, num_recomendaciones):

    vecinos = list(g_movies.neighbors(pelicula))
    pesos_similitud = {}

    for vecino in vecinos:

        peso = g_movies[pelicula][vecino]['weight']
        pesos_similitud[vecino] = peso

    vecinos_ordenados = sorted(pesos_similitud, key = pesos_similitud.get, reverse=True)
    recomendaciones = vecinos_ordenados[:num_recomendaciones]
#DECUELVE UNA LISTA DE RECOMENDACIONES SIMILARES A LA PELICULA DADA, DEVUELVE ORDENADAS POR SIMILITUD (ENCARGADA LA PALABRA RESERVADA SORTED Y REVERSE = TRUE)
    return recomendaciones

#interfaz o ventana principal en el sistema de recomendación de pelicula
class MainWindow(QMainWindow):
    #contrustor principal de la ventana principal
    def __init__(self):
        super().__init__()

        self.setWindowTitle("¿Qué película deseas ver?")
        self.movie_labels = []
        self.selected_movie = None
        self.create_movie_labels()
        self.create_subtitle()
        central_widget = QWidget(self)
        layout = QVBoxLayout()
        layout.addWidget(self.subtitle_label, alignment=Qt.AlignTop | Qt.AlignLeft)
        rows = [self.movie_labels[i:i + 5] for i in range(0, len(self.movie_labels), 5)]
        for row in rows:
            row_layout = QHBoxLayout()
            for widget in row:
                row_layout.addWidget(widget)
            layout.addLayout(row_layout)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.resize(1000, 600)
    
    #Este es el método de inicialización de la clase. Aquí se establece el título de la ventana, se inicializan variables (movie_labels y selected_movie),
    #y se llaman a otros métodos para crear etiquetas de películas y subtítulos. También se configura el diseño de la ventana 
    # mediante un QVBoxLayout que contiene etiquetas de películas organizadas en filas y columnas.



#crea las etiquetas de las películas y las organiza en una lista (movie_labels). Utiliza nombres de películas aleatorias seleccionadas mediante sample
#y crea etiquetas que incluyen la imagen de la película y el nombre

    def create_movie_labels(self):
        movie_Nombres = [movie.Nombre for movie in l_movies]
        selected_movies = sample(movie_Nombres, 10)
        for movie_Nombre in selected_movies:
            image_path = f"C:\\Users\\David\\Downloads\\Discretas\\Recomendaciones\\Fotos de cartelera\\{movie_Nombre}.jpg"# tenemos de nuevo que buscar las imagenes de las peliculas, tuto en youtube
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(185, 285, Qt.AspectRatioMode.KeepAspectRatio)
            movie_label = QLabel(self)
            movie_label.setPixmap(pixmap)
            movie_label.setAlignment(Qt.AlignCenter)
            movie_label.mousePressEvent = lambda event, movie=movie_Nombre: self.select_movie(movie)
            movie_Nombre_label = QLabel(self)
            movie_Nombre_label.setText(movie_Nombre)
            movie_Nombre_label.setAlignment(Qt.AlignCenter)
            movie_Nombre_label.setStyleSheet("font-size: 11pt;")

            layout = QVBoxLayout()
            layout.addWidget(movie_label)
            layout.addWidget(movie_Nombre_label)
            container_widget = QWidget()
            container_widget.setLayout(layout)
            self.movie_labels.append(container_widget)

#metodo que indica al usuario que debe seleccionar una pelicula
    def create_subtitle(self):
        self.subtitle_label = QLabel(self)
        self.subtitle_label.setText("Selecciona una Película:")
        self.subtitle_label.setFont(QFont("Times New Roman", 12, QFont.Bold))


# Este método imprime en la consola las recomendaciones para una película dada y
# luego llama al método mostrar_recomendaciones_imagenes para mostrar las imágenes de las películas recomendadas en la interfaz.
    def mostrar_recomendaciones(self, movie):

        num_recomendaciones = 10
        recomendaciones = obtener_recomendaciones(movie, num_recomendaciones)

        print("Recomendaciones para", movie.Nombre, ":")

        for recomendacion in recomendaciones:
            print(recomendacion.Nombre)

        self.mostrar_recomendaciones_imagenes(recomendaciones)


#Este método se ejecuta cuando se selecciona una película. Actualiza la película seleccionada y muestra las recomendaciones para esa película.
    def select_movie(self, movie_Nombre):

        self.selected_movie = movie_Nombre
        print("Película seleccionada:", movie_Nombre)
        selected_movie = next((movie for movie in l_movies if movie.Nombre == movie_Nombre), None)

        if selected_movie:
            self.mostrar_recomendaciones(selected_movie)
        else:
            print("No se encontró la película en la lista.")


#: Este método muestra las imágenes de las películas recomendadas en la interfaz gráfica.
# Organiza las imágenes en filas y columnas, y utiliza las imágenes de las películas recomendadas.
    def mostrar_recomendaciones_imagenes(self, recomendaciones):
        layout = QVBoxLayout()
        subtitle_label = QLabel(self)
        subtitle_label.setText("Películas Recomendadas:")
        subtitle_label.setFont(QFont("Times New Roman", 16, QFont.Bold))
        layout.addWidget(subtitle_label, alignment=Qt.AlignTop | Qt.AlignLeft)

        for i in range(0, len(recomendaciones), 5):
            row_layout = QHBoxLayout()
            for recomendacion in recomendaciones[i:i + 5]:
                container_widget = QWidget()
                container_layout = QVBoxLayout()
                image_path = f"C:\\Users\\David\\Downloads\\Discretas\\Recomendaciones\\Fotos de cartelera\\{recomendacion.Nombre}.jpg"
                pixmap = QPixmap(image_path)
                pixmap = pixmap.scaled(185, 285)
                movie_label = QLabel(self)  # Agregado para definir la etiqueta de la película
                movie_label.setPixmap(pixmap)
                movie_label.setAlignment(Qt.AlignCenter)               
                container_layout.addWidget(movie_label)
                movie_Nombre_label = QLabel(self)  # Agregado para definir la etiqueta del nombre de la película
                movie_Nombre_label.setText(recomendacion.Nombre)
                movie_Nombre_label.setAlignment(Qt.AlignCenter)
                movie_Nombre_label.setStyleSheet("font-size: 11pt;")
                container_layout.addWidget(movie_Nombre_label)
                
                container_widget.setLayout(container_layout)    
                row_layout.addWidget(container_widget)
            
            layout.addLayout(row_layout)
        
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())#sys.argv proporciona la lista de argumentos de la línea de comandos, y se usa para inicializar la aplicación y realizar la ejecución del programa mediante sys.exit(app.exec_()).
