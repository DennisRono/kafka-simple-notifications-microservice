# Event-Driven Microservices System

## Overview

This project implements an event-driven microservices architecture using FastAPI, Redis, and Docker. It consists of three main services:

1. **Producer Service**: Generates and sends events.
2. **Consumer Service**: Receives and processes events.
3. **Notification Service**: Sends email notifications based on events.

The system uses Redis as a message broker to facilitate communication between services.

## Project Structure

```
event-driven-system/
├── producer/
│   ├── main.py
│   └── Dockerfile
├── consumer/
│   ├── main.py
│   └── Dockerfile
├── notification/
│   ├── main.py
│   └── Dockerfile
├── docker-compose.yml
├── .env
└── README.md
```

## Prerequisites

- Docker
- Docker Compose

## Setup and Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/DennisRono/kafka-simple-notifications-microservice.git
   cd kafka-simple-notifications-microservice
   ```

2. **Create a `.env` file** in the root directory with the following content:

   ```ini
   REDIS_HOST=redis
   REDIS_PORT=6379
   NOTIFICATION_SERVICE_URL=http://notification:8002
   SMTP_SERVER=smtp.example.com
   SMTP_PORT=587
   SMTP_USERNAME=your_username
   SMTP_PASSWORD=your_password
   FROM_EMAIL=noreply@example.com
   ```

   Replace the SMTP and email settings with your actual values.

3. **Build and run the services:**
   ```sh
   docker-compose up --build
   ```

## Usage

Once the services are up and running, you can interact with the system as follows:

1. **Send an event:**

   ```sh
   curl -X POST http://localhost:8000/send-event \
        -H "Content-Type: application/json" \
        -d '{"topic": "email_notifications", "message": {"to_email": "user@example.com", "subject": "Test Notification", "body": "This is a test notification."}}'
   ```

2. The **Consumer Service** will automatically process the event and forward it to the **Notification Service**.
3. The **Notification Service** will attempt to send an email based on the event data.

## Service Details

### Producer Service (Port 8000)

- **Endpoint**: `POST /send-event`
- Accepts a JSON payload with `topic` and `message`.
- Publishes the event to Redis.

### Consumer Service (Port 8001)

- Subscribes to Redis channels.
- Processes incoming events.
- Forwards events to the Notification Service.

### Notification Service (Port 8002)

- **Endpoint**: `POST /send-notification`
- Accepts a JSON payload with `to_email`, `subject`, and `body`.
- Sends emails using the configured SMTP server.

## Development

To modify or extend the services:

1. Update the respective `main.py` files in each service directory.
2. Rebuild the Docker images:
   ```sh
   docker-compose up --build
   ```

## Troubleshooting

- If services fail to start, check the Docker logs:
  ```sh
  docker-compose logs
  ```
- Ensure all environment variables in the `.env` file are correctly set.
- Verify that the SMTP server settings are correct and that the server is accessible.

## Contributing

Please read `CONTRIBUTING.md` for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.
