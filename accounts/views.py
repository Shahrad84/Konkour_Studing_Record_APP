from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile


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



@login_required
def profile_view(request):
    """
    نمایش پروفایل کاربر و امکان انتخاب مشاور (برای دانش‌آموزان)
    """
    profile = request.user.profile
    
    if request.method == 'POST' and profile.role == 'student':
        consultant_username = request.POST.get('consultant_username', '').strip()
        
        if consultant_username:
            try:
                consultant_user = User.objects.get(username=consultant_username)
                
                if hasattr(consultant_user, 'profile') and consultant_user.profile.role == 'consultant':
                    if consultant_user == request.user:
                        messages.error(request, 'شما نمی‌توانید خودتان را به عنوان مشاور انتخاب کنید!')
                    else:
                        profile.consultant = consultant_user.profile
                        profile.save()
                        messages.success(request, f'مشاور {consultant_user.username} با موفقیت انتخاب شد!')
                else:
                    messages.error(request, 'این کاربر نقش مشاور را ندارد!')

            except User.DoesNotExist:
                messages.error(request, 'کاربری با این نام کاربری در دیتابیس وجود ندارد!')
        else:
            messages.warning(request, 'لطفاً نام کاربری مشاور را وارد کنید.')
    
    context = {
        'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)