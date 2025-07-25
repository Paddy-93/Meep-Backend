# users/views/verify_email_view.py
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from django.http import HttpResponse

User = get_user_model()


class VerifyEmailView(APIView):
    """
    Verifies the user's email using uid and token.
    URL: /api/users/verify-email/<uidb64>/<token>/
    """

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(User, pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return render(request, "users/email_verification_failed.html")

        if default_token_generator.check_token(user, token):
            user.is_verified = True
            user.save()
        
            # Optional: Redirect to your app with deep link
            # app_redirect_url = request.GET.get("redirect")
            # if app_redirect_url:
            #     return redirect(app_redirect_url)

            context = {
                'user': user
            }
            
            return render(request, "users/email_verification_success.html", context)

        return render(request, "users/email_verification_failed.html", status=400)
