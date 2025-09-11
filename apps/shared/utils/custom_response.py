from dataclasses import dataclass
from typing import Dict, Any, Optional

from rest_framework.request import Request
from rest_framework.response import Response

from apps.shared.exceptions.translator import get_message_detail


@dataclass
class ResponseBody:
    """Standardized response structure with translation support"""
    message_key: str
    request: Optional[Request] = None
    context: Optional[Dict] = None

    def to_dict(self, **kwargs) -> Dict[str, Any]:
        # Get translated message details
        lang = self._get_request_language()
        message_detail = get_message_detail(
            message_key=self.message_key,
            lang=lang,
            context=self.context
        )

        return {
            "message": message_detail["message"],
            "status_code": message_detail["status_code"],
            **kwargs
        }

    def _get_request_language(self) -> str:
        """Extract language from request headers"""
        if self.request and hasattr(self.request, 'headers'):
            return self.request.headers.get('Accept-Language', 'en').split(',')[0]

        return 'en'


class CustomResponse:
    """Handle responses with automatic message translation"""

    @staticmethod
    def success(
            message_key: str = "SUCCESS_MESSAGE",
            request: Request = None,
            data: Any = None,
            context: Dict = None,
            **kwargs
    ) -> Response:
        body = ResponseBody(
            message_key=message_key,
            request=request,
            context=context
        ).to_dict(data=data, **kwargs)

        return Response(body, status=body["status_code"])

    @staticmethod
    def error(
            message_key: str,
            request: Request = None,
            context: Dict = None,
            **kwargs
    ) -> Response:
        body = ResponseBody(
            message_key=message_key,
            request=request,
            context=context
        ).to_dict(**kwargs)

        return Response(body, status=body["status_code"])
