# uniforms/models/sizes/pants_size.py
from django.db import models
from core.models import BaseModel


class PantsSize(BaseModel):
    PANTS_SIZES = [
        ('36', '۳۶'),
        ('38', '۳۸'),
        ('40', '۴۰'),
        ('42', '۴۲'),
        ('44', '۴۴'),
        ('46', '۴۶'),
        ('48', '۴۸'),
        ('50', '۵۰'),
        ('52', '۵۲'),
        ('54', '۵۴'),
        ('56', '۵۶'),
        ('58', '۵۸'),
        ('100', '۱۰۰'),
        ('105', '۱۰۵'),
    ]

    size = models.CharField(max_length=10, choices=PANTS_SIZES, unique=True, verbose_name="سایز شلوار")

    class Meta:
        verbose_name = "سایز شلوار"
        verbose_name_plural = "سایزهای شلوار"

    def __str__(self):
        return self.size