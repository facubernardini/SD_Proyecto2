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

CREATE TABLE cliente_categoria (
    id_cliente INT,
    id_categoria INT,
    PRIMARY KEY (id_cliente, id_categoria),

    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria) ON DELETE CASCADE
);

CREATE TABLE noticias (
    id_noticia INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    contenido TEXT NOT NULL,
    time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    id_cliente INT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE SET NULL,

    id_categoria INT,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria) ON DELETE SET NULL
);

#------------------ VISTAS ------------------#

#-- Ver todas las categorias disponibles
CREATE VIEW vista_categorias_disponibles AS
SELECT 
  id_categoria,
  nombre AS nombre_categoria
FROM categorias;

#-- Ver todas las noticias de las últimas 24 hs 
CREATE VIEW vista_noticias_ultimas_24hs AS
SELECT 
  n.id_noticia,
  n.titulo,
  n.contenido,
  n.time_stamp,
  cli.nombre AS cliente,
  cat.nombre AS categoria
FROM noticias n
LEFT JOIN clientes cli ON n.id_cliente = cli.id_cliente
LEFT JOIN categorias cat ON n.id_categoria = cat.id_categoria
WHERE n.time_stamp >= NOW() - INTERVAL 1 DAY;

#-- Ver todas las noticias que creó el cliente
CREATE VIEW vista_noticias_creadas_cliente AS
SELECT 
  n.id_noticia,
  n.titulo,
  n.contenido,
  n.time_stamp,
  cli.id_cliente,
  cli.nombre AS autor,
  cat.nombre AS nombre_categoria
FROM noticias n
LEFT JOIN clientes cli ON n.id_cliente = cli.id_cliente
LEFT JOIN categorias cat ON n.id_categoria = cat.id_categoria;

#-- Ver a que categorias está suscripto el cliente
CREATE VIEW vista_suscripciones_cliente AS
SELECT 
  cc.id_cliente,
  cat.id_categoria,
  cat.nombre AS categoria
FROM cliente_categoria cc
JOIN categorias cat ON cc.id_categoria = cat.id_categoria;

#-- Ver todas las noticias de las categorias a las que está suscripto el cliente
CREATE VIEW vista_noticias_para_cliente AS
SELECT 
  cc.id_cliente,
  n.id_noticia,
  n.titulo,
  n.contenido,
  n.time_stamp,
  cat.nombre AS categoria,
  cli.nombre AS autor
FROM cliente_categoria cc
JOIN noticias n ON cc.id_categoria = n.id_categoria
LEFT JOIN categorias cat ON n.id_categoria = cat.id_categoria
LEFT JOIN clientes cli ON n.id_cliente = cli.id_cliente;

#-- Ver las nuevas noticias (última hora)
CREATE VIEW vista_nuevas_noticias_para_enviar AS
SELECT 
  cc.id_cliente,
  cli.nombre AS nombre_cliente,
  cli.email,
  n.id_noticia,
  n.titulo,
  n.contenido,
  n.time_stamp,
  cat.nombre AS categoria
FROM noticias n
JOIN categorias cat ON n.id_categoria = cat.id_categoria
JOIN cliente_categoria cc ON n.id_categoria = cc.id_categoria
JOIN clientes cli ON cc.id_cliente = cli.id_cliente
WHERE n.time_stamp >= NOW() - INTERVAL 1 HOUR;


#------------------ DATOS DE PRUEBA ------------------#

INSERT INTO clientes(id_cliente, password_cliente, nombre, email) VALUES (41460004, MD5('prueba'), 'Facundo', 'prueba@hola.com');
INSERT INTO clientes(id_cliente, password_cliente, nombre, email) VALUES (41460005, MD5('prueba'), 'Pepe', 'prueba2@hola.com');
INSERT INTO clientes(id_cliente, password_cliente, nombre, email) VALUES (41460006, MD5('prueba'), 'Pablo', 'prueba3@hola.com');

INSERT INTO categorias(id_categoria, nombre) VALUES (1, 'Policial');
INSERT INTO categorias(id_categoria, nombre) VALUES (2, 'Deportiva');
INSERT INTO categorias(id_categoria, nombre) VALUES (3, 'Finanzas');

INSERT INTO cliente_categoria(id_cliente, id_categoria) VALUES (41460004, 1);
INSERT INTO cliente_categoria(id_cliente, id_categoria) VALUES (41460004, 2);
INSERT INTO cliente_categoria(id_cliente, id_categoria) VALUES (41460005, 2);
INSERT INTO cliente_categoria(id_cliente, id_categoria) VALUES (41460006, 3);

INSERT INTO noticias(titulo, contenido, id_cliente, id_categoria) VALUES ('Cientificos reviven al Diego', 'Segun fuentes de tiktok aseguran haber revivido al Diegote pero ahora patea con la derecha', 41460004, 2);
INSERT INTO noticias(titulo, contenido, id_cliente, id_categoria) VALUES ('Choque sobre ruta 3', 'Por la madrugada del lunes chocaron dos vehiculos. No se registraron heridos.', 41460004, 1);
INSERT INTO noticias(titulo, contenido, id_cliente, id_categoria) VALUES ('Vuela el dolar', 'El dolar toca los $23049 por unidad', 41460005, 3);
