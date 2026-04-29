from .models import UsageRecord


def check_upgrade_recommendation(usage_record):
    usage_percentage = (
        usage_record.used_units / usage_record.usage_limit
    ) * 100

    if usage_percentage >= 80:
        return {
            "recommended": True,
            "message": "Upgrade recommended: usage above 80%"
        }

    return {
        "recommended": False,
        "message": "Current plan is sufficient"
    }