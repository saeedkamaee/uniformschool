# core/models/academic_year.py
from django.db import models
from django.core.exceptions import ValidationError

from core.models.base_model import BaseModel


class AcademicYear(BaseModel):
    year = models.CharField(max_length=9, unique=True, verbose_name="سال تحصیلی")
    is_default = models.BooleanField(default=False, verbose_name="سال پیش‌فرض")
    start_date = models.DateField(verbose_name="تاریخ شروع")
    end_date = models.DateField(verbose_name="تاریخ پایان")

    class Meta:
        verbose_name = "سال تحصیلی"
        verbose_name_plural = "سال‌های تحصیلی"
        ordering = ['-year']
        # مهم: فقط یک رکورد می‌تواند is_default=True باشد
        constraints = [
            models.UniqueConstraint(
                fields=['is_default'],
                condition=models.Q(is_default=True),
                name='unique_default_academic_year'
            )
        ]

    def clean(self):
        super().clean()
        # چک اضافی (اختیاری، برای فرم‌ها و ادمین)
        if self.is_default and AcademicYear.objects.filter(is_default=True).exclude(pk=self.pk).exists():
            raise ValidationError("فقط یک سال تحصیلی می‌تواند پیش‌فرض باشد.")

    def save(self, *args, **kwargs):
        if self.is_default:
            # اگر این رکورد پیش‌فرض شد، همه قبلی‌ها را غیرپیش‌فرض کن
            AcademicYear.objects.filter(is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.year