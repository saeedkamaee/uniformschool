# uniforms/models/agreed_price.py
from django.db import models
from django.core.exceptions import ValidationError

from core.models import BaseModel, School
from .clothing_size import ClothingSize


class AgreedPrice(BaseModel):
    school = models.ForeignKey(
        School,
        on_delete=models.PROTECT,
        related_name='agreed_prices',
        verbose_name="مدرسه"
    )
    clothing_size = models.ForeignKey(
        ClothingSize,
        on_delete=models.PROTECT,
        related_name='prices',
        verbose_name="سایز لباس"
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
        """مبلغ نهایی (توافقی منهای علی‌الحساب)"""
        return self.agreed_amount - self.advance_amount

    class Meta:
        unique_together = ['school', 'clothing_size']
        verbose_name = "قیمت توافقی"
        verbose_name_plural = "قیمت‌های توافقی"

    def clean(self):
        super().clean()
        # چک تطابق جنسیت لباس با جنسیت مدرسه
        if self.school.gender != self.clothing_size.clothing_type.gender:
            raise ValidationError(
                f"جنسیت لباس ({self.clothing_size.clothing_type.get_gender_display()}) "
                f"با جنسیت مدرسه ({self.school.get_gender_display()}) همخوانی ندارد."
            )
        # چک مبلغ علی‌الحساب بیشتر از توافقی نباشد
        if self.advance_amount > self.agreed_amount:
            raise ValidationError("مبلغ علی‌الحساب نمی‌تواند بیشتر از مبلغ توافقی باشد.")

    def __str__(self):
        return f"{self.clothing_size} - {self.school.name}: {self.agreed_amount:,} تومان"