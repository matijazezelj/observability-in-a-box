import asyncio
import json
import random
import time
from nats.aio.client import Client as NATS

# Configuration
NATS_URL = "nats://localhost:4222"        # Adjust if NATS server is at a different host or port
SUBJECT = "logs"                          # Subject Vector listens to in your vector.toml

# Some example log levels and apps for variety
LOG_LEVELS = ["INFO", "WARN", "ERROR", "DEBUG"]
APPS = ["webserver", "database", "auth-service", "payment-gateway"]

async def run():
    nc = NATS()
    await nc.connect(servers=[NATS_URL])

    print(f"Connected to NATS at {NATS_URL} - sending logs to subject '{SUBJECT}'")

    try:
        while True:
            # Compose a log message with some random values
            log_event = {
                "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                "level": random.choice(LOG_LEVELS),
                "app": random.choice(APPS),
                "host": "host1",
                "message": "Test log message",
                "request_id": f"{random.randint(1000, 9999)}"
            }

            payload = json.dumps(log_event).encode()
            await nc.publish(SUBJECT, payload)
            await nc.flush()  # Ensure message is sent immediately

            print(f"Sent: {log_event}")

            await asyncio.sleep(1)  # Send a log message every second

    except asyncio.CancelledError:
        pass
    finally:
        await nc.drain()

if __name__ == '__main__':
    asyncio.run(run())

