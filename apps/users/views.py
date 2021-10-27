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



def main(request):
    # return render(request, 'registration/password_reset.html')
    return render(request, 'main/index.html')

def password_reset(request):
    form = UserEmailForm()
    if request.method == 'POST':
        form = UserEmailForm(request.POST, request=request)
        if form.is_valid():
            return render(request, 'registration/password_reset.html', {'form':form})
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
            # user.is_active = True
            # user.save(update_fields=['is_active'])
            # login(request, user)
            return render(request, 'registration/password_set.html', {'form': form})
        else:
            # messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('/')
    
    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            print(request.session.get('user_id'))
            user = User.objects.get(pk=request.session.get('user_id'))
        except User.DoesNotExist:
            print('none')
            pass
        else:
            del request.session['user_id']
            form = SetPasswordForm(request.POST, user=user)
            if form.is_valid():
                form.save()
                return redirect('/')
            return render(request, 'registration/password_set.html', {'form': form})
