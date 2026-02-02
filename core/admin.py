# core/admin.py
from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter # برای نمایش تاریخ شمسی در فیلترها
from .models import AcademicYear, School, ClassRoom, Student


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ['year', 'is_default', 'start_date', 'end_date']
    list_filter = ['is_default', ('start_date', JDateFieldListFilter), ('end_date', JDateFieldListFilter)]
    search_fields = ['year']
    actions = ['make_default']  # اکشن برای تنظیم پیش‌فرض

    def make_default(self, request, queryset):
        queryset.update(is_default=False)
        queryset.update(is_default=True)
        self.message_user(request, "سال تحصیلی انتخاب‌شده به عنوان پیش‌فرض تنظیم شد.")
    make_default.short_description = "تنظیم به عنوان سال پیش‌فرض"

admin.site.register(School)
admin.site.register(ClassRoom)
admin.site.register(Student)