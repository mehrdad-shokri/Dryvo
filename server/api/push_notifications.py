from server.error_handling import NotificationError

from pathlib import Path
import firebase_admin
from firebase_admin import credentials, messaging
from firebase_admin.project_management import ApiCallError
import json
from loguru import logger


def init_app(app):
    if not len(firebase_admin._apps):
        logger.debug("initializing firebase app")
        cred = credentials.Certificate(json.loads(app.config['FIREBASE_JSON']))
        firebase_admin.initialize_app(cred)


class FCM(object):
    @staticmethod
    def notify(token, title, body):
        message = messaging.Message(
            notification={
                'title': title,
                'body': body,
            },
            token=token,
        )
        try:
            messaging.send(message)
        except (ValueError, ApiCallError) as e:
            raise NotificationError(str(e))
