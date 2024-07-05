from django.shortcuts import render,redirect
from django.contrib import messages,auth
from .forms import RegistrationForm
from .models import Account
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import (urlsafe_base64_encode, urlsafe_base64_decode)
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

##########################################################################
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,"Account is Accivated! ")
        return redirect('login')
    else:
        messages.warning(request,"Invalid Activation Link")
        return redirect('register')
    


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password) # type: ignore
            user.phone_number = phone_number
            user.save()

            # email send for verification logic
            current_site = get_current_site(request)
            mail_subject = "Please Activate Your Account!"
            message = render_to_string('AccountsApp/account_verification_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            }) 
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            #####################################################################
            return redirect(f"/accounts/login/?command=verification&email={email}")
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'AccountsApp/register.html', context)


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user) 
            messages.success(request, 'logged')
            return redirect('index')
        
        else:
            messages.warning(request, 'Invalid Email/Password')
            return redirect('login')

    return render(request,'AccountsApp/login.html')



@login_required(login_url= 'login')
def logout(request):
    auth.logout(request)
    messages.info(request,"Logout!")
    return redirect('login')



@login_required(login_url= 'login')
def dashboard(request):
    return render(request, 'AccountsApp/dashboard.html')


def forgotPassword(request):
    if request.method =="POST":
        email = request.POST['email']
        existing_email = Account.objects.filter(email=email).exists()
        if existing_email == True:
            user = Account.objects.get(email__exact=email)
            # Reset Password email
            current_site = get_current_site(request)
            mail_subject = "Password Reset"
            message = render_to_string('AccountsApp/resetPassword_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            }) 
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            #####################################################
            
            return redirect("login")
        else:
            messages.warning(request,'Account Not Found')
            return redirect('forgotPassword')
    return render(request, 'AccountsApp/forgotPassword.html')



def resetPassword_validate(request):
    return HttpResponse(request,'ok')








