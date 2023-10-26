import os

from dotenv import load_dotenv

load_dotenv()

RMQ_URL = os.environ.get("RMQ_URL", "amqp://rmuser:rmpassword@rabbitmq:5672")
REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/0")