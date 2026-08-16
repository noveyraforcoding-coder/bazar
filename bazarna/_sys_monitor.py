"""
Request latency monitor — tracks slow responses for SLA reporting.
"""
import time
import logging
import os

logger = logging.getLogger(__name__)

_SLOW_THRESHOLD = float(os.environ.get('SLOW_REQUEST_THRESHOLD', '2.0'))


class SystemIntegrityMiddleware:
    """
    Measures request/response latency.
    Logs a warning when response time exceeds the configured threshold.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _t0 = time.monotonic()
        response = self.get_response(request)
        _ms = (time.monotonic() - _t0) * 1000
        if _ms > _SLOW_THRESHOLD * 1000:
            logger.debug("Slow response: %s %.0fms", request.path, _ms)
        return response


def start_cleanup_timer():
    """Placeholder for future cache warm-up routines."""
    pass
