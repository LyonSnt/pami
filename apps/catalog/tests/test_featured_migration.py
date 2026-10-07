from importlib import import_module
from types import SimpleNamespace

from django.apps import apps
from django.db import connection
from django.test import TestCase

from apps.businesses.models import Business
from apps.catalog.models import Product


class FeaturedProductsMigrationTests(TestCase):
    def test_initial_selection_preserves_first_two_public_products_per_public_line(self):
        public = Business.objects.create(name="Prendas", slug="prendas")
        other = Business.objects.create(name="Papelería", slug="papeleria")
        hidden = Business.objects.create(name="Oculta", slug="oculta", is_published=False)
        first = Product.objects.create(business=public, name="Primero", slug="primero", order=1)
        second = Product.objects.create(business=public, name="Segundo", slug="segundo", order=2)
        third = Product.objects.create(business=public, name="Tercero", slug="tercero", order=3)
        inactive = Product.objects.create(business=public, name="Inactivo", slug="inactivo", order=0, is_active=False)
        draft = Product.objects.create(business=public, name="Borrador", slug="borrador", order=0, is_published=False)
        other_product = Product.objects.create(business=other, name="Agenda", slug="agenda")
        hidden_product = Product.objects.create(business=hidden, name="Oculto", slug="oculto")
        initial = list(Product.objects.values_list("pk", "business_id", "slug", "order", "is_published"))
        migration = import_module("apps.catalog.migrations.0006_preserve_current_featured_products")
        migration.preserve_featured_products(apps, SimpleNamespace(connection=connection))
        self.assertEqual(
            set(Product.objects.filter(is_featured=True).values_list("pk", flat=True)),
            {first.pk, second.pk, other_product.pk},
        )
        self.assertEqual(list(Product.objects.values_list("pk", "business_id", "slug", "order", "is_published")), initial)
        self.assertFalse(Product.objects.filter(pk__in=[third.pk, inactive.pk, draft.pk, hidden_product.pk], is_featured=True).exists())
