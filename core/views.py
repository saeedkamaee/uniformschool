# core/views.py
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView

from core.models.school import School
from .forms.school_form import SchoolForm


def school_create(request:HttpRequest):
    if request.method == 'POST':
        form = SchoolForm(request.POST, request.FILES)
        if form.is_valid():
            school = form.save()
            messages.success(request, f'مدرسه "{school.name}" با موفقیت ثبت شد.')
            return redirect('school_list')  # بعداً لیست می‌سازیم
        else:
            messages.error(request, 'لطفاً فیلدهای اجباری را پر کنید یا داده‌ها را اصلاح کنید.')
    else:
        form = SchoolForm()

    return render(request, 'core/school_create.html', {'form': form})

class SchoolListView(ListView):
    model = School
    template_name = 'core/school_list.html'
    context_object_name = 'schools'
    ordering = ['name']