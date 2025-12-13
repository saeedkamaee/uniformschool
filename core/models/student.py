# core/models/student.py
from django.db import models
from django.core.validators import RegexValidator

from .base_model import BaseModel


class Student(BaseModel):
    first_name = models.CharField(max_length=100, verbose_name="نام")
    last_name = models.CharField(max_length=100, verbose_name="نام خانوادگی")
    national_id = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(r'^\d{10}$', 'کد ملی باید دقیقاً ۱۰ رقم باشد.')],
        verbose_name="کد ملی"
    )
    phone = models.CharField(
        max_length=11,
        validators=[RegexValidator(r'^09\d{9}$', 'شماره موبایل باید با ۰۹ شروع شود و ۱۱ رقم باشد.')],
        verbose_name="شماره موبایل"
    )
    class_room = models.ForeignKey(
        'ClassRoom',
        on_delete=models.PROTECT,
        related_name='students',
        verbose_name="کلاس"
    )

    class Meta:
        verbose_name = "دانش‌آموز"
        verbose_name_plural = "دانش‌آموزان"
        ordering = ['last_name', 'first_name']  # مرتب‌سازی بر اساس نام خانوادگی و سپس نام
        unique_together = ['class_room', 'national_id']  # جلوگیری از تکرار دانش‌آموز در یک کلاس

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.national_id}) - {self.class_room}"

    @property
    def full_name(self):
        """برای مواقعی که بخوایم نام کامل رو یکجا داشته باشیم (مثل فرم‌ها یا نمایش)"""
        return f"{self.first_name} {self.last_name}".strip()