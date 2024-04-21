from core.celery import app
from src.utils.helpers import send_sms


@app.task
def send_password(phone_number, password):
    """ """
    text = f"""
        ПОПЫТКА ВХОДА!!!
        Ваш новый пароль: {password}
        Просим вас изменить пароль после входа!
    """
    return send_sms(phone_number, text)


@app.task
def send_verify_code(phone_number, code):
    """ """
    text = f"""
        НИКОМУ НЕ СООБЩАЙТЕ ЭТОТ КОД!!!
        Ваш код подтверждения: {code}
    """
    return send_sms(phone_number, text)
