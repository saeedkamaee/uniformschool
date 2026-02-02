# core/views.py
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .forms.school_form import SchoolForm


def school_create(request:HttpRequest):
    if request.method == 'POST':
        form = SchoolForm(request.POST, request.FILES)
        if form.is_valid():
            school = form.save()
            messages.success(
                request,
                _(f'مدرسه "{school.name}" با موفقیت ثبت شد.')
            )
            return redirect('school_create') 
        else:
            # پیام خطای کلی برای فرم ناقص
            messages.error(
                request,
                _('لطفاً تمام فیلدهای اجباری را پر کنید یا داده‌های نادرست را اصلاح کنید.')
            )
    else:
        form = SchoolForm()

    return render(request, 'core/school_create.html', {'form': form})