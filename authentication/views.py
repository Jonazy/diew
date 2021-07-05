from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator
from django.contrib import auth
# Create your views here.


class SignupView(View):
    def get(self, request):
        return render(request, 'authentication/signup.html')

    def post(self, request):
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/signup.html', context)
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                # user.is_active = False
                user.save()

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

                domain = get_current_site(request).domain
                link = reverse('activate-account', kwargs={
                    "uidb64": uidb64,
                    "token": token_generator.make_token(user),
                })
                sender = 'jonaz.honur@gmail.com'
                activate_url = "http//"+domain+link
                send_mail(
                    'Account Activation',
                    'Hi, ' + username + ' click link below to activate account\n' + activate_url,
                    sender,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'Account created successfully')
                return render(request, 'authentication/signup.html')
        return render(request, 'authentication/signup.html')


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({"username_error": "Username should only contain alphanumeric characters"}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({"username_error": "Username already exists."}, status=400)
        return JsonResponse({"username_valid": True}, status=200)


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({"email_error": "Email is invalid."}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({"email_error": "Email is already taken, please enter another email."}, status=400)
        return JsonResponse({"email_valid": True}, status=200)


class AccountVerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            context = {
                'fieldValues': request.GET
            }

            if not token_generator.check_token(user, token):
                messages.info(request, "Account already activated. Please Login")
                return redirect('login', context)
            if user.is_active:
                return redirect('login', context)
            user.is_active = True
            user.save()
            messages.success(request, "Account activated successfully")
            return redirect('login', context)
        except Exception as ex:
            pass
        return render(request, 'authentication/login.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, "login successfully")
                    return redirect("index")
                messages.error(request, "Account is not activated yet, Please check your email")
                return render(request, "authentication/login.html")
            messages.error(request, "Invalid login credentials")
            return render(request, "authentication/login.html")
        messages.error(request, "Fill all fields")
        return render(request, "authentication/login.html")


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "You have been logout")
        return redirect('login')