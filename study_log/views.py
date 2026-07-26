from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import DailyReport, StudySession
from .forms import DailyReportForm, StudySessionForm
from accounts.models import Profile


# -----------------------------------------------------


def student_required(view_func):
    """
    دکوراتور برای بررسی اینکه کاربر نقش دانش‌آموز رو داره
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        
        # if user is student or no
        if hasattr(request.user, 'profile') and request.user.profile.role == 'student':
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'شما دسترسی به این بخش را ندارید!')
            return redirect('accounts:profile')
    return wrapper


# -------------------------------------------------------

@student_required
@login_required
def my_reports(request):
    """
    نمایش لیست همه‌ی روزهایی که کاربر گزارش ثبت کرده
    """
    reports = DailyReport.objects.filter(student=request.user).order_by('-date')
    
    context = {
        'reports': reports,
    }
    return render(request, 'study_log/my_reports.html', context)


# --------------------------------------------------------


@student_required
@login_required
def create_report(request):
    """
    کاربر یک روز جدید رو انتخاب میکنه و یه DailyReport می‌سازه
    """

    if request.method == 'POST':
        
        form = DailyReportForm(request.POST)


        if form.is_valid():
            # check if there is already a form for today
            date = form.cleaned_data['date']
            existing_report = DailyReport.objects.filter(
                student=request.user, 
                date=date
            ).first()
            
            if existing_report:
                messages.warning(request, f'شما قبلاً برای تاریخ {date} گزارش ثبت کردید!')
                return redirect('study_log:daily_detail', daily_report_id=existing_report.id)
            
            # create a new report
            report = form.save(commit=False)
            report.student = request.user
            report.save()
            
            messages.success(request, f'گزارش روز {date} با موفقیت ساخته شد!')
            return redirect('study_log:daily_detail', daily_report_id=report.id)
    else:

        form = DailyReportForm(initial={'date': timezone.now().date()})
    
    return render(request, 'study_log/create_report.html', {'form': form})


@student_required
@login_required
def daily_detail(request, daily_report_id):
    """
    نمایش همه‌ی جلسات مطالعه برای یک روز خاص
    """
    report = get_object_or_404(DailyReport, id=daily_report_id, student=request.user)
    sessions = report.sessions.all().order_by('start_time')
    

    total_minutes = 0
    total_tests = 0
    for session in sessions:
        total_minutes += session.duration_minutes()
        total_tests += session.test_count
    
    total_hours = total_minutes // 60
    remaining_minutes = total_minutes % 60
    
    context = {
        'report': report,
        'sessions': sessions,
        'total_hours': total_hours,
        'total_minutes': remaining_minutes,
        'total_tests': total_tests,
    }
    return render(request, 'study_log/daily_detail.html', context)



@student_required
@login_required
def add_session(request, daily_report_id):
    """
    افزودن یک جلسه‌ی مطالعه به یک گزارش روزانه
    """
    report = get_object_or_404(DailyReport, id=daily_report_id, student=request.user)
    
    if request.method == 'POST':
        form = StudySessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.daily_report = report
            session.save()
            
            messages.success(request, f'جلسه‌ی {session.subject} با موفقیت ثبت شد!')
            return redirect('study_log:daily_detail', daily_report_id=report.id)
    else:
        form = StudySessionForm()
    
    context = {
        'form': form,
        'report': report,
    }
    return render(request, 'study_log/add_session.html', context)



@student_required
@login_required
def edit_session(request, session_id):
    """
    ویرایش یک جلسه‌ی مطالعه
    """
    session = get_object_or_404(StudySession, id=session_id, daily_report__student=request.user)
    report = session.daily_report
    
    if request.method == 'POST':
        form = StudySessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, 'جلسه با موفقیت ویرایش شد!')
            return redirect('study_log:daily_detail', daily_report_id=report.id)
    else:
        form = StudySessionForm(instance=session)
    
    context = {
        'form': form,
        'session': session,
        'report': report,
    }
    return render(request, 'study_log/edit_session.html', context)



@student_required
@login_required
def delete_session(request, session_id):
    """
    حذف یک جلسه‌ی مطالعه
    """
    session = get_object_or_404(StudySession, id=session_id, daily_report__student=request.user)
    report = session.daily_report
    
    if request.method == 'POST':
        session.delete()
        messages.success(request, 'جلسه با موفقیت حذف شد!')
        return redirect('study_log:daily_detail', daily_report_id=report.id)
    
    context = {
        'session': session,
        'report': report,
    }
    return render(request, 'study_log/delete_session.html', context)




# ===== consultant users 's features =====

@login_required
def consultant_dashboard(request):
    """
    نمایش لیست دانش‌آموزانی که به این مشاور متصل هستن
    """
    # just consultants
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'consultant':
        messages.error(request, 'شما دسترسی به این بخش را ندارید!')
        return redirect('accounts:profile')
    
    students = request.user.profile.students.all()
    

    students_data = []
    today = timezone.now().date()

    
    for student_profile in students:

        total_reports = DailyReport.objects.filter(student=student_profile.user).count()
        
        # آیا امروز گزارش ثبت کرده؟
        today_report = DailyReport.objects.filter(
            student=student_profile.user,
            date=today
        ).first()
        
        students_data.append({
            'profile': student_profile,
            'username': student_profile.user.username,
            'total_reports': total_reports,
            'today_report': today_report,
            'has_reported_today': today_report is not None,
        })
    
    context = {
        'students': students_data,
        'today': today,
    }
    return render(request, 'study_log/consultant_dashboard.html', context)


@login_required
def consultant_student_detail(request, student_id):
    """
    نمایش تمام گزارش‌های یک دانش‌آموز خاص به مشاور
    """

    if not hasattr(request.user, 'profile') or request.user.profile.role != 'consultant':
        messages.error(request, 'شما دسترسی به این بخش را ندارید!')
        return redirect('accounts:profile')
    
    student_profile = get_object_or_404(Profile, id=student_id, role='student')
    
    if student_profile.consultant != request.user.profile:
        messages.error(request, 'شما دسترسی به گزارش‌های این دانش‌آموز را ندارید!')
        return redirect('study_log:consultant_dashboard')
    
    reports = DailyReport.objects.filter(student=student_profile.user).order_by('-date')
    
    reports_data = []
    for report in reports:
        sessions = report.sessions.all().order_by('start_time')
        total_minutes = sum(s.duration_minutes() for s in sessions)
        total_tests = sum(s.test_count for s in sessions)
        
        reports_data.append({
            'report': report,
            'sessions': sessions,
            'total_minutes': total_minutes,
            'total_tests': total_tests,
        })
    
    context = {
        'student': student_profile,
        'reports': reports_data,
        'total_reports': len(reports_data),
    }
    return render(request, 'study_log/consultant_student_detail.html', context)