import os
from flask import Flask, render_template, g
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
        # Si el usuario está logueado, obtenemos sus suscripciones
        if g.user:
            subscriptions = g.user['subscription'].split(',') if g.user['subscription'] else []
        else:
            subscriptions = []

        games, movies, comics = [], [], []

        # Scraping de videojuegos
        if not subscriptions or 'videojuegos' in subscriptions:
            URL = "https://www.lavanguardia.com/andro4all/juegos/mejores-juegos-android-multijugador"
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            game_elements = soup.find_all("h3")
            for game in game_elements:
                title = game.get_text(strip=True)
                link_tag = game.find_next("a")
                link = link_tag["href"] if link_tag else "No disponible"
                games.append({'title': title, 'link': link})

        # Scraping de películas
        if not subscriptions or 'peliculas' in subscriptions:
            URL = "https://www.espinof.com/listas/mejores-peliculas-netflix-2024"
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            headlines_div = soup.find("div", id="headlines")
            post_items = headlines_div.find_all("li")
            for post in post_items:
                title_element = post.find("a")
                if title_element:
                    title = title_element.text.strip()
                    link = title_element['href']
                    if not link.startswith("http"):
                        link = f"https://www.espinof.com{link}"
                    date_element = post.find("time")
                    date = date_element['datetime'] if date_element else "No disponible"
                    movies.append({'title': title, 'link': link, 'date': date})

        # Scraping de cómics
        if not subscriptions or 'comics' in subscriptions:
            URL = "https://365comicsxyear.blogspot.com/2022/06/"
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find(id="Blog1")
            posts = results.find_all("h3", class_="post-title entry-title")
            for post in posts:
                title = post.get_text(strip=True)
                link = post.find("a")["href"]
                comics.append({'title': title, 'link': link})

        return render_template('blog/index.html', games=games, movies=movies, comics=comics)


    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
