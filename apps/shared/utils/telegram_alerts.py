import html
import logging
import threading

import telebot

# Initialize bot once
bot = telebot.TeleBot(token="7590412308:AAEXdbv2SdN-5hhqiFaUyLZL41PcbFrk9a4")


def _send_telegram_message(text: str):
    """Internal function: Sends a Telegram message (runs inside thread)."""
    try:
        bot.send_message(
            chat_id="-1002529908861",
            text=text,
            parse_mode='HTML',
            disable_web_page_preview=True
        )
    except Exception as e:
        logging.error(f"Failed to send alert to Telegram: {str(e)}")


def send_alert(text: str):
    """Starts a thread to send alert without blocking."""
    threading.Thread(target=_send_telegram_message, args=(text,), daemon=True).start()


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def alert_to_telegram(traceback_text: str, message: str = "No message provided", request=None, ip: str = None,
                      port: str = None):
    if not isinstance(message, str):
        message = str(message)

    if request and not ip:
        ip = get_client_ip(request)
        port = request.META.get("REMOTE_PORT")

    safe_message = html.escape(message)
    safe_traceback = html.escape(traceback_text)
    safe_ip = html.escape(ip) if ip else "unknown"
    safe_port = html.escape(str(port)) if port else "unknown"

    text = (
        "❌ <b>Exception Alert</b> ❌\n\n"
        f"<b>✍️ Message:</b> <code>{safe_message}</code>\n\n"
        f"<b>🔖 Traceback:</b> <code>{safe_traceback}</code>\n\n"
        f"<b>🌐 IP Address/Port:</b> <code>{safe_ip}:{safe_port}</code>\n\n"
    )
    send_alert(text)
