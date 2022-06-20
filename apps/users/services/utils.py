from decouple import config
from django.core.mail import send_mail


def send_activation_code(activate_code: str, email:str):
    title = "Hello it is activate link your user_shop in site OnlineShop"
    message = f"please click this activate code {config('link_send_activation_code')}{activate_code}"
    from_email = "OnlineShop@gmail.com"

    send_mail(
        title,
        message,
        from_email,
        [email],
        fail_silently=False,
    )


def send_new_password(email: str, activate_code: str):
    title = "Hi it is reset your password user_shop in site"
    message = f"Please write this password to change your password : {activate_code}"
    from_email = "OnlineShop@gmail.com"

    send_mail(
        title,
        message,
        from_email,
        [email],
        fail_silently=False,
    )


def send_order_activate_code(email: str, activate_code: str):
    title = "Hi you ordered some product in our site please confirm it"
    message = f"Please click to this link to confirm your order  {config('link_send_order_activate_code')}{activate_code}"
    from_email = "OnlineShop@gmail.com"

    send_mail(
        title,
        message,
        from_email,
        [email],
        fail_silently=False,
    )


def send_notification_message(email: str, product, product_id):
    title = "Hi you got this message because you subscribed in site OnlineShopping"
    message = f"Please see our new products we add some new products:   {product }  " \
              f"{config('link_product_notification')}{product_id}"
    from_email = "OnlineShop@gmail.com"

    send_mail(
        title,
        message,
        from_email,
        [email],
        fail_silently=False,
    )