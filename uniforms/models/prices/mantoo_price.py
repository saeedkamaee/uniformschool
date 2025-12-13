# uniforms/models/prices/mantoo_price.py
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import DecimalField

from core.models import BaseModel, School
from ..sizes.mantoo_size import MantooSize


class AgreedMantooPrice(BaseModel):
    school = models.ForeignKey(
        School,
        on_delete=models.PROTECT,
        limit_choices_to={'gender': 'F'},  # فقط مدارس دخترانه
        related_name='mantoo_prices',
        verbose_name="مدرسه"
    )
    size = models.ForeignKey(
        MantooSize,
        on_delete=models.PROTECT,
        related_name='prices',
        verbose_name="سایز مانتو"
    )
    agreed_amount = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name="مبلغ توافقی کل"
    )
    advance_amount = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name="مبلغ علی‌الحساب"
    )

    @property
    def final_amount(self):
        """مبلغ نهایی (اتوماتیک محاسبه می‌شود)"""
        return self.agreed_amount - self.advance_amount

    class Meta:
        unique_together = ['school', 'size']
        verbose_name = "قیمت توافقی مانتو"
        verbose_name_plural = "قیمت‌های توافقی مانتو"

    def clean(self):
        if self.advance_amount > self.agreed_amount:
            raise ValidationError("مبلغ علی‌الحساب نمی‌تواند بیشتر از مبلغ توافقی باشد.")

    def __str__(self):
        return f"مانتو {self.size} - {self.school.name}: {self.agreed_amount:,} تومان"