from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from apps.site.models import SiteConfiguration


class FeaturedLimitValidationTests(TestCase):
    def test_limit_rejects_values_outside_range_in_forms(self):
        for limit in (0, 13):
            with self.subTest(limit=limit), self.assertRaises(ValidationError) as error:
                SiteConfiguration(featured_products_limit=limit).full_clean()
            self.assertIn("featured_products_limit", error.exception.message_dict)

    def test_limit_rejects_invalid_direct_database_updates(self):
        configuration = SiteConfiguration.objects.create()
        for limit in (0, 13):
            with self.subTest(limit=limit), self.assertRaises(IntegrityError), transaction.atomic():
                SiteConfiguration.objects.filter(pk=configuration.pk).update(featured_products_limit=limit)
