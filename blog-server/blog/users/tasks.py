from celery import shared_task
from users.models import User, EmailVerification

from django.utils.timezone import now, timedelta
import uuid

import logging

logger = logging.getLogger(__name__)


@shared_task
def send_email_task(user_id):
    print('in task')
    user = User.objects.get(pk=user_id)
    expiration = now() + timedelta(hours=24)
    record = EmailVerification.objects.create(
        code=uuid.uuid4(),
        user=user,
        expiration=expiration
    )
    record.send_verification_email()