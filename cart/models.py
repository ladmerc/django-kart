from django.db import models
from django.utils.translation import ugettext_lazy as _


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')
        ordering = ('-created_at',)

    def __str__(self):
        return unicode(self.id)
