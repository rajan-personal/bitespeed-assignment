from django.db import models
from django.utils.translation import gettext_lazy as _

class TimeStampedModel(models.Model):
    createdAt = models.DateTimeField(_('createdAt'),auto_now_add=True)
    updatedAt = models.DateTimeField(_('updatedAt'),auto_now=True)
    deletedAt = models.DateTimeField(_('deletedAt'), blank=True, null=True)

    class Meta:
        abstract = True

class Orders(TimeStampedModel):
    class LinkPrecedence(models.IntegerChoices):
        PRIMARY = 1, _('Primary')
        SECONDARY = 2, _('Secondary')

    phoneNumber = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    linkedId = models.IntegerField(blank=True, null=True)
    linkPrecedence = models.PositiveSmallIntegerField(
        choices=LinkPrecedence.choices
    )