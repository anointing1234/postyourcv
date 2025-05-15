from django.shortcuts import render,get_object_or_404, redirect
from django.urls import reverse
# from .form import RegisterForm,LoginForm,SendresetcodeForm,PasswordResetForm,ReviewForm 
from django.http import JsonResponse
import requests 
from decimal import Decimal, InvalidOperation
import logging
import traceback
import json
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout,login,authenticate
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal,InvalidOperation
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static
from django.core.mail import EmailMultiAlternatives
import pytz
from datetime import datetime, timedelta
from pytz import timezone as pytz_timezone
import logging
from django.db import transaction
from django.db.models import F,Sum
from django.contrib.auth.decorators import login_required
from .models import FootballJob
import logging
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from .models import FootballJob,PlayerJobApplication,ResetCode,Account
from .forms import PlayerJobApplicationForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import random
from django.contrib.auth.hashers import make_password

logger = logging.getLogger(__name__)

User = get_user_model()



def auth_login_view(request):
    return render(request,'auth/login.html')
    
def auth_signup_view(request):
    return render(request,'auth/signup.html')


def register(request):
    if request.method == "POST" and request.content_type == "application/json":
        try:
            data = json.loads(request.body)
            firstname        = data.get("Firstname", "").strip()
            lastname         = data.get("Lastname", "").strip()
            username         = data.get("username", "").strip()
            email            = data.get("email", "").strip()
            password         = data.get("password", "")
            confirm_password = data.get("confirm_password", "")
            terms_agreed     = data.get("terms", False)

            # 1) Validate required fields
            if not all([firstname,lastname,username, email, password, confirm_password]):
                return JsonResponse({'success': False, 'error': 'All fields are required!'})

            # 2) Validate email format
            try:
                validate_email(email)
            except ValidationError:
                return JsonResponse({'success': False, 'error': 'Enter a valid email address!'})

            # 3) Password rules
            if len(password) < 6:
                return JsonResponse({'success': False, 'error': 'Password must be at least 6 characters!'})
            if password != confirm_password:
                return JsonResponse({'success': False, 'error': 'Passwords do not match!'})

            # 4) Terms agreement
            if not terms_agreed:
                return JsonResponse({'success': False, 'error': 'You must agree to the Terms & Conditions!'})

            # 5) Uniqueness checks
            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'error': 'Username is already taken!'})
            if User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'error': 'Email is already in use!'})

            # 6) Create user
            user = User.objects.create_user(
                first_name=firstname,
                last_name=lastname,
                username=username,
                email=email,
                password=password
            )
            user.save()

            # 7) Log the user in
            login(request, user)

            # 8) Send welcome email
            subject = "Welcome to PYFCV"
            text = (
                f"Dear {username},\n\n"
                "Welcome to PYFCV! PYFCV is a professional football network that connects talented players with clubs, scouts, and agents.\n"
                "Whether you’re looking to showcase your profile, find new opportunities, or build your career in football,\n"
                "PYFCV is the platform that puts your game on the map.\n\n"
                "Get started by logging in and completing your profile.\n\n"
                "Best of luck on the pitch,\n"
                "The PYFCV Team"
            )
            html = f"""
            <html><body style="font-family:Arial,sans-serif;color:#333;">
              <div style="max-width:600px;margin:auto;padding:20px;border:1px solid #ddd;">
                <h2 style="color:#004e64;text-align:center;">
                  Welcome to PYFCV, {username}!
                </h2>
                <p>
                  PYFCV is a professional football network that connects talented players with clubs, scouts, and agents.
                </p>
                <p>
                  Whether you’re looking to <strong>showcase your profile</strong>, <strong>find new opportunities</strong>, 
                  or <strong>build your career in football</strong>, PYFCV is the platform that puts your game on the map.
                </p>
                <p>
                  Click the button below to log in and complete your profile:
                </p>
                <p style="text-align:center;">
                  <a href="{request.build_absolute_uri('/login/')}" 
                     style="display:inline-block;padding:10px 20px;border-radius:4px;
                            background:#028090;color:#fff;text-decoration:none;">
                    Log In to PYFCV
                  </a>
                </p>
                <p style="margin-top:30px;">
                  Best of luck on the pitch,<br>
                  <em>The PYFCV Team</em>
                </p>
              </div>
            </body></html>
            """

            try:
                send_mail(
                    subject,
                    text,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    html_message=html,
                    fail_silently=False,
                )
            except Exception as mail_exc:
                logger.exception("Welcome email sending failed.")
                return JsonResponse({
                    'success': False,
                    'error': 'User created, but failed to send welcome email. Please contact support.'
                })

            return JsonResponse({
                'success': True,
                'message': 'Registration successful! Welcome email sent.'
            })

        except Exception as exc:
            logger.exception("Registration error")
            return JsonResponse({
                'success': False,
                'error': f"Server error: {str(exc)}"
            })

    return render(request, 'forms/signup.html')



