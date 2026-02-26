FROM node:22-alpine

WORKDIR /frontend

COPY /react-app/package.json .

#install everthing in package.json
RUN npm install

#Copy entire frontend directory to the container
COPY . .

WORKDIR /frontend/react-app

#Frontend runs on port 5173
EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]