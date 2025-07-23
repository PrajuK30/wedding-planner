from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib.auth.decorators import login_required
from .forms import CustomUserEditForm
from .models import CustomUser


# Temporary OTP store
otp_storage = {}

# Welcome Page
def welcome_page(request):
    return render(request, 'account/welcome.html')

# Registration View
def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        gender = request.POST.get('gender')
        mobile = request.POST.get('mobile')
        location = request.POST.get('location')
        pincode = request.POST.get('pincode')
        age = request.POST.get('age')

        if User.objects.filter(username=email).exists():
            messages.error(request, "This email is already registered. Please use another.")
            return render(request, 'account/register.html')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        user.middle_name = middle_name
        user.role = role
        user.gender = gender
        user.mobile = mobile
        user.location = location
        user.pincode = pincode
        user.age = age
        user.is_active = False
        user.save()

        otp = str(random.randint(100000, 999999))
        otp_storage[email] = otp

        send_mail(
            subject='Your OTP for Wedding Planner Registration',
            message=f'Hi {first_name},\nYour OTP is: {otp}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )

        request.session['otp_email'] = email
        messages.success(request, 'You are successfully registered! Check your email for the OTP.')
        return redirect('otp_verification')

    return render(request, 'account/register.html')

# OTP Verification View
def otp_verification_view(request):
    email = request.session.get('otp_email')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')

        if not entered_otp:
            messages.error(request, "Please enter OTP.")
            return redirect('otp_verification')

        if email in otp_storage and otp_storage[email] == entered_otp:
            try:
                user = User.objects.get(username=email)
                user.is_active = True
                user.save()
                del otp_storage[email]
                messages.success(request, "You are verified!")
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, "User not found.")
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'account/otp_verification.html', {'email': email})

# Resend OTP
def resend_otp_view(request):
    email = request.session.get('otp_email')
    if email:
        otp = str(random.randint(100000, 999999))
        otp_storage[email] = otp

        send_mail(
            subject='Resend OTP for Wedding Planner',
            message=f'Your OTP is: {otp}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )
        messages.success(request, "OTP resent successfully.")
    else:
        messages.error(request, "Email not found or OTP expired.")
    return redirect('otp_verification')

# Login View
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, "You are successfully logged in!")
                return redirect('dashboard')
            else:
                messages.error(request, "Account not verified. Please complete OTP verification.")
                request.session['otp_email'] = email
                return redirect('otp_verification')
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'account/login.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Success Pages
def register_success(request):
    return render(request, 'account/register_success.html')

def otp_success(request):
    return render(request, 'account/otp_success.html')

def login_success(request):
    return render(request, 'account/login_success.html')

# Dashboard View
@login_required
def dashboard_view(request):
    return render(request, 'account/dashboard.html', {'user': request.user})

# Profile View
@login_required
def profile_view(request):
    return render(request, 'account/profile.html', {'user': request.user})

# Edit Profile View
@login_required
def edit_profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserEditForm(instance=user)

    return render(request, 'account/edit_profile.html', {'form': form})

from django.contrib import messages
import random
from django.core.mail import send_mail

def resend_otp(request):
    email = request.session.get('email')
    if not email:
        messages.error(request, "Session expired. Please register again.")
        return redirect('register')

    # Generate new OTP
    otp = random.randint(100000, 999999)
    
    # Save to session again
    request.session['otp'] = str(otp)

    # Send OTP again
    send_mail(
        subject="Your Resent OTP - Wedding Planner",
        message=f"Your new OTP is {otp}",
        from_email="your_email@example.com",
        recipient_list=[email],
        fail_silently=False,
    )

    messages.success(request, "New OTP has been sent to your email.")
    return redirect('verify_otp')
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
import random

User = get_user_model()

# Forgot Password View
def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            
            otp = random.randint(1000, 9999)
            request.session['reset_email'] = email
            request.session['reset_otp'] = str(otp)

            # Send OTP to email
            send_mail(
                'Your OTP for Password Reset',
                f'Your OTP is: {otp}',
                'from@example.com',
                [email],
                fail_silently=False,
            )

            # ✅ If OTP sent successfully, go to reset password page
            return redirect('reset_password')

        except User.DoesNotExist:
            # 🔴 Show error on the same page
            return render(request, 'account/forgot_password.html', {
                'error': 'Email not registered. Please try again.'
            })

    return render(request, 'account/forgot_password.html')


def reset_password_otp_view(request):
    if request.method == "POST":
        otp_entered = request.POST.get('otp')
        password = request.POST.get('new_password')  # ✅ match HTML input name
        confirm_password = request.POST.get('confirm_password')

        real_otp = request.session.get('reset_otp')
        email = request.session.get('reset_email')

        if not otp_entered:
            return render(request, 'account/reset_password_otp.html', {'error': 'Please enter OTP first'})
        if otp_entered != real_otp:
            return render(request, 'account/reset_password_otp.html', {'error': 'Invalid OTP'})
        if password != confirm_password:
            return render(request, 'account/reset_password_otp.html', {'error': 'Passwords do not match'})

        try:
            user = CustomUser.objects.get(email=email)
            user.set_password(password)
            user.save()

            # ✅ Set popup flag
            request.session['popup'] = True
            request.session['popup_message'] = 'Password reset successful! You can now log in.'

            return redirect('reset_done')  # ✅ Will show popup

        except CustomUser.DoesNotExist:
            return render(request, 'account/reset_password_otp.html', {'error': 'User not found'})

    return render(request, 'account/reset_password_otp.html')
def reset_success_view(request):
    return render(request, 'reset_success.html')




def reset_done(request):
    popup = request.session.pop('popup', False)
    popup_message = request.session.pop('popup_message', '')
    return render(request, 'account/reset_success.html', {
        'popup': popup,
        'popup_message': popup_message,
    })