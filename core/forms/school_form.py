# core/forms/school_form.py
from django import forms
from ..models.school import School


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = [
            'name', 'gender', 'level', 'address', 'education_manager',
            'manager_phone', 'manager_email', 'fabric_color_image', 'description'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'level': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'education_manager': forms.TextInput(attrs={'class': 'form-control'}),
            'manager_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'manager_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'fabric_color_image': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

    def clean_manager_phone(self):
        phone = self.cleaned_data.get('manager_phone')
        if phone and not phone.startswith('09'):
            raise forms.ValidationError('شماره موبایل باید با ۰۹ شروع شود.')
        return phone