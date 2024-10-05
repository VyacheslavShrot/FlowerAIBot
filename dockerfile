FROM python:3.11

WORKDIR /FlowerAIBot

# Copy Files
COPY . .

# Install Netcat
RUN apt-get update && apt-get install -y netcat-openbsd

# Install Packages
RUN pip install -r requirements.txt

# Set Permissions
RUN chmod +x commands/wait_for_db.sh

ENV CONFIG_PATH=/FlowerAIBot/web/config
#ENV APIS_PATH=/fast_api_mvc/apis

# Add Config and Apis Directories to PYTHONPATH
ENV PYTHONPATH="${CONFIG_PATH}:$PYTHONPATH"

CMD ["sh", "-c", "cd /FlowerAIBot && ./commands/wait_for_db.sh db 3306 -- alembic revision --autogenerate && alembic upgrade head && python3 run_web.py"]