def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({"success": True, "message": "Login successful!"})
        else:
            return JsonResponse({"success": False, "message": "Invalid username or password. Please try again."})

    return render(request, "forms/login.html")



def logout_view(request):
    auth_logout(request)
    return render(request,'home/index.html')
   



def update_profile_picture(request):
    if request.method == "POST" and "profile_picture" in request.FILES:
        # assign the uploaded file to the correct field:
        request.user.profile_image = request.FILES["profile_picture"]
        request.user.save()
        messages.success(request, "Profile picture updated successfully!")
    else:
        messages.error(request, "No file selected. Please choose a valid image.")
    # redirect instead of render so the browser reloads with the new URL
    return render(request, "home/Account.html")



@login_required
@require_POST
def update_bio(request):
    """
    AJAX endpoint to update the logged-in user’s bio.
    Expects JSON payload: { "bio": "new text" }
    Returns { "success": true } or { "success": false, "error": "…" }.
    """
    try:
        payload = json.loads(request.body.decode('utf-8'))
        new_bio = payload.get('bio', '').strip()
        request.user.bio = new_bio
        request.user.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)




@login_required
@csrf_exempt  # Because you're posting JSON via fetch (make sure CSRF token is sent too)
def update_profile_info(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            user = request.user
            user.phone_number = data.get('phone_number', '')
            user.date_of_birth = data.get('date_of_birth') or None
            user.nationality = data.get('nationality', '')
            user.birth_date = data.get('birth_date', '')
            user.birth_place = data.get('birth_place', '')
            user.height = data.get('height') or None
            user.weight = data.get('weight') or None
            user.position = data.get('position', '')
            user.preferred_foot = data.get('preferred_foot', '')
            
            user.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})   

def football_job(request):
    jobs = FootballJob.objects.all()
    return render(request, "home/football_jobs.html",{'jobs': jobs})



def is_profile_complete(user):
    required_fields = [
        user.first_name,
        user.last_name,
        user.date_of_birth,
        user.nationality,
        user.phone_number,
        user.height,
        user.weight,
        user.position,
        user.preferred_foot,
        user.profile_image,
    ]
    return all(required_fields)


@login_required(login_url='home')
def apply_for_job(request, job_id):
    job = get_object_or_404(FootballJob, id=job_id)
    user = request.user

    # 🔒 Check if user profile is complete
    if not is_profile_complete(user):
        return redirect('player_account')  # Change this to your profile update URL name

    if request.method == 'POST':
        form = PlayerJobApplicationForm(request.POST, request.FILES, user=user)
        if form.is_valid():
            try:
                application = form.save(commit=False)
                application.job = job
                application.save()
                messages.success(request, "Application submitted successfully.")
                return redirect('apply_for_job', job_id=job.id)
            except Exception as e:
                messages.error(request, f"An error occurred while saving your application: {str(e)}")
        else:
            messages.error(request, "Please correct the errors in the form before submitting.")
            print(form.errors)
    else:
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_of_birth': user.date_of_birth,
            'nationality': user.nationality,
            'phone_number': user.phone_number,
            'email_address': user.email,
            'height': user.height,
            'weight': user.weight,
            'position': user.position,
            'preferred_foot': user.preferred_foot,
            'profile_image': user.profile_image,
        }
        form = PlayerJobApplicationForm(initial=initial_data, user=user)

    return render(request, 'home/apply.html', {'form': form, 'job': job})



