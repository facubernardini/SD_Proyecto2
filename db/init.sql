USE consorcio;

CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
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

#-- Contiene todas las noticias de las ultimas 24 hs 
CREATE VIEW vista_noticias_ultimas_24hs AS
SELECT 
    n.id_noticia,
    n.titulo,
    n.contenido,
    n.time_stamp,
    c.nombre AS cliente,
    cat.nombre AS categoria
FROM noticias n
LEFT JOIN clientes c ON n.id_cliente = c.id_cliente
LEFT JOIN categorias cat ON n.id_categoria = cat.id_categoria
WHERE n.time_stamp >= NOW() - INTERVAL 1 DAY;

#-- Contiene todas las categorias a las que se suscribio el cliente
CREATE VIEW vista_categorias_por_cliente AS
SELECT 
    cc.id_cliente,
    c.id_categoria,
    c.nombre AS categoria
FROM cliente_categoria cc
JOIN categorias c ON cc.id_categoria = c.id_categoria;
