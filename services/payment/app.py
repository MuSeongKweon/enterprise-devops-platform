# payment_service.py
import redis
import time

#r = redis.Redis(host='host.docker.internal', port=6379)
r = redis.Redis(host='redis-master',port=6379)

while True:
    message = "payment completed"
    r.publish("payment", message)
    print(f"[Payment] Sent: {message}", flush=True)
    time.sleep(5)
