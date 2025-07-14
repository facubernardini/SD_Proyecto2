si se utiliza la base de datos que crea el compose se deben ejecutar los siguientes pasos

# Levantar la base de datos, este comando tambien crea una red llamada sd_proyecto2_default
docker compose up

# Moverse a la carpeta asminAreas
cd suscribeCategoria

# Crear la imagen del servicio admin areas
docker build -t suscribecategoria . 

# Correr la imagen en un contenedor, -d levanta la imagen y la deja corriendo en segundo plano, -p mapea el puerto 50053, --name nombran el contenedor suscribecategoria, --network setea la red a utilizar sd_proyecto2_default, el ultimo parametro selecciona la imagen a correr
docker run -d -p 50053:50053 --name suscribecategoria --network sd_proyecto2_default suscribecategoria 