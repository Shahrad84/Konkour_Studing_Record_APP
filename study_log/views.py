from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import DailyReport, StudySession
from .forms import DailyReportForm, StudySessionForm


# -------------------------------------------------------


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