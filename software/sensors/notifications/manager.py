"""
LUXX HAUS Notification Manager
Handles alerts via multiple channels: push, SMS, email, voice.
"""

from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from loguru import logger

from ..core import AlertSeverity, EventType, get_config, get_event_bus, on_event


@dataclass
class Notification:
    """Represents a notification to be sent."""

    title: str
    message: str
    severity: AlertSeverity
    channel: str
    recipient: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


class NotificationChannel(ABC):
    """Abstract base class for notification channels."""

    def __init__(self, name: str, enabled: bool = True):
        self.name = name
        self.enabled = enabled

    @abstractmethod
    async def send(self, notification: Notification) -> bool:
        """Send a notification. Returns True if successful."""
        pass

    def is_available(self) -> bool:
        """Check if channel is configured and available."""
        return self.enabled


class PushNotificationChannel(NotificationChannel):
    """Firebase Cloud Messaging push notifications."""

    def __init__(
        self,
        credentials_path: Optional[str] = None,
        default_topic: str = "luxx_haus_alerts",
    ):
        config = get_config().notifications.push
        super().__init__("push", config.enabled)
        
        self.credentials_path = credentials_path or config.firebase_credentials_path
        self.default_topic = default_topic or config.default_topic
        self._initialized = False
        
        if self.enabled and self.credentials_path:
            self._init_firebase()

    def _init_firebase(self) -> None:
        """Initialize Firebase Admin SDK."""
        try:
            import firebase_admin
            from firebase_admin import credentials
            
            if not firebase_admin._apps:
                cred = credentials.Certificate(self.credentials_path)
                firebase_admin.initialize_app(cred)
                self._initialized = True
                logger.info("Firebase initialized for push notifications")
        except ImportError:
            logger.warning("firebase-admin not installed")
            self.enabled = False
        except Exception as e:
            logger.error(f"Firebase init failed: {e}")
            self.enabled = False

    async def send(self, notification: Notification) -> bool:
        """Send push notification via Firebase."""
        if not self.enabled or not self._initialized:
            logger.debug(f"Push notifications disabled, skipping: {notification.title}")
            return False
        
        try:
            from firebase_admin import messaging
            
            # Build message
            message = messaging.Message(
                notification=messaging.Notification(
                    title=notification.title,
                    body=notification.message,
                ),
                data={
                    "severity": notification.severity.value,
                    "timestamp": notification.timestamp.isoformat(),
                    **(notification.data or {}),
                },
                topic=self.default_topic,
            )
            
            # Send asynchronously
            response = await asyncio.to_thread(messaging.send, message)
            logger.info(f"Push notification sent: {response}")
            return True
            
        except Exception as e:
            logger.error(f"Push notification failed: {e}")
            return False

    def is_available(self) -> bool:
        return self.enabled and self._initialized


class SMSNotificationChannel(NotificationChannel):
    """Twilio SMS notifications."""

    def __init__(
        self,
        account_sid: Optional[str] = None,
        auth_token: Optional[str] = None,
        from_number: Optional[str] = None,
    ):
        config = get_config().notifications.sms
        super().__init__("sms", config.enabled)
        
        self.account_sid = account_sid or config.twilio_account_sid
        self.auth_token = auth_token or config.twilio_auth_token
        self.from_number = from_number or config.from_number
        self._client = None
        
        if self.enabled and self.account_sid and self.auth_token:
            self._init_twilio()

    def _init_twilio(self) -> None:
        """Initialize Twilio client."""
        try:
            from twilio.rest import Client
            self._client = Client(self.account_sid, self.auth_token)
            logger.info("Twilio initialized for SMS notifications")
        except ImportError:
            logger.warning("twilio not installed")
            self.enabled = False
        except Exception as e:
            logger.error(f"Twilio init failed: {e}")
            self.enabled = False

    async def send(self, notification: Notification) -> bool:
        """Send SMS via Twilio."""
        if not self.enabled or not self._client:
            logger.debug(f"SMS disabled, skipping: {notification.title}")
            return False
        
        if not notification.recipient:
            logger.warning("No recipient for SMS notification")
            return False
        
        try:
            # Format message (SMS has character limits)
            body = f"🏠 LUXX HAUS: {notification.title}\n{notification.message}"
            if len(body) > 160:
                body = body[:157] + "..."
            
            message = await asyncio.to_thread(
                self._client.messages.create,
                body=body,
                from_=self.from_number,
                to=notification.recipient,
            )
            
            logger.info(f"SMS sent: {message.sid}")
            return True
            
        except Exception as e:
            logger.error(f"SMS failed: {e}")
            return False

    def is_available(self) -> bool:
        return self.enabled and self._client is not None


