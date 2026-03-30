from datetime import datetime, timedelta

def is_account_locked(user) -> bool:
    return user.locked_until and user.locked_until > datetime.utcnow()

def lock_account(user):
    user.locked_until = datetime.utcnow() + timedelta(minutes=15)
    user.failed_attempts = 0