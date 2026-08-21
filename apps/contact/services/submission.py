import hashlib
import json
from time import time as current_time

from django.conf import settings
from django.core.cache import cache


FINGERPRINT_SESSION_KEY = "contact_last_fingerprint"
TIMESTAMP_SESSION_KEY = "contact_last_submitted_at"
RATE_LIMIT_KEY_PREFIX = "contact-rate"


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


def is_rate_limited(request):
    client_address = _get_client_address(request)
    address_hash = hashlib.sha256(client_address.encode("utf-8")).hexdigest()
    cache_key = f"{RATE_LIMIT_KEY_PREFIX}:{address_hash}"

    if cache.add(cache_key, 1, settings.CONTACT_RATE_LIMIT_WINDOW_SECONDS):
        return False

    try:
        attempt_count = cache.incr(cache_key)
    except ValueError:
        cache.set(cache_key, 1, settings.CONTACT_RATE_LIMIT_WINDOW_SECONDS)
        return False

    return attempt_count > settings.CONTACT_RATE_LIMIT_MAX_SUBMISSIONS


def _get_client_address(request):
    return request.META.get("HTTP_X_REAL_IP") or request.META.get(
        "REMOTE_ADDR",
        "unknown",
    )


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
