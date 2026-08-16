import logging
import os

import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings
from django.db.models import Q

from accounts.models import User, UserFCMToken, NotificationLog
from store.models import Notification

logger = logging.getLogger(__name__)


# ==============================================================================
# 1. Firebase Initialisation
# ==============================================================================
FIREBASE_KEY_PATH = os.path.join(settings.BASE_DIR, 'firebase-key.json')

if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(FIREBASE_KEY_PATH)
        firebase_admin.initialize_app(cred)
        logger.info("Firebase Admin SDK initialised successfully.")
    except Exception as e:
        logger.warning("Firebase Admin SDK could not be initialised: %s", e)


# ==============================================================================
# 2. In-App Notifications
# ==============================================================================

def send_notification(user, title, message, link=None):
    """Create an in-app notification record for a single user."""
    if user and user.is_authenticated:
        Notification.objects.create(
            recipient=user,
            title=title,
            message=message,
            link=link,
        )


def notify_admins(title, message, link=None):
    """Broadcast an in-app notification to all admin-level users."""
    admins = User.objects.filter(
        Q(is_superuser=True) | Q(role__in=['ADMIN_LVL2', 'ADMIN_LVL3', 'COUNTRY_ADMIN', 'OWNER'])
    )
    notifications = [
        Notification(recipient=admin, title=title, message=message, link=link)
        for admin in admins
    ]
    if notifications:
        Notification.objects.bulk_create(notifications)


# ==============================================================================
# 3. Firebase Push Notifications
# ==============================================================================

def send_push_to_user(user, title, body):
    """
    Send a push notification to all FCM-registered devices of a user.
    Returns True if at least one message was delivered successfully.
    """
    try:
        user_tokens = list(
            UserFCMToken.objects.filter(user=user).values_list('token', flat=True)
        )

        if not user_tokens:
            logger.debug("User '%s' has no registered FCM tokens. Skipping push.", user.username)
            return False

        messages_list = [
            messaging.Message(
                notification=messaging.Notification(title=title, body=body),
                android=messaging.AndroidConfig(
                    priority='high',
                    notification=messaging.AndroidNotification(
                        channel_id='high_importance_channel',
                        sound='default',
                    ),
                ),
                token=token,
            )
            for token in user_tokens
        ]

        response = messaging.send_each(messages_list)

        # Purge stale tokens
        if response.failure_count > 0:
            for i, res in enumerate(response.responses):
                if not res.success:
                    dead_token = user_tokens[i]
                    UserFCMToken.objects.filter(token=dead_token).delete()
                    logger.info("Removed expired FCM token for user '%s'.", user.username)

        if response.success_count > 0:
            NotificationLog.objects.create(
                user=user, title=title, status="Success",
                details=f"Delivered to {response.success_count} device(s).",
            )
            return True

        NotificationLog.objects.create(
            user=user, title=title, status="Failed",
            details="All send attempts failed. Tokens may be stale.",
        )
        return False

    except Exception as e:
        logger.error("Error sending push notification to user '%s': %s", user.username, e)
        NotificationLog.objects.create(
            user=user, title=title, status="Error", details=str(e)
        )
        return False