from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Max

from idm_core.attestation.mixins import Attestable
from idm_core.relationship.models import Affiliation
from idm_core.identity.models import Identity


class ContactContext(models.Model):
    id = models.SlugField(primary_key=True)
    label = models.CharField(max_length=255)


class Contact(Attestable, models.Model):
    identity_content_type = models.ForeignKey(ContentType)
    identity_id = models.UUIDField()
    identity = GenericForeignKey('identity_content_type', 'identity_id')

    validated = models.BooleanField(default=False)
    affiliation = models.ForeignKey(Affiliation, null=True, blank=True)
    context = models.ForeignKey(ContactContext)
    order = models.PositiveSmallIntegerField()

    class Meta:
        abstract = True
        unique_together = (('identity_content_type', 'identity_id', 'order'),)
        ordering = ('identity_content_type', 'identity_id', 'order')

    def save(self, *args, **kwargs):
        from .mixins import Contactable
        assert isinstance(self.identity, Contactable)

        if not self.order:
            c = type(self).objects.filter(identity_content_type=self.identity_content_type,
                                          identity_id=self.identity_id).aggregate(Max('order')).get('order__max')
            self.order = 0 if c is None else c + 1
        return super().save(*args, **kwargs)


class Email(Contact):
    value = models.EmailField()


class Telephone(Contact):
    value = models.EmailField()


class Address(Contact):
    pass


class OnlineAccount(Contact):
    pass

