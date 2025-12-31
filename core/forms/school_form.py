# core/forms/school_form.py
from django import forms
from jdatetime import date as jdate  # برای تبدیل شمسی به میلادی
from ..models.school import School


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = [
            'name', 'gender', 'level', 'address', 'education_manager',
            'manager_phone', 'manager_email', 'contract_date', 'fabric_color_image', 'description'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'level': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'education_manager': forms.TextInput(attrs={'class': 'form-control'}),
            'manager_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'manager_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contract_date': forms.TextInput(attrs={'class': 'form-control persian-date', 'placeholder': 'YYYY/MM/DD (شمسی)', 'readonly': 'readonly'}),
            'fabric_color_image': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

    def clean_manager_phone(self):
        phone = self.cleaned_data.get('manager_phone')
        if phone and not phone.startswith('09'):
            raise forms.ValidationError('شماره موبایل باید با ۰۹ شروع شود.')
        return phone

    def clean_contract_date(self):
        contract_date = self.cleaned_data.get('contract_date')
        if contract_date:
            # تبدیل شمسی به میلادی برای ذخیره در دیتابیس
            try:
                jd = jdate.fromjalali(contract_date.year, contract_date.month, contract_date.day)
                contract_date = jd.togregorian()
            except ValueError:
                raise forms.ValidationError('تاریخ قرارداد نامعتبر است.')
        return contract_date