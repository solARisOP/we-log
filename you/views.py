from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from home.models import UserProfile
from blog.models import Post
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.mail import send_mail
import random
from email_validator import validate_email, EmailNotValidError
import json
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate

# Create your views here.

def profilePage(request):
    if request.user.is_authenticated:
        allPosts = Post.objects.filter(user = request.user)
        try:
            profile = UserProfile.objects.get(user = request.user)
            context = {'profile' : profile, 'allPosts' : allPosts, 'user_' : request.user}
        except ObjectDoesNotExist:
            context = {'allPosts' : allPosts, 'user_' : request.user}
        return render(request, 'account/user_profile.html', context)
    else :
        return render(request, 'account/non_profile.html')

def profileEdit(request):
    if request.user.is_authenticated:
        fname= request.POST['fname']
        lname= request.POST['lname']
        desc = request.POST['desc']
        # avatar = request.POST['avatar']
        user = User.objects.get(username = request.user.username)
        user.first_name = fname
        user.last_name = lname
        user.save()
        profile, created = UserProfile.objects.get_or_create(user = request.user)
        profile.description = desc
        profile.save()
        return redirect('/you') 

def otpVerificater(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('message', '')

        # try:
        #     emailinfo = validate_email(email)
        #     email = emailinfo['email']

        # except EmailNotValidError as e:
        #     return JsonResponse({''})
        currentPath = request.META.get('HTTP_REFERER').split("127.0.0.1:8000")[1]
        flag = User.objects.filter(email = email).exists()
        

        if flag:
            request.session['path'] = currentPath
            request.session['email'] = email
            OTP = random.randint(100000, 999999)
            subject = "OTP verification"
            message = f'''
            Dear {email},

            We have received your request to reset the password for your Welog account. To ensure the security of your account, please use the following One-Time Password (OTP) to complete the password reset process:

            OTP: {OTP}

            Please enter this OTP on the password reset page to create a new password for your account. If you didn't initiate this request or have any concerns regarding your account's security, please get in touch with our support 
            team immediately at {settings.EMAIL_HOST_USER}.
            Please note that this OTP is valid for a limited time to maintain the security of your account. If you do not use it within 2 mins, you may need to request another OTP.

            Thank you for choosing Welog. We appreciate your trust in us.

            Best regards,
            Welog admin
            Welog'''

            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list)
            response = {'otp' : f"{OTP}"}
        else:
            response = {'message' : "email doesnot exists in welog you have to signup to create an account"}

        return JsonResponse(response)
    
    return HttpResponse('very bad request', status=405)

def passwordReseter(request):
    if request.method == "POST":
        if request.user.is_authenticated == False:
            pass1 = request.POST['respass1']
            pass2 = request.POST['respass2']
            email = request.session['email']
            currentPath = request.session['path']
            
            if pass1 != pass2:
                messages.error(request, "Sorry passwords doesnot match")
                return redirect(currentPath)
            
            try:
                user = User.objects.get(email = email)
                user.set_password(pass1)
                user.save()
                messages.success(request, "Your password has successfully been changed")
            except ObjectDoesNotExist:
                messages.error(request, "Sorry no user exists")
            
            return redirect(currentPath)
        else:
            pass_ = request.POST['useroldpass']
            pass1 = request.POST['respass1']
            pass2 = request.POST['respass2']
            currentPath = request.META.get('HTTP_REFERER').split("127.0.0.1:8000")[1]
            if pass1 != pass2:
                messages.error(request, "Sorry passwords doesnot match")
                return redirect(currentPath)
            
            user = authenticate(username = request.user.username, password = pass_)

            if user is not None:
                user.set_password(pass1)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Your password has successfully been changed")
            else:
                messages.error(request, "wrong current password")

            return redirect(currentPath)
    return HttpResponse('very bad request', status=405)

def checker(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        if "email" in data:
            email = data['email']
            flag = User.objects.filter(email = email).exists()
            if flag == 0:
                request.session['email'] = email
                request.session['desc'] = data['desc']
                # request.session['img'] = data['avatar']
                request.session['fname'] = data['fname']
                request.session['lname'] = data['lname']
                request.session['currpath'] = request.META.get('HTTP_REFERER').split("127.0.0.1:8000")[1]
                OTP = random.randint(100000, 999999)
                subject = "OTP verification"
                message = f'''
                Dear {email},

                Thank you for choosing Welog! We're excited to have you as part of our community. To ensure the security of your account and complete the registration process, we require your email verification.

                Here is your One-Time Password (OTP):

                OTP: {OTP}

                If you did not request this OTP or have any concerns about your account's security, please contact our support team immediately at {settings.EMAIL_HOST_USER}.

                Thank you for joining [Company Name]. We look forward to serving you!

                Best regards,

                Welog Admin
                Welog'''

                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]
                send_mail(subject, message, email_from, recipient_list)
                message = False if flag==1 else True
                return JsonResponse({'message' : message, 'otp' : f"{OTP}"})
        else:  
            flag = User.objects.filter(username = data['username']).exists()
            message = False if flag else True
            return JsonResponse({'message' : message})
    
    return HttpResponse("what can i say, very very bad request", status=404)