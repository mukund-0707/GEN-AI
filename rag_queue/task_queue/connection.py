import os
from redis import Redis
from rq import Queue

redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", "6379"))
queue = Queue(connection=Redis(host=redis_host, port=redis_port))
