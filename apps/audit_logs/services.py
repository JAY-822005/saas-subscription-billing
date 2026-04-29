from .models import AuditLog


def create_audit_log(
    user=None,
    organization=None,
    action=None,
    model_name=None,
    object_id=None,
    metadata=None,
    ip_address=None
):
    return AuditLog.objects.create(
        user=user,
        organization=organization,
        action=action,
        model_name=model_name,
        object_id=object_id,
        metadata=metadata or {},
        ip_address=ip_address
    )
