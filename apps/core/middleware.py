import time
import logging

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time

        logger.info(
            f"{request.method} {request.path} "
            f"STATUS={response.status_code} "
            f"TIME={duration:.3f}s"
        )

        return response
    
import logging
import traceback

logger = logging.getLogger(__name__)


class ErrorLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)

        except Exception as e:
            logger.error(
                "Exception occurred",
                exc_info=True,
                extra={
                    "path": request.path,
                    "method": request.method,
                    "error": str(e),
                    "trace": traceback.format_exc(),
                }
            )
            raise