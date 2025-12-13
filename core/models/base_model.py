# core/models/base_model.py
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")

    class Meta:
        abstract = True
        ordering = ['-created_at']