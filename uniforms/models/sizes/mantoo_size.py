# uniforms/models/sizes/mantoo_size.py
from django.db import models
from core.models import BaseModel


class MantooSize(BaseModel):
    MANTOO_SIZES = [
        ('22', '۲۲'),
        ('24', '۲۴'),
        ('26', '۲۶'),
        ('28', '۲۸'),
        ('30', '۳۰'),
        ('32', '۳۲'),
        ('34', '۳۴'),
        ('36', '۳۶'),
        ('38', '۳۸'),
        ('40', '۴۰'),
        ('42', '۴۲'),
        ('44', '۴۴'),
        ('46', '۴۶'),
        ('48', '۴۸'),
        ('50', '۵۰'),
    ]

    size = models.CharField(max_length=10, choices=MANTOO_SIZES, unique=True, verbose_name="سایز مانتو")

    class Meta:
        verbose_name = "سایز مانتو"
        verbose_name_plural = "سایزهای مانتو"

    def __str__(self):
        return self.size