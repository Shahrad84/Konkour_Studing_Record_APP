from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta  # ← این رو حتماً اضافه کنید

class DailyReport(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_reports')
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.student.username} - {self.date}"
    
    def total_tests(self):
        return sum(session.test_count for session in self.sessions.all())


class StudySession(models.Model):
    daily_report = models.ForeignKey(DailyReport, on_delete=models.CASCADE, related_name='sessions')
    subject = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    test_count = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.daily_report.student.username} - {self.subject} - {self.daily_report.date}"
    
    def duration_minutes(self):
        """محاسبه مدت زمان جلسه به دقیقه"""
        today = datetime.now().date()
        start_dt = datetime.combine(today, self.start_time)
        end_dt = datetime.combine(today, self.end_time)
        
        if end_dt < start_dt:
            end_dt += timedelta(days=1)
        
        delta = end_dt - start_dt
        return delta.total_seconds() / 60