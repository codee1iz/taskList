FROM node:20-slim

WORKDIR /app

COPY package*.json ./

RUN npm install --legacy-peer-deps

COPY . .

RUN npm run build

COPY flag.txt /app/flag.txt

EXPOSE 3000

CMD ["npm", "start"]
