import os
from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        # Scrape Vicente
        # URL de la página web
        URL = "https://www.lavanguardia.com/andro4all/juegos/mejores-juegos-android-multijugador"
        page = requests.get(URL)

        # Verificar el estado de la solicitud
        if page.status_code == 200:
            print("Conexión exitosa")
        else:
            print(f"Error en la conexión: {page.status_code}")

        # Parsear el HTML de la página
        soup = BeautifulSoup(page.content, "html.parser")

        # Buscar todas las entradas de los juegos
        # Buscaremos los títulos con un enfoque en las etiquetas 'h2' o 'h3' que rodean los títulos de juegos y sus enlaces
        game_elements = soup.find_all("h3")

        # Lista para almacenar la información de los juegos
        games = []

        # Extraer el título y el enlace más cercano
        for game in game_elements:
            title = game.get_text(strip=True)

            # Buscar el enlace en el contenedor más cercano a los títulos (ej. etiqueta 'a' alrededor o cercana)
            link_tag = game.find_next("a")
            link = link_tag["href"] if link_tag else "No disponible"

            games.append({
                'title': title,
                'link': link
            })

    
        # Scrape Ignacio
        URL = "https://www.espinof.com/listas/mejores-peliculas-netflix-2024"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        headlines_div = soup.find("div", id="headlines")
        post_items = headlines_div.find_all("li")

        movies = []
        for post in post_items:
            title_element = post.find("a")
            if title_element:
                title = title_element.text.strip()
                link = title_element['href']
                if not link.startswith("http"):
                    link = f"https://www.espinof.com{link}"

                date_element = post.find("time")
                date = date_element['datetime'] if date_element else "No disponible"

                movies.append({
                    'title': title,
                    'link': link,
                    'date': date
                })
        #Scrape EDU
        # Paso 1: Hacer la solicitud a la página web
        URL = "https://365comicsxyear.blogspot.com/2022/06/"
        page = requests.get(URL)

        # Paso 2: Parsear el HTML de la página
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="Blog1")

        # Buscar todas las entradas del blog
        posts = results.find_all("h3", class_="post-title entry-title")

        # Lista para almacenar la información de los cómics
        comics = []

        # Paso 4: Extraer y mostrar el título y la URL de cada entrada
        for post in posts:
            title = post.get_text(strip=True)
            link = post.find("a")["href"]

            comics.append({
                'title': title,
                'link': link
            })

        # Renderizar la plantilla HTML y pasar las listas de juegos y películas
        return render_template('blog/index.html', games=games, movies=movies, comics=comics)

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
