from django.template.loader import render_to_string
from django.test import RequestFactory, TestCase
from django.urls import reverse

from apps.site.context_processors import (
    _is_current_internal_path,
    site_configuration,
)
from apps.site.models import NavigationItem


class NavigationStateTests(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def test_parent_navigation_item_is_current_on_detail_path(self):
        NavigationItem.objects.create(
            label="Portafolio",
            url="/portafolio/",
            order=1,
        )
        request = self.request_factory.get(
            "/portafolio/confecciones/coleccion-inicial/"
        )
        context = site_configuration(request)

        html = render_to_string("base/_navigation.html", context)

        self.assertIn('href="/portafolio/"', html)
        self.assertIn('aria-current="page"', html)
        self.assertTrue(context["navigation_items"][0].is_current)

    def test_home_is_only_current_on_root_path(self):
        home_context = site_configuration(self.request_factory.get("/"))
        detail_context = site_configuration(
            self.request_factory.get("/catalogo/confecciones/chaquetas/")
        )

        self.assertTrue(home_context["home_is_current"])
        self.assertFalse(detail_context["home_is_current"])

    def test_external_and_similar_paths_are_not_marked_current(self):
        self.assertFalse(
            _is_current_internal_path("/blog/articulo/", "https://example.com/blog/")
        )
        self.assertFalse(_is_current_internal_path("/blog-extra/", "/blog/"))

    def test_search_accesses_are_marked_current(self):
        response = self.client.get(reverse("site:search"))

        self.assertContains(response, 'aria-label="Buscar en Pámi"')
        self.assertContains(response, 'aria-current="page"', count=2)

    def test_contact_accesses_are_marked_current(self):
        response = self.client.get(reverse("contact:form"))

        self.assertContains(response, 'aria-current="page"', count=2)

    def test_mobile_navigation_exposes_interaction_hooks(self):
        response = self.client.get(reverse("site:home"))

        self.assertContains(response, "data-mobile-navigation")
        self.assertContains(response, "data-mobile-navigation-toggle")
        self.assertContains(response, 'aria-expanded="false"')
        self.assertContains(response, 'event.key === "Escape"')
        self.assertContains(response, 'event.target.closest("a")')
