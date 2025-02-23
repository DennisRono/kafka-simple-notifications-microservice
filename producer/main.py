import os
from fastapi import FastAPI, HTTPException
from confluent_kafka import Producer
from pydantic import BaseModel
import json
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Kafka producer configuration
producer_config = {"bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS")}

producer = Producer(producer_config)


class Event(BaseModel):
    topic: str
    message: dict


@app.post("/send-event")
async def send_event(event: Event):
    try:
        producer.produce(
            event.topic,
            json.dumps(event.dict()).encode("utf-8"),
            callback=delivery_report,
        )
        producer.flush()
        return {"status": "success", "message": "Event sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
