# uniforms/models/prices/maghnaeh_price.py
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import DecimalField

from core.models import BaseModel, School
from ..sizes.maghnaeh_size import MaghnaehSize


class AgreedMaghnaehPrice(BaseModel):
    school = models.ForeignKey(
        School,
        on_delete=models.PROTECT,
        limit_choices_to={'gender': 'F'},  # فقط مدارس دخترانه
        related_name='maghnaeh_prices',
        verbose_name="مدرسه"
    )
    size = models.ForeignKey(
        MaghnaehSize,
        on_delete=models.PROTECT,
        related_name='prices',
        verbose_name="سایز مقنعه"
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
        verbose_name = "قیمت توافقی مقنعه"
        verbose_name_plural = "قیمت‌های توافقی مقنعه"

    def clean(self):
        if self.advance_amount > self.agreed_amount:
            raise ValidationError("مبلغ علی‌الحساب نمی‌تواند بیشتر از مبلغ توافقی باشد.")

    def __str__(self):
        return f"مقنعه {self.size} - {self.school.name}: {self.agreed_amount:,} تومان"