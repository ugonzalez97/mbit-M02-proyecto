# Usar la imagen base de Python 3.11
FROM python:3.11

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el código fuente de la carpeta actual al directorio de trabajo
COPY . /app

# Instalar las dependencias desde el archivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto en el que el servidor WSGI estará escuchando
EXPOSE 8080

# Ejecutar el servidor WSGI utilizando Waitress
CMD ["waitress-serve", "--listen=0.0.0.0:8080", "app:views"]