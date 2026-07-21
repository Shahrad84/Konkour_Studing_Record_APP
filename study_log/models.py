# study_log/models.py
from django.db import models
from django.contrib.auth.models import User


class DailyReport(models.Model):

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_reports')
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'date']
    
    def __str__(self):
        return f"{self.student.username} - {self.date}"
    
    def total_study_time(self):
        """محاسبه‌ی مجموع زمان مطالعه در این روز"""
        total_minutes = 0

        for session in self.sessions.all():
            delta = session.end_time - session.start_time
            total_minutes += delta.total_seconds() / 60

        return total_minutes
    
    def total_tests(self):
        """مجموع تست‌های زده شده در این روز"""
        return sum(session.test_count for session in self.sessions.all())


class StudySession(models.Model):
    
    daily_report = models.ForeignKey(DailyReport, on_delete=models.CASCADE, related_name='sessions')
    subject = models.CharField(max_length=100)
    start_time = models.TimeField()  # 14:30
    end_time = models.TimeField()    # 15:30
    test_count = models.PositiveIntegerField()  # 30
    description = models.TextField(blank=True, null=True)  # optional description
    
    def __str__(self):
        return f"{self.daily_report.student.username} - {self.subject} - {self.daily_report.date}"
    
    def duration_minutes(self):
        """مدت زمان جلسه به دقیقه"""
        delta = self.end_time - self.start_time
        return delta.total_seconds() / 60