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
        URL = "https://vandal.elespanol.com/juegos/0/videojuegos"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        rows = soup.find_all("tr")

        platform_keywords = ["PC", "PS4", "Xbox", "Switch", "PlayStation", "Nintendo", "Steam", "Series X", "One"]
        games = []
        for row in rows:
            title_element = row.find("a", title=True)
            platform_elements = row.find_all("span")
            platforms = []

            for platform in platform_elements:
                platform_text = platform.text.strip()
                if any(keyword in platform_text for keyword in platform_keywords):
                    platforms.append(platform_text)

            if title_element:
                title = title_element.text.strip()
                link = title_element['href']
                platforms = ', '.join(platforms)
                
                games.append({
                    'title': title,
                    'platforms': platforms,
                    'link': f"https://vandal.elespanol.com{link}"
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
