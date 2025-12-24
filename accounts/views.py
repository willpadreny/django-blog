from django.views.generic import FormView, TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from .forms import SignupForm
from .forms import SigninForm
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp import user_has_device
from django_otp.util import random_hex
import qrcode
import qrcode.image.svg
from io import BytesIO
import base64

class SignupView(FormView):
    template_name = 'accounts/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('blog:home')

    def form_valid(self, form):
        user = User.objects.create_user(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password'],
            email = form.cleaned_data['email']
        )
        login(self.request, user)
        return super().form_valid(form)

class SigninView(FormView):
    template_name = 'accounts/signin.html'
    form_class = SigninForm
    success_url = reverse_lazy('blog:home') # change to home url

    def form_valid(self, form):

         username = form.cleaned_data['username']
         password = form.cleaned_data['password']

         user = authenticate(self.request, username=username, password=password)

         if user is not None:
            # Check if user has 2FA enabled
            has_2fa = TOTPDevice.objects.filter(user=user, confirmed=True).exists()

            if has_2fa:
                # Store user ID in session and redirect to 2FA verification
                self.request.session['pre_2fa_user_id'] = user.id
                return redirect('accounts:2fa_verify')
            else:
                # No 2FA, login normally
                login(self.request, user)
                return super().form_valid(form)
         else:
            form.add_error(None, 'Invalid username or password')
            return self.form_invalid(form)


def logout_view(request):
    logout(request)
    return redirect('/')

class TwoFactorSetupView(LoginRequiredMixin, View):
    login_url = '/accounts/signin/'

    def get(self, request):
        # Check if user already has a device
        existing_device = TOTPDevice.objects.filter(user=request.user, confirmed=True).first()

        if existing_device:
            messages.info(request, 'You already have 2FA enabled.')
            return redirect('blog:my_profile')

        # Create or get unconfirmed device
        device, created = TOTPDevice.objects.get_or_create(
            user=request.user,
            name='default',
            confirmed=False
        )

        # Generate QR code
        url = device.config_url
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        context = {
            'qr_code': img_str,
            'secret_key': device.key,
        }

        return render(request, 'accounts/2fa_setup.html', context)

class TwoFactorVerifySetupView(LoginRequiredMixin, View):
    login_url = '/accounts/signin/'

    def post(self, request):
        token = request.POST.get('token')

        device = TOTPDevice.objects.filter(user=request.user, confirmed=False).first()

        if not device:
            messages.error(request, 'No setup in progress. Please start again.')
            return redirect('accounts:2fa_setup')

        if device.verify_token(token):
            device.confirmed = True
            device.save()
            messages.success(request, '2FA has been enabled successfully!')
            return redirect('blog:my_profile')
        else:
            messages.error(request, 'Invalid code. Please try again.')
            return redirect('accounts:2fa_setup')

class TwoFactorDisableView(LoginRequiredMixin, View):
    login_url = '/accounts/signin/'

    def post(self, request):
        TOTPDevice.objects.filter(user=request.user).delete()
        messages.success(request, '2FA has been disabled.')
        return redirect('blog:my_profile')

class TwoFactorVerifyView(View):
    def get(self, request):
        # Check if user is in session but not verified
        if not request.session.get('pre_2fa_user_id'):
            return redirect('accounts:signin')

        return render(request, 'accounts/2fa_verify.html')

    def post(self, request):
        token = request.POST.get('token')
        user_id = request.session.get('pre_2fa_user_id')

        if not user_id:
            messages.error(request, 'Session expired. Please log in again.')
            return redirect('accounts:signin')

        try:
            user = User.objects.get(id=user_id)
            device = TOTPDevice.objects.filter(user=user, confirmed=True).first()

            if device and device.verify_token(token):
                # Complete the login
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                del request.session['pre_2fa_user_id']
                messages.success(request, 'Successfully logged in with 2FA!')
                return redirect('blog:home')
            else:
                messages.error(request, 'Invalid code. Please try again.')
                return render(request, 'accounts/2fa_verify.html')
        except User.DoesNotExist:
            messages.error(request, 'Session expired. Please log in again.')
            return redirect('accounts:signin')
