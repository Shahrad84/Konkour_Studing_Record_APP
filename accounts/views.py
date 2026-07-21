from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm


def register_view(request):
    """
    این ویو کارش نمایش فرم ثبت‌نام و پردازش اطلاعات اونه
    """


    if request.user.is_authenticated:
        return redirect('accounts:profile')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'ثبت‌نام با موفقیت انجام شد! خوش آمدی {user.username}')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'لطفاً خطاها رو تصحیح کنید.')


    else:
        # کاربر اولین باره که میاد این صفحه، یه فرم خالی بهش نشون بده
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})





def login_view(request):
    """
    این ویو کارش نمایش فرم ورود و احراز هویت کاربره
    """


    if request.user.is_authenticated:
        return redirect('accounts:profile')
    
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)


        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'خوش آمدی {username}!')
                return redirect('accounts:profile')
            else:
                messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
        else:
            messages.error(request, 'لطفاً اطلاعات را درست وارد کنید.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})




def logout_view(request):
    """
    کاربر رو از سیستم خارج میکنه
    """
    logout(request)
    messages.info(request, 'با موفقیت خارج شدید.')
    return redirect('accounts:login')





def profile_view(request):
    """
    صفحه‌ی پروفایل کاربر رو نشون میده (بعد از لاگین)
    """

    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    return render(request, 'accounts/profile.html', {
        'user': request.user
    })