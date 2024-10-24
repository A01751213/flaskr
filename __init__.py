import os
from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

def create_app(test_config=None):
    # Crear y configurar la aplicación
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # Cargar la configuración de la instancia, si existe, cuando no esté en pruebas
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Cargar la configuración de pruebas si se pasa
        app.config.from_mapping(test_config)

    # Asegurarse de que la carpeta de instancias exista
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Ruta que ejecuta el scraper y muestra los resultados
    @app.route('/')
    def index():
        # Paso 1: Hacer la solicitud a la página web
        URL = "https://vandal.elespanol.com/juegos/0/videojuegos"
        page = requests.get(URL)

        # Paso 2: Parsear el HTML de la página
        soup = BeautifulSoup(page.content, "html.parser")

        # Paso 3: Encontrar los elementos que contienen la información
        rows = soup.find_all("tr")

        # Lista de palabras clave que pueden representar plataformas de videojuegos
        platform_keywords = ["PC", "PS4", "Xbox", "Switch", "PlayStation", "Nintendo", "Steam", "Series X", "One"]

        # Paso 4: Buscar y extraer la información de cada videojuego
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

        # Renderizar la plantilla HTML y pasar la lista de juegos
        return render_template('blog/index.html', games=games)

    # Simple route to say hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
