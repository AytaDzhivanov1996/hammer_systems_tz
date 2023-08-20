from django.conf import settings
from django.utils.crypto import get_random_string

def generate_otp():
    """Функция для создания кода активации"""
    otp_length = getattr(settings, "OTP_LENGTH", 4)
    return get_random_string(otp_length, allowed_chars="0123456789")

def generate_referral_link():
    """Фунцкия создания реферальной ссылки"""
    link_length = getattr(settings, "LINK_LENGTH", 6)
    return get_random_string(link_length, allowed_chars="0123456789abcdefghijklmnopqrstuvwxyz")
