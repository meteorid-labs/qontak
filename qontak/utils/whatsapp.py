from phonenumbers import parse, format_number, PhoneNumberFormat


def whatsapp_phone_number(phone_number, region=None):
    return format_number(parse(phone_number, region), PhoneNumberFormat.E164)
