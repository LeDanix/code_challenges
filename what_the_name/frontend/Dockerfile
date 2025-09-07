# Node 20
FROM node:20

WORKDIR /app

# Copiamos package.json y package-lock.json
COPY package*.json ./

# Instalamos dependencias
RUN npm install

# Copiamos todo el frontend
COPY . .

# Exponemos el puerto de desarrollo de Vite
EXPOSE 5173

# Comando para levantar la app
CMD ["npm", "run", "dev", "--", "--host"]
