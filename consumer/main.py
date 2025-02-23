import os
from fastapi import FastAPI
from confluent_kafka import Consumer, KafkaError
import json
import requests
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Kafka consumer configuration
consumer_config = {
    "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    "group.id": "event_consumer_group",
    "auto.offset.reset": "earliest",
}

consumer = Consumer(consumer_config)

# Subscribe to topics
consumer.subscribe(["email_notifications"])

notification_service_url = os.getenv("NOTIFICATION_SERVICE_URL")


@app.on_event("startup")
async def startup_event():
    # Start consuming messages in a background task
    import asyncio

    asyncio.create_task(consume_messages())


async def consume_messages():
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Error: {msg.error()}")
                continue

        try:
            event_data = json.loads(msg.value().decode("utf-8"))
            # Forward the event to the notification service
            response = requests.post(
                f"{notification_service_url}/send-notification", json=event_data
            )
            response.raise_for_status()
            print(f"Event processed and forwarded: {event_data}")
        except Exception as e:
            print(f"Error processing event: {str(e)}")


@app.get("/")
async def root():
    return {"message": "Consumer service is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
