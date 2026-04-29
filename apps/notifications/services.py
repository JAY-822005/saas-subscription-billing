def generate_renewal_message(organization_name, plan_name):
    return {
        "title": f"Subscription Renewal Reminder",
        "message": (
            f"Your {plan_name} plan for {organization_name} "
            f"will renew soon. Please ensure payment details are updated."
        )
    }