FROM node:20-alpine

WORKDIR /app

# Install dependencies first for Docker caching
COPY package.json package-lock.json* ./
RUN npm install

# Copy all files
COPY . .

# Build the Next.js app
RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "start"]
