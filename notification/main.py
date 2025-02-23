import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


class EmailNotification(BaseModel):
    to_email: str
    subject: str
    body: str


@app.post("/send-notification")
async def send_notification(notification: EmailNotification):
    try:
        # Email configuration
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_port = int(os.getenv("SMTP_PORT"))
        smtp_username = os.getenv("SMTP_USERNAME")
        smtp_password = os.getenv("SMTP_PASSWORD")
        from_email = os.getenv("FROM_EMAIL")

        # Create the email message
        message = MIMEMultipart()
        message["From"] = from_email
        message["To"] = notification.to_email
        message["Subject"] = notification.subject
        message.attach(MIMEText(notification.body, "plain"))

        # Send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(message)

        return {"status": "success", "message": "Notification sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"message": "Notification service is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8002)
