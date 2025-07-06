USE consorcio;

CREATE TABLE clientes (
  id_cliente INT PRIMARY KEY,
  password_cliente VARCHAR(255) NOT NULL,
  nombre VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL
);

CREATE TABLE categorias (
  id_categoria INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE noticias (
  id_noticia INT AUTO_INCREMENT PRIMARY KEY,
  titulo VARCHAR(255) NOT NULL,
  contenido TEXT NOT NULL,
  time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cliente_categoria (
  id_cliente INT,
  id_categoria INT,
  PRIMARY KEY (id_cliente, id_categoria),
  FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE,
  FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria) ON DELETE CASCADE
);

CREATE TABLE noticia_categoria (
  id_noticia INT,
  id_categoria INT,
  PRIMARY KEY (id_noticia, id_categoria),
  FOREIGN KEY (id_noticia) REFERENCES noticias(id_noticia) ON DELETE CASCADE,
  FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria) ON DELETE CASCADE
);

INSERT INTO clientes(id_cliente, password_cliente, nombre, email) VALUES (1, MD5('1234'), 'Juan', 'juan@consorcio.com');
INSERT INTO categorias(nombre) VALUES ('Policial'), ('Deportiva'), ('Finanzas');
INSERT INTO noticias(titulo, contenido) VALUES ('Noticia 1', 'Contenido 1'), ('Noticia 2', 'Contenido 2');

INSERT INTO noticia_categoria(id_noticia, id_categoria) VALUES (1, 1), (2, 2);