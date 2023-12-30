FROM node:18-slim
WORKDIR /usr/src/app


#COPY package*.json .

# Copy your media.
#COPY media ./media

# Copy your public files.
#COPY public ./public

COPY . .

# Run npm install.
RUN npm install

# Build assets.
#RUN npm run build

#EXPOSE 80
CMD ["npm", "run", "dev"]