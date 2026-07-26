from django import forms
from .models import DailyReport, StudySession

class DailyReportForm(forms.ModelForm):
    """فرم ایجاد گزارش روزانه (فقط انتخاب تاریخ)"""
    
    class Meta:
        model = DailyReport
        fields = ['date']
        widgets = {
            'date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
        }

        labels = {
            'date': 'تاریخ گزارش',
        }


class StudySessionForm(forms.ModelForm):
    """فرم ثبت یک جلسه‌ی مطالعه"""
    
    class Meta:
        model = StudySession
        fields = ['subject', 'start_time', 'end_time', 'test_count', 'description']

        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'مثال: ریاضیات گسسته'
            }),

            'start_time': forms.TimeInput(attrs={
                'type': 'time', 
                'class': 'form-control'
            }),

            'end_time': forms.TimeInput(attrs={
                'type': 'time', 
                'class': 'form-control'
            }),

            'test_count': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': 0,
                'placeholder': 'تعداد تست'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'توضیحات اختیاری...'
            }),
        }

        labels = {
            'subject': 'درس',
            'start_time': 'ساعت شروع',
            'end_time': 'ساعت پایان',
            'test_count': 'تعداد تست',
            'description': 'توضیحات (اختیاری)',
        }
    
    
    def clean(self):
        """اعتبارسنجی: چک میکنه که ساعت شروع از پایان کمتر باشه"""
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time:
            if start_time >= end_time:
                raise forms.ValidationError(
                    'ساعت شروع باید از ساعت پایان کمتر باشد!'
                )
        return cleaned_data