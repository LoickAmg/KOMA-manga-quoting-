from django.db import models


class Theme(models.TextChoices):
    """Thème dominant de la citation — sert au filtrage, pas à imposer une
    icône ou une couleur par thème (on garde une seule teinte d'accent)."""

    DETERMINATION = "determination", "Détermination"
    LOSS = "loss", "Perte"
    FRIENDSHIP = "friendship", "Amitié"
    AMBITION = "ambition", "Ambition"
    WISDOM = "wisdom", "Sagesse"
    DEFIANCE = "defiance", "Défi"
    FREEDOM = "freedom", "Liberté"
    FEAR = "fear", "Peur"


class TranslationOrigin(models.TextChoices):
    """D'où vient la traduction française — affiché dans l'UI pour rester
    honnête sur la fiabilité : une traduction communautaire vérifiée n'a
    pas la même valeur qu'une traduction générée qui n'a pas été relue par
    un locuteur natif ou comparée au doublage/sous-titrage officiel."""

    COMMUNITY = "community", "Traduction communautaire"
    ASSISTED = "assisted", "Traduction assistée (non vérifiée)"


class Quote(models.Model):
    text = models.TextField()
    text_fr = models.TextField(
        blank=True,
        help_text="Traduction française. Voir fr_origin pour sa provenance/fiabilité.",
    )
    fr_origin = models.CharField(
        max_length=20,
        choices=TranslationOrigin.choices,
        blank=True,
        help_text="Provenance de text_fr — laissé vide si aucune traduction n'existe.",
    )
    character = models.CharField(max_length=120)
    series = models.CharField(max_length=120)
    source = models.CharField(
        max_length=120,
        blank=True,
        help_text="Ex. 'Chapitre 24', 'Épisode 5, saison 1'.",
    )
    theme = models.CharField(max_length=20, choices=Theme.choices, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["series", "character"]

    def __str__(self) -> str:
        return f"{self.character} — {self.series}"
