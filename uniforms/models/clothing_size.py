# uniforms/models/clothing_size.py
from django.db import models

from core.models import BaseModel
from .clothing_type import ClothingType


class ClothingSize(BaseModel):
    clothing_type = models.ForeignKey(
        ClothingType,
        on_delete=models.PROTECT,
        related_name='sizes',
        verbose_name="نوع لباس"
    )
    size = models.CharField(max_length=10, verbose_name="سایز")

    class Meta:
        unique_together = ['clothing_type', 'size']
        verbose_name = "سایز لباس"
        verbose_name_plural = "سایزهای لباس"
        ordering = ['clothing_type', 'size']

    def __str__(self):
        return f"{self.size} ({self.clothing_type})"