# core/admin.py
from django.contrib import admin
from .models import School, ClassRoom, Student


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_gender_display', 'get_level_display', 'education_manager', 'manager_phone', 'contract_date']
    list_filter = ['gender', 'level']
    search_fields = ['name', 'education_manager']
    date_hierarchy = 'contract_date'  # برای فیلتر تاریخ قرارداد
    readonly_fields = ['created_at', 'updated_at']  # فقط نمایش، نه ویرایش

    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('name', 'gender', 'level')
        }),
        ('اطلاعات تماس', {
            'fields': ('address', 'education_manager', 'manager_phone')
        }),
        ('قرارداد و ظاهر', {
            'fields': ('contract_date', 'fabric_color_image')
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at', 'description'),
            'classes': ('collapse',)
        }),
    )


admin.site.register(ClassRoom)
admin.site.register(Student)