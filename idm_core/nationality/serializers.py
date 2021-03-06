from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from idm_core.attestation.serializers import Attestable
from idm_core.person.models import Person
from . import models


class CountrySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:country-detail')

    class Meta:
        model = models.Country
        exclude = ('people',)


class NationalitySerializer(Attestable, serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:nationality-detail')
    country = CountrySerializer()

    class Meta:
        model = models.Nationality
        exclude = ('identity',)

    def to_internal_value(self, data):
        try:
            country = data['country']
        except KeyError:
            raise ValidationError("country must be provided")
        try:
            if isinstance(country, int):
                country = models.Country.objects.get(id=country)
            elif isinstance(country, str) and len(country) == 2:
                country = models.Country.objects.get(alpha_2=country)
            elif isinstance(country, str) and country.isdigit() and len(country) == 3:
                country = models.Country.objects.get(numeric=country)
            elif isinstance(country, str) and len(country) == 3:
                country = models.Country.objects.get(alpha_3=country)
            else:
                raise ValidationError("country must be provided")
        except models.Country.DoesNotExist as e:
            raise ValidationError("No such country") from e
        return {'country': country}


class EmbeddedNationalitySerializer(NationalitySerializer):
    identity = serializers.HyperlinkedRelatedField(queryset=Person.objects.all(), view_name='api:person-detail')

    class Meta(NationalitySerializer.Meta):
        exclude = ('attestations',)
