from django.core.mail import EmailMultiAlternatives


def sendCode(send_to=None, code=None):
    msg = EmailMultiAlternatives(
        "Activation code",
        f"Go to your profile and fill in the field to activate mail",
        "bonafresco@gmail.com",
        [send_to]
    )
    html_content = f"<div style='background-color:white;color:black;font-size: 20px;'>" \
                   f"   <p>Your code: {code}</p>" \
                   f"</div>"
    msg.attach_alternative(html_content, "text/html")
    msg.send()
