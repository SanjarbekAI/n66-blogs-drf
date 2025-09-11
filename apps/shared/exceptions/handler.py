import traceback

from django.http import Http404
from rest_framework.exceptions import (
    PermissionDenied,
    NotAuthenticated,
    ValidationError,
    AuthenticationFailed,
    NotFound,
    MethodNotAllowed,
    NotAcceptable,
    UnsupportedMediaType,
    Throttled
)
from rest_framework.views import exception_handler as drf_exception_handler

from apps.shared.utils.custom_response import CustomResponse
from apps.shared.utils.telegram_alerts import alert_to_telegram
from apps.shared.exceptions.custom_exceptions import CustomException


def custom_exception_handler(exc, context):
    request = context.get("request")

    if request and (request.path.startswith("/api/v1/core/docs/")):
        return drf_exception_handler(exc, context)

    # Mapping of exception types to error codes
    exception_mapping = {
        ValidationError: "VALIDATION_ERROR",
        Http404: "NOT_FOUND",
        PermissionDenied: "PERMISSION_DENIED",
        NotAuthenticated: "AUTHENTICATION_FAILED",
        AuthenticationFailed: "AUTHENTICATION_FAILED",
        NotFound: "NOT_FOUND",
        MethodNotAllowed: "METHOD_NOT_ALLOWED",
        NotAcceptable: "NOT_ACCEPTABLE",
        UnsupportedMediaType: "UNSUPPORTED_MEDIA_TYPE",
        Throttled: "THROTTLED"
    }

    # Handle CustomException separately as it has special context handling
    if isinstance(exc, CustomException):
        return CustomResponse.error(
            message_key=exc.message_key,
            request=request,
            context=exc.context
        )

    # Handle mapped exceptions
    for exc_type, error_code in exception_mapping.items():
        if isinstance(exc, exc_type):
            return CustomResponse.error(
                message_key=error_code,
                request=request,
                context=context,
                exc=str(exc)
            )

    # Unknown messages handling
    current_traceback = traceback.format_exc()
    safe_traceback = (
        current_traceback[-2000:]
        if current_traceback and current_traceback.strip() != "NoneType: None"
        else "No traceback available"
    )

    alert_to_telegram(safe_traceback, str(exc), request=request)

    return CustomResponse.error(
        message_key="UNKNOWN_ERROR",
        request=request,
        context=context
    )
