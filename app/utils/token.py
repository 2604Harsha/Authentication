import uuid
from datetime import datetime, timedelta

def generate_token(minutes=15):
    return str(uuid.uuid4()), datetime.utcnow() + timedelta(minutes=minutes)
