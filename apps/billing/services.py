from django.utils import timezone
from datetime import timedelta


def calculate_next_retry(retry_count):
    """
    Smart retry logic:
    Retry 1 → after 1 day
    Retry 2 → after 3 days
    Retry 3 → after 7 days
    """

    if retry_count == 1:
        return timezone.now() + timedelta(days=1)

    if retry_count == 2:
        return timezone.now() + timedelta(days=3)

    return timezone.now() + timedelta(days=7)