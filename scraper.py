from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    # Paso 1: Hacer la solicitud a la página web
    URL = "https://vandal.elespanol.com/juegos/0/videojuegos"
    page = requests.get(URL)

    # Paso 2: Parsear el HTML de la página
    soup = BeautifulSoup(page.content, "html.parser")

    # Paso 3: Encontrar los elementos que contienen la información que te interesa
    rows = soup.find_all("tr")

    # Lista de palabras clave que pueden representar plataformas de videojuegos
    platform_keywords = ["PC", "PS4", "Xbox", "Switch", "PlayStation", "Nintendo", "Steam", "Series X", "One", "PS5", "XBOne", "XSX", "Android", "Iphone"]

    # Lista para almacenar la información de los juegos
    games = []

    # Paso 4: Buscar y extraer la información de cada videojuego
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
            platforms = ', '.join(platforms)  # Unir las plataformas encontradas
            
            # Almacenar la información en la lista de juegos
            games.append({
                'title': title,
                'platforms': platforms,
                'link': f"https://vandal.elespanol.com{link}"
            })

    # Pasar los juegos a la plantilla HTML
    return render_template('base.html', games=games)

if __name__ == '__main__':
    app.run(debug=True)
