from datetime import datetime, timedelta
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils import timezone

from shops.models.shop_admins import ShopAdmin
from shops.models.shops import Shop

__all__ = ('SalesmanInvitation',)


class SalesmanInvitation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    shop = models.ForeignKey(
        to=Shop,
        on_delete=models.CASCADE,
    )
    created_by_admin = models.ForeignKey(
        to=ShopAdmin,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'invitation'
        verbose_name_plural = 'invitations'


    @property
    def expires_at(self) -> datetime:
        return self.created_at + timedelta(
            seconds=settings.SALESMAN_INVITATION_LIFETIME_SECONDS,
        )

    @property
    def is_expired(self) -> bool:
        return self.expires_at < timezone.now()
