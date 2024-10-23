DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS scraper_data;
DROP TABLE IF EXISTS user_scraper;

-- Tabla de usuarios
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

-- Tabla de posts (puedes adaptarla para los scrapers si decides usar posts)
CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

-- Tabla para almacenar los datos scrapeados
CREATE TABLE scraper_data (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  scraper_id INTEGER NOT NULL, -- Identificador del scraper (1, 2 o 3)
  title TEXT NOT NULL,
  url TEXT NOT NULL,
  content TEXT, -- Opcional, puedes almacenar contenido adicional si es necesario
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabla intermedia para usuarios y los scrapers que siguen
CREATE TABLE user_scraper (
  user_id INTEGER NOT NULL,
  scraper_id INTEGER NOT NULL,
  PRIMARY KEY (user_id, scraper_id),
  FOREIGN KEY (user_id) REFERENCES user (id),
  FOREIGN KEY (scraper_id) REFERENCES scraper_data (scraper_id)
);
