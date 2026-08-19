from django.test import TestCase
from django.urls import reverse

from .models import Quote, Theme, TranslationOrigin


def make_quote(**overrides):
    defaults = {
        "text": "Le monde est cruel, et pourtant magnifique.",
        "character": "Mikasa Ackerman",
        "series": "Attack on Titan",
        "theme": Theme.WISDOM,
    }
    defaults.update(overrides)
    return Quote.objects.create(**defaults)


class QuoteModelTests(TestCase):
    def test_str_uses_character_and_series(self):
        quote = make_quote()
        self.assertEqual(str(quote), "Mikasa Ackerman — Attack on Titan")

    def test_ordering_is_series_then_character(self):
        make_quote(character="Zeta", series="Bravo", text="a")
        make_quote(character="Alpha", series="Alpha", text="b")
        make_quote(character="Alpha", series="Bravo", text="c")

        ordered = list(Quote.objects.values_list("series", "character"))
        self.assertEqual(
            ordered,
            [("Alpha", "Alpha"), ("Bravo", "Alpha"), ("Bravo", "Zeta")],
        )

    def test_source_and_theme_are_optional(self):
        quote = Quote.objects.create(
            text="Une citation sans source ni thème.",
            character="Inconnu",
            series="Série X",
        )
        self.assertEqual(quote.source, "")
        self.assertEqual(quote.theme, "")

    def test_text_fr_and_fr_origin_default_to_blank(self):
        quote = make_quote()
        self.assertEqual(quote.text_fr, "")
        self.assertEqual(quote.fr_origin, "")

    def test_text_fr_can_be_set_with_an_origin(self):
        quote = make_quote(
            text_fr="Le monde est cruel, et pourtant magnifique.",
            fr_origin=TranslationOrigin.ASSISTED,
        )
        self.assertEqual(quote.fr_origin, "assisted")


class HomeViewTests(TestCase):
    def test_home_with_no_quotes_renders_without_error(self):
        response = self.client.get(reverse("quotes:home"))
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context["quote"])

    def test_home_renders_french_translation_when_present(self):
        make_quote(text_fr="Traduction test.", fr_origin=TranslationOrigin.ASSISTED)
        response = self.client.get(reverse("quotes:home"))
        self.assertContains(response, "Traduction test.")
        self.assertContains(response, 'data-quote-text="fr"')

    def test_home_returns_a_quote_when_available(self):
        make_quote()
        response = self.client.get(reverse("quotes:home"))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context["quote"])


