from typing import TypedDict, Any

from apps.shared.messages import MESSAGES


class MessageDetail(TypedDict):
    id: str
    message: str
    status_code: int


def _get_message_detail(
        message_key: str,
        lang: str = "ru",
        context: dict[str, Any] | None = None
) -> MessageDetail:
    message = MESSAGES.get(message_key) or MESSAGES.get('UNKNOWN_ERROR')

    context = context or {}
    template = message["messages"].get(lang, message["messages"]["ru"])
    try:
        formatted_message = template.format(**context)
    except (KeyError, ValueError) as e:
        # Consider logging the formatting error here
        formatted_message = template

    return {
        "id": message["id"],
        "message": formatted_message,
        "status_code": message["status_code"]
    }


def get_message_detail(message_key: str, lang: str = "en", context: dict[str, Any] | None = None) -> MessageDetail:
    print(lang, "*********")
    return _get_message_detail(message_key, lang, context)


def get_message(message_key: str):
    return MESSAGES.get(message_key) or MESSAGES.get('UNKNOWN_ERROR') or {}
