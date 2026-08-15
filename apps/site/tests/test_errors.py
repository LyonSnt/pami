from django.test import RequestFactory, TestCase, override_settings
from django.views.defaults import server_error


@override_settings(DEBUG=False)
class PublicErrorPageTests(TestCase):
    def test_not_found_page_uses_branding_and_correct_status(self):
        response = self.client.get("/pagina-que-no-existe/")

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "No encontramos esta página", status_code=404)
        self.assertContains(
            response,
            'name="robots" content="noindex, nofollow"',
            status_code=404,
        )
        self.assertContains(response, 'href="/buscar/"', status_code=404)

    def test_server_error_page_is_independent_and_uses_correct_status(self):
        request = RequestFactory().get("/error-interno/")

        with self.assertNumQueries(0):
            response = server_error(request)

        self.assertEqual(response.status_code, 500)
        self.assertContains(
            response,
            "Algo no salió como esperábamos",
            status_code=500,
        )
        self.assertContains(
            response,
            'name="robots" content="noindex, nofollow"',
            status_code=500,
        )
