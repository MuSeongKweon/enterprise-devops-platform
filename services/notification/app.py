# notification_service.py
import redis

#r = redis.Redis(host='host.docker.internal', port=6379)
r = redis.Redis(host='redis-master',port=6379)

pubsub = r.pubsub()

pubsub.subscribe("payment")

print("[Notification] Waiting for messages...", flush=True)

for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"[Notification] Received: {message['data'].decode()}", flush=True)
