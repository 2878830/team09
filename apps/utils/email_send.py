# encoding: utf-8
from random import Random

from users.models import EmailVerifyRecord

from django.core.mail import send_mail,EmailMessage

from CourseOnline.settings import EMAIL_FROM
:
from django.template import loader



def random_str(random_length=8):
    str = ''
   
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str



def send_register_eamil(email, send_type="register"):
   
    email_record = EmailVerifyRecord()
  
    if send_type == "update_email":
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type

    email_record.save()

  
    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "LearnEase Online Course Learning System - Registration activation link"
      
        email_body = loader.render_to_string(
                "email_register.html",  # 需要渲染的html模板
                {
                    "active_code": code  # 参数
                }
            )
        msg = EmailMessage(email_title, email_body, EMAIL_FROM, [email])
        msg.content_subtype = "html"
        send_status = msg.send()
      
        if send_status:
                pass
    elif send_type == "forget":
        email_title = "LearnEase online course learning system - Retrieve password link"
        email_body = loader.render_to_string(
            "email_forget.html",
            {
                "active_code": code  
            }
        )
        msg = EmailMessage(email_title, email_body, EMAIL_FROM, [email])
        msg.content_subtype = "html"
        send_status = msg.send()
    elif send_type == "update_email":
        email_title = "LearnEase online course learning system - modify email verification code"
        email_body = loader.render_to_string(
            "email_update_email.html", 
            {
                "active_code": code 
            }
        )
        msg = EmailMessage(email_title, email_body, EMAIL_FROM, [email])
        msg.content_subtype = "html"
        send_status = msg.send()
