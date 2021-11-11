from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View

from django.views.generic.edit import FormView, DeleteView, UpdateView, CreateView

from .forms import RegisterForm, LoginForm, UserEmailForm, SetPasswordForm
from django.contrib.auth import authenticate, login
from django.views.generic import FormView
from django.contrib import messages

from django.urls import reverse_lazy
from .models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token
from django.http import JsonResponse
import json


def password_reset(request):
    form = UserEmailForm()
    if request.method == 'POST' and request.is_ajax():
        form = UserEmailForm(request.POST, request=request)
        if form.is_valid():
            return JsonResponse({'success': 'Reset link was sent to your email.'}, status=200)
        error_dict = {'status': 'form_invalid', 'form_errors': form.errors}
        return HttpResponse(json.dumps(error_dict),content_type="application/json", status=400)
    return render(request, 'registration/password_reset.html', {'form':form})


class UserSignInView(FormView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        username = form.cleaned_data.get('username_email_phone')
        password = form.cleaned_data.get('password')
        user = authenticate(
            self.request, username=username, 
            password=password
        )
        if user:
            login(self.request, user)
            return super().form_valid(form)
        messages.error(self.request, 'Wrong password or username.')
        return render(self.request, self.template_name)
        

class UserRegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('index')


class PasswordResetConfirmView(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            request.session['user_id'] = user.pk
            form = SetPasswordForm(request.POST, user=user)
            return render(request, 'registration/password_set.html', {'form': form})
        else:
            # return redirect('/')
            return HttpResponse('User is none or activation link expired')
    
    def post(self, request, *args, **kwargs):
        try:
            print('user id:', request.session.get('user_id'))
            user = User.objects.get(pk=request.session.get('user_id'))
        except User.DoesNotExist:
            print('user does not exist')
            pass
        else:
            del request.session['user_id']
            form = SetPasswordForm(request.POST, user=user)
            if form.is_valid():
                form.save()
                if user.username:
                    user = authenticate(
                        self.request, username=user.username, 
                        password=form.cleaned_data['new_password1']
                    )
                    if user:
                        login(self.request, user)
                return redirect('/')
            return render(request, 'registration/password_set.html', {'form': form})
