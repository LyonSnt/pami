import hashlib
import json
from time import time as current_time

from django.conf import settings


FINGERPRINT_SESSION_KEY = "contact_last_fingerprint"
TIMESTAMP_SESSION_KEY = "contact_last_submitted_at"


def is_duplicate_submission(request, data):
    fingerprint = _build_fingerprint(data)
    previous_fingerprint = request.session.get(FINGERPRINT_SESSION_KEY)
    previous_timestamp = request.session.get(TIMESTAMP_SESSION_KEY, 0)
    elapsed_seconds = current_time() - previous_timestamp

    return (
        fingerprint == previous_fingerprint
        and 0 <= elapsed_seconds <= settings.CONTACT_DUPLICATE_WINDOW_SECONDS
    )


def remember_submission(request, data):
    request.session[FINGERPRINT_SESSION_KEY] = _build_fingerprint(data)
    request.session[TIMESTAMP_SESSION_KEY] = current_time()


def _build_fingerprint(data):
    normalized_data = {
        key: str(value.pk if hasattr(value, "pk") else value).strip().lower()
        for key, value in sorted(data.items())
    }
    serialized_data = json.dumps(
        normalized_data,
        ensure_ascii=True,
        sort_keys=True,
    )
    return hashlib.sha256(serialized_data.encode("utf-8")).hexdigest()