def contact_player_view(request):
    if request.method == 'POST':
        # Grab and validate form data
        your_name       = request.POST.get('your_name', '').strip()
        email           = request.POST.get('email', '').strip()
        your_location   = request.POST.get('your_location', '').strip()
        player_name     = request.POST.get('player_name', '').strip() or 'N/A'
        player_location = request.POST.get('player_location', '').strip() or 'N/A'

        if not your_name or not email or not your_location:
            return JsonResponse(
                {'success': False, 'error': 'Please fill in all required fields.'},
                status=400
            )

        # Build plain-text fallback
        subject = f"Player Contact Request: {player_name}"
        text_body = (
            f"New contact request:\n\n"
            f"Your Name: {your_name}\n"
            f"Your Email: {email}\n"
            f"Your Location: {your_location}\n\n"
            f"Player Name: {player_name}\n"
            f"Player Location: {player_location}\n\n"
            "— End of message —"
        )

        # Build rich HTML message
        html_body = f"""
        <html>
          <body style="font-family:Arial,sans-serif;color:#333;background:#f9f9f9;padding:20px;">
            <div style="max-width:600px;margin:auto;background:#fff;
                        border:1px solid #ddd;border-radius:8px;overflow:hidden;">
              <div style="background:#004e64;color:#fff;padding:15px;text-align:center;">
                <h2 style="margin:0;font-size:1.5rem;">
                  Player Contact Request
                </h2>
              </div>
              <div style="padding:20px;">
                <p style="margin-bottom:12px;">
                  <strong>Contactor Name:</strong> {your_name}
                </p>
                <p style="margin-bottom:12px;">
                  <strong>Contactor Email:</strong> {email}
                </p>
                <p style="margin-bottom:12px;">
                  <strong>Contactor Location:</strong> {your_location}
                </p>
                <hr style="border:none;border-top:1px solid #eee;margin:20px 0;">
                <p style="margin-bottom:12px;">
                  <strong>Player Name:</strong> {player_name}
                </p>
                <p style="margin-bottom:12px;">
                  <strong>Player Location:</strong> {player_location}
                </p>
              </div>
              <div style="background:#f1f1f1;color:#555;padding:15px;text-align:center;font-size:0.9rem;">
                <p style="margin:0;">Please review this request in the admin dashboard.</p>
              </div>
            </div>
          </body>
        </html>
        """

        # Send email 
        try:
            send_mail(
                subject,
                text_body,
                settings.EMAIL_HOST_USER,
                ['yakubudestiny9@gmail.com'],
                html_message=html_body,
                fail_silently=False,
            )
        except Exception as e:
            logger.exception("Failed to send contact email")
            return JsonResponse(
                {'success': False, 'error': f'Could not send email. Error: {str(e)}'},
                status=500
            )
        return JsonResponse({'success': True})

    # GET: just render contact page
    return render(request,'home/contact.html')


def send_reset_code_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = get_object_or_404(Account, email=email)
        except:
            return JsonResponse({"success": False, "message": "Email not found."})

        # Generate 6-digit reset code
        reset_code = str(random.randint(100000, 999999))

        # Fetch or create ResetCode object
        reset_obj, created = ResetCode.objects.get_or_create(user=user)

        # Update code and status
        reset_obj.reset_code = reset_code
        reset_obj.reset_code_created_at = now()
        reset_obj.reset_code_status = "active"
        reset_obj.save()

        # Send email
        send_mail(
            "Password Reset Code",
            f"Your password reset code is: {reset_code}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return JsonResponse({"success": True, "message": "Reset code sent to your email."})

    return JsonResponse({"success": False, "message": "Invalid request."})




def reset_password_view(request):
    if request.method == "POST":
        # detect AJAX
        is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"

        email      = request.POST.get("email", "").strip()
        reset_code = request.POST.get("reset_code", "").strip()
        new_pass   = request.POST.get("new_password", "").strip()
        # confirm_password comes from client only for JS‐side validation

        # 1) Basic required‐fields check
        if not all([email, reset_code, new_pass]):
            msg = "All fields are required."
            if is_ajax:
                return JsonResponse({"success": False, "message": msg})
            messages.error(request, msg)
            return render(request, "auth/reset_pass.html")

        # 2) Look up user & ResetCode
        try:
            user = User.objects.get(email=email)
            code_obj = ResetCode.objects.get(user=user)
        except User.DoesNotExist:
            msg = "No user found with this email."
            if is_ajax:
                return JsonResponse({"success": False, "message": msg})
            messages.error(request, msg)
            return render(request, "auth/reset_pass.html")
        except ResetCode.DoesNotExist:
            msg = "Invalid reset code."
            if is_ajax:
                return JsonResponse({"success": False, "message": msg})
            messages.error(request, msg)
            return render(request, "auth/reset_pass.html")

        # 3) Validate the reset_code status & expiry (20 minutes)
        expired = now() - code_obj.reset_code_created_at > timedelta(minutes=20)
        if (
            str(code_obj.reset_code) != reset_code
            or code_obj.reset_code_status != "active"
            or expired
        ):
            msg = "Invalid or expired reset code."
            if is_ajax:
                return JsonResponse({"success": False, "message": msg})
            messages.error(request, msg)
            return render(request, "auth/reset_pass.html")

        # 4) All good → reset the password
        user.password = make_password(new_pass)
        user.save()

        # 5) Mark code as used
        code_obj.reset_code_status = "used"
        code_obj.save()

        msg = "Password reset successful. Please log in."
        if is_ajax:
            return JsonResponse({"success": True, "message": msg})
        messages.success(request, msg)
        return render(request, "auth/reset_pass.html")

    # GET (or other) → just show the form
    return render(request, "auth/reset_pass.html")
