# Flower AI Bot

### Flow

- at the moment only Admin Mode Flow is fully functional. You can enter a password in the chat and further communicate with the neuron network as an admin, create, delete, update and read Flower model data. To exit Admin Mode you need to enter the password again

### INSTALLATION

- Copy this repository to your system

```
git clone https://github.com/VyacheslavShrot/FlowerAIBot.git
```

- Create an .env file at the project level

```
# Config for Database
MYSQL_ROOT_PASSWORD=admin
MYSQL_DATABASE=admin
MYSQL_USER=admin
MYSQL_PASSWORD=admin

# For TG WebHook
HTTPS_URL=https://026f-193-28-84-64.ngrok-free.app

# Telegram Token
TELEGRAM_BOT_TOKEN=7114...

# For Enable in Chat with Bot Admin Mode
ADMIN_PASSWORD=5543

OPENAI_API_KEY=sk-pro...
```

- Give permissions to the directory
```
chmod +x commands/wait_for_db.sh
```

### START

- Run ngrok for Working TG WebHook with Https

```
ngrok http 8080
```

- Run Docker-Compose

```
docker-compose up -d --build
```