class BrowseViewTests(TestCase):
    def setUp(self):
        self.q1 = make_quote(
            text="I mustn't run away.",
            character="Shinji Ikari",
            series="Neon Genesis Evangelion",
            theme=Theme.DETERMINATION,
        )
        self.q2 = make_quote(
            text="Whatever happens, happens.",
            character="Spike Spiegel",
            series="Cowboy Bebop",
            theme=Theme.FREEDOM,
        )
        self.q3 = make_quote(
            text="Set your heart ablaze!",
            character="Kyojuro Rengoku",
            series="Demon Slayer",
            theme=Theme.DETERMINATION,
        )

    def test_browse_lists_all_quotes_by_default(self):
        response = self.client.get(reverse("quotes:browse"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_obj"].paginator.count, 3)

    def test_search_filters_by_text_character_or_series(self):
        response = self.client.get(reverse("quotes:browse"), {"q": "Spike"})
        results = list(response.context["page_obj"])
        self.assertEqual(results, [self.q2])

    def test_search_is_case_insensitive_and_matches_series(self):
        response = self.client.get(reverse("quotes:browse"), {"q": "cowboy"})
        results = list(response.context["page_obj"])
        self.assertEqual(results, [self.q2])

    def test_filter_by_series_exact(self):
        response = self.client.get(reverse("quotes:browse"), {"series": "Demon Slayer"})
        results = list(response.context["page_obj"])
        self.assertEqual(results, [self.q3])

    def test_filter_by_theme_exact(self):
        response = self.client.get(reverse("quotes:browse"), {"theme": Theme.DETERMINATION})
        results = set(response.context["page_obj"])
        self.assertEqual(results, {self.q1, self.q3})

    def test_combined_filters_are_all_applied(self):
        response = self.client.get(
            reverse("quotes:browse"),
            {"theme": Theme.DETERMINATION, "series": "Demon Slayer"},
        )
        results = list(response.context["page_obj"])
        self.assertEqual(results, [self.q3])

    def test_no_match_renders_empty_state_without_error(self):
        response = self.client.get(reverse("quotes:browse"), {"q": "nonexistent-xyz"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_obj"].paginator.count, 0)

    def test_base_query_excludes_page_but_keeps_other_filters(self):
        response = self.client.get(reverse("quotes:browse"), {"q": "run", "page": "1"})
        self.assertIn("q=run", response.context["base_query"])
        self.assertNotIn("page=", response.context["base_query"])

    def test_pagination_splits_results_across_pages(self):
        Quote.objects.all().delete()
        for i in range(25):
            make_quote(text=f"Citation numéro {i}", character=f"Perso {i}", series="Série Longue")

        page1 = self.client.get(reverse("quotes:browse"))
        self.assertEqual(len(page1.context["page_obj"]), 12)
        self.assertTrue(page1.context["page_obj"].has_next())

        page3 = self.client.get(reverse("quotes:browse"), {"page": "3"})
        self.assertEqual(len(page3.context["page_obj"]), 1)
        self.assertFalse(page3.context["page_obj"].has_next())


class QuoteDetailViewTests(TestCase):
    def test_detail_renders_existing_quote(self):
        quote = make_quote()
        response = self.client.get(reverse("quotes:detail", args=[quote.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, quote.character)

    def test_detail_404s_for_missing_quote(self):
        response = self.client.get(reverse("quotes:detail", args=[9999]))
        self.assertEqual(response.status_code, 404)


class QuoteApiTests(TestCase):
    def setUp(self):
        self.q1 = make_quote(
            text="I am justice!",
            character="Light Yagami",
            series="Death Note",
            theme=Theme.AMBITION,
        )
        self.q2 = make_quote(
            text="Yare yare daze.",
            character="Jotaro Kujo",
            series="JoJo's Bizarre Adventure",
            theme=Theme.DEFIANCE,
        )

    def test_list_endpoint_returns_all_quotes(self):
        response = self.client.get("/api/quotes/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 2)

    def test_list_endpoint_respects_filters(self):
        response = self.client.get("/api/quotes/", {"series": "Death Note"})
        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["character"], "Light Yagami")

    def test_detail_endpoint_returns_single_quote(self):
        response = self.client.get(f"/api/quotes/{self.q1.pk}/")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["character"], "Light Yagami")
        self.assertEqual(body["theme_label"], "Ambition")

    def test_detail_endpoint_404s_for_missing_quote(self):
        response = self.client.get("/api/quotes/9999/")
        self.assertEqual(response.status_code, 404)

    def test_detail_endpoint_exposes_french_translation_fields(self):
        translated = make_quote(
            character="Test Character",
            series="Test Series",
            text_fr="Version française.",
            fr_origin=TranslationOrigin.ASSISTED,
        )
        response = self.client.get(f"/api/quotes/{translated.pk}/")
        body = response.json()
        self.assertEqual(body["text_fr"], "Version française.")
        self.assertEqual(body["fr_origin"], "assisted")
        self.assertEqual(body["fr_origin_label"], "Traduction assistée (non vérifiée)")

    def test_random_endpoint_returns_one_of_the_matching_quotes(self):
        response = self.client.get("/api/quotes/random/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.json()["character"], {"Light Yagami", "Jotaro Kujo"})

    def test_random_endpoint_respects_filters(self):
        response = self.client.get("/api/quotes/random/", {"theme": Theme.DEFIANCE})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["character"], "Jotaro Kujo")

    def test_random_endpoint_404s_when_no_quote_matches(self):
        response = self.client.get("/api/quotes/random/", {"q": "nonexistent-xyz"})
        self.assertEqual(response.status_code, 404)
        self.assertIn("detail", response.json())


class SeedCommandTests(TestCase):
    def test_seed_command_is_idempotent(self):
        from django.core.management import call_command

        call_command("seed_quotes")
        first_count = Quote.objects.count()
        self.assertGreater(first_count, 0)

        call_command("seed_quotes")
        second_count = Quote.objects.count()
        self.assertEqual(first_count, second_count)