class EmailNotificationChannel(NotificationChannel):
    """Email notifications via SMTP or SendGrid."""

    def __init__(
        self,
        smtp_host: Optional[str] = None,
        smtp_port: Optional[int] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        from_address: Optional[str] = None,
    ):
        config = get_config().notifications.email
        super().__init__("email", config.enabled)
        
        self.smtp_host = smtp_host or config.smtp_host
        self.smtp_port = smtp_port or config.smtp_port
        self.username = username or config.smtp_username
        self.password = password or config.smtp_password
        self.from_address = from_address or config.from_address

    async def send(self, notification: Notification) -> bool:
        """Send email notification."""
        if not self.enabled:
            logger.debug(f"Email disabled, skipping: {notification.title}")
            return False
        
        if not notification.recipient:
            logger.warning("No recipient for email notification")
            return False
        
        try:
            import aiosmtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            # Build email
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"🏠 LUXX HAUS Alert: {notification.title}"
            msg["From"] = self.from_address
            msg["To"] = notification.recipient
            
            # Plain text version
            text = f"""
LUXX HAUS Alert
===============

{notification.title}

{notification.message}

Severity: {notification.severity.value.upper()}
Time: {notification.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

---
This is an automated alert from your LUXX HAUS smart home protection system.
            """
            
            # HTML version
            severity_colors = {
                AlertSeverity.INFO: "#3498db",
                AlertSeverity.WARNING: "#f39c12",
                AlertSeverity.DANGER: "#e67e22",
                AlertSeverity.CRITICAL: "#e74c3c",
            }
            color = severity_colors.get(notification.severity, "#333")
            
            html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .alert-box {{ 
            border-left: 4px solid {color}; 
            padding: 15px; 
            margin: 20px 0;
            background: #f9f9f9;
        }}
        .severity {{ 
            display: inline-block;
            padding: 4px 8px;
            background: {color};
            color: white;
            border-radius: 4px;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <h2>🏠 LUXX HAUS Alert</h2>
    <div class="alert-box">
        <h3>{notification.title}</h3>
        <p>{notification.message}</p>
        <p>
            <span class="severity">{notification.severity.value.upper()}</span>
            <small style="margin-left: 10px; color: #666;">
                {notification.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
            </small>
        </p>
    </div>
    <hr>
    <p style="color: #999; font-size: 12px;">
        This is an automated alert from your LUXX HAUS smart home protection system.
    </p>
</body>
</html>
            """
            
            msg.attach(MIMEText(text, "plain"))
            msg.attach(MIMEText(html, "html"))
            
            # Send
            await aiosmtplib.send(
                msg,
                hostname=self.smtp_host,
                port=self.smtp_port,
                username=self.username,
                password=self.password,
                start_tls=True,
            )
            
            logger.info(f"Email sent to {notification.recipient}")
            return True
            
        except ImportError:
            logger.warning("aiosmtplib not installed")
            return False
        except Exception as e:
            logger.error(f"Email failed: {e}")
            return False


class NotificationManager:
    """
    Central notification manager.
    
    Handles routing alerts to appropriate channels based on severity
    and user preferences.
    """

    def __init__(self):
        self.channels: Dict[str, NotificationChannel] = {}
        self.contacts: List[Dict[str, Any]] = []
        
        # Load configuration
        config = get_config()
        
        # Initialize channels
        self.channels["push"] = PushNotificationChannel()
        self.channels["sms"] = SMSNotificationChannel()
        self.channels["email"] = EmailNotificationChannel()
        
        # Load emergency contacts
        for contact in config.emergency_contacts:
            self.contacts.append({
                "name": contact.name,
                "phone": contact.phone,
                "email": contact.email,
                "notify_on": [s.value for s in contact.notify_on],
            })
        
        # Subscribe to alert events
        self._setup_event_handlers()
        
        logger.info(
            f"NotificationManager initialized with channels: "
            f"{[c for c, ch in self.channels.items() if ch.is_available()]}"
        )

    def _setup_event_handlers(self) -> None:
        """Subscribe to relevant events."""
        event_bus = get_event_bus()
        event_bus.subscribe(EventType.ALERT_TRIGGERED, self._handle_alert_event)

    async def _handle_alert_event(self, event) -> None:
        """Handle incoming alert events."""
        data = event.data
        severity = AlertSeverity(data.get("severity", "warning"))
        
        await self.send_alert(
            title=f"{data.get('sensor_type', 'Sensor').replace('_', ' ').title()} Alert",
            message=data.get("message", "Alert triggered"),
            severity=severity,
        )

    async def send_alert(
        self,
        title: str,
        message: str,
        severity: AlertSeverity,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, bool]:
        """
        Send alert through appropriate channels based on severity.
        
        Returns dict of channel -> success status.
        """
        config = get_config().notifications
        results = {}
        
        # Determine channels based on severity
        if severity == AlertSeverity.CRITICAL:
            channel_names = config.critical_channels
        elif severity == AlertSeverity.DANGER:
            channel_names = config.danger_channels
        else:
            channel_names = config.warning_channels
        
        # Send to each channel
        for channel_name in channel_names:
            channel = self.channels.get(channel_name)
            if not channel or not channel.is_available():
                continue
            
            # For SMS/email, send to each contact
            if channel_name in ["sms", "email"]:
                for contact in self.contacts:
                    # Check if contact wants this severity
                    if severity.value not in contact.get("notify_on", []):
                        continue
                    
                    recipient = (
                        contact.get("phone") if channel_name == "sms"
                        else contact.get("email")
                    )
                    
                    if recipient:
                        notification = Notification(
                            title=title,
                            message=message,
                            severity=severity,
                            channel=channel_name,
                            recipient=recipient,
                            data=data,
                        )
                        success = await channel.send(notification)
                        results[f"{channel_name}:{contact['name']}"] = success
            else:
                # Push notifications go to topic
                notification = Notification(
                    title=title,
                    message=message,
                    severity=severity,
                    channel=channel_name,
                    data=data,
                )
                results[channel_name] = await channel.send(notification)
        
        logger.info(f"Alert sent via channels: {results}")
        return results

    async def send_test_notification(self) -> Dict[str, bool]:
        """Send a test notification to verify all channels."""
        return await self.send_alert(
            title="Test Notification",
            message="This is a test from LUXX HAUS. All systems operational.",
            severity=AlertSeverity.INFO,
        )

    def add_contact(
        self,
        name: str,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        notify_on: Optional[List[AlertSeverity]] = None,
    ) -> None:
        """Add an emergency contact."""
        self.contacts.append({
            "name": name,
            "phone": phone,
            "email": email,
            "notify_on": [s.value for s in (notify_on or [AlertSeverity.CRITICAL])],
        })
        logger.info(f"Added contact: {name}")

    def get_status(self) -> Dict[str, Any]:
        """Get notification system status."""
        return {
            "channels": {
                name: {
                    "enabled": ch.enabled,
                    "available": ch.is_available(),
                }
                for name, ch in self.channels.items()
            },
            "contacts": len(self.contacts),
        }


# Singleton instance
_notification_manager: Optional[NotificationManager] = None


def get_notification_manager() -> NotificationManager:
    """Get the notification manager instance."""
    global _notification_manager
    if _notification_manager is None:
        _notification_manager = NotificationManager()
    return _notification_manager
