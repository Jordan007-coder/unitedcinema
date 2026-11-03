from django.db import models
from django.contrib.auth.models import User

class Film(models.Model):
    STATUS_CHOICES = [
        ('now_showing', 'Actuellement en salle'),
        ('upcoming', 'Prochainement'),
    ]

    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='now_showing', help_text="En salle ou sortie future")
    release_date = models.DateField(null=True, blank=True, help_text="Date exacte de sortie (pour le tri chronologique)")
    date_out = models.CharField(max_length=100, blank=True)
    synopsis = models.TextField()
    genre = models.CharField(max_length=100)
    format_type = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    thumb = models.ImageField(null=True, blank=True, upload_to='media')
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class WeeklySchedule(models.Model):
    title = models.CharField(
        max_length=200, 
        default="Programme de la Semaine",
        help_text="ex: Programme de la Semaine du 11 au 17 Septembre 2026"
    )
    start_date = models.DateField(null=True, blank=True, help_text="Date de début (ex: 2026-09-11)")
    end_date = models.DateField(null=True, blank=True, help_text="Date de fin (ex: 2026-09-17)")
    poster = models.ImageField(upload_to='schedules/', null=True, blank=True, help_text="Affiche officielle du programme")
    subtitle = models.CharField(
        max_length=300, 
        default="Consultez l'affiche officielle des séances, horaires et tarifs de la semaine en cours."
    )
    notice = models.CharField(
        max_length=300, 
        blank=True, 
        default="🎬 Navette gratuite Ahala ↔ Mbankomo pour toutes les séances à partir de 18h00 !"
    )
    
    # Pricing tags
    price_standard = models.CharField(max_length=50, default="3 000 XAF")
    price_under_12 = models.CharField(max_length=50, default="1 500 XAF")
    price_glasses_3d = models.CharField(max_length=50, default="1 500 XAF")
    price_premiere = models.CharField(max_length=50, default="5 000 XAF")
    price_avant_premiere = models.CharField(max_length=50, default="5 000 XAF")
    
    is_active = models.BooleanField(default=True, help_text="Afficher ce programme sur le site public")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class PackageCategory(models.Model):
    LAYOUT_CHOICES = [
        ('stack', 'Pile verticale de cartes (ex: Loisirs)'),
        ('grid', 'Grille de cartes (ex: Spa, Week-end Détente)'),
    ]

    name = models.CharField(max_length=150, help_text="ex: Packages Loisirs & Évasion, Beauté, Spa & Bien-être, Week-end Détente")
    slug = models.SlugField(max_length=150, unique=True, blank=True, help_text="Identifiant URL unique (ex: loisir-evasion). Généré automatiquement.")
    badge = models.CharField(max_length=150, blank=True, help_text="ex: Divertissement & Sensations, 🏨 Séjour & Détente Hôtel 4 Étoiles")
    subtitle = models.CharField(max_length=350, blank=True, help_text="Sous-titre ou description courte de la catégorie")
    notice = models.CharField(max_length=350, blank=True, help_text="Bandeau d'information spécifique (optionnel)")
    flyer_image = models.ImageField(upload_to='packages/flyers/', null=True, blank=True, help_text="Grande affiche / Flyer officiel de la catégorie")
    flyer_title = models.CharField(max_length=150, blank=True, default="Affiche Officielle", help_text="Titre au-dessus de l'affiche")
    layout_type = models.CharField(max_length=30, choices=LAYOUT_CHOICES, default='grid', help_text="Disposition des cartes de packages")
    order = models.PositiveIntegerField(default=0, help_text="Ordre d'affichage de la section (0 = en premier)")
    is_active = models.BooleanField(default=True, help_text="Afficher cette catégorie sur le site public")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Catégorie de Package"
        verbose_name_plural = "Catégories de Packages"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        if not self.slug:
            base_slug = slugify(self.name) or "categorie"
            slug = base_slug
            counter = 1
            while PackageCategory.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def active_packages(self):
        return self.packages.filter(is_active=True).order_by('order', 'price', 'name')

    @property
    def get_flyer_url(self):
        if self.flyer_image:
            try:
                return self.flyer_image.url
            except ValueError:
                pass
        # Si un package rattaché possède une image propre, on l'utilise en priorité
        for pkg in self.packages.filter(is_active=True).exclude(image='').exclude(image__isnull=True):
            if pkg.get_image_url:
                return pkg.get_image_url
        if self.slug in ['loisirs-evasion', 'loisir', 'loisirs']:
            return '/static/images/packages/flyer_loisir_evasion.jpg'
        if self.slug in ['beaute-spa', 'spa']:
            return '/static/images/packages/flyer_beaute_spa.jpg'
        if self.slug in ['weekend-detente', 'weekend']:
            return '/static/images/packages/flyer_weekend_detente.jpg'
        return '/static/images/packages/flyer_loisir_evasion.jpg'


class Package(models.Model):
    category = models.ForeignKey(
        PackageCategory, 
        on_delete=models.CASCADE, 
        related_name='packages',
        null=True, 
        blank=True,
        help_text="Catégorie parente de ce package"
    )
    name = models.CharField(max_length=150, help_text="ex: PACKAGE LOISIR, PACK II, Pack Couple...")
    slug = models.SlugField(max_length=150, unique=True, blank=True, help_text="Identifiant unique (ex: package-loisir). Généré automatiquement.")
    subtitle = models.CharField(max_length=200, blank=True, help_text="ex: Fraîcheur & Bien-être, 2 personnes...")
    badge = models.CharField(max_length=100, blank=True, help_text="ex: Formule Conviviale, ⭐ Best-Seller Tout Inclus")
    price = models.PositiveIntegerField(default=5000, help_text="Tarif en FCFA (chiffre uniquement, ex: 5000)")
    price_display = models.CharField(max_length=100, blank=True, help_text="Affichage personnalisé (ex: 5 000 FCFA). Si vide, sera généré.")
    tagline = models.CharField(max_length=350, blank=True, help_text="Description courte / accroche")
    image = models.ImageField(upload_to='packages/items/', null=True, blank=True, help_text="Photo / visuel spécifique du package (champ séparé de l'affiche de la catégorie)")
    features_text = models.TextField(
        blank=True, 
        help_text="Une prestation par ligne au format : Icône | Nom | Description | VIP (optionnel)"
    )
    highlight = models.BooleanField(default=False, help_text="Mettre en avant ce package avec une bordure dorée (Best-seller)")
    transport_included = models.BooleanField(default=False, help_text="Navette aller-retour incluse")
    is_active = models.BooleanField(default=True, help_text="Afficher ce package sur le site public")
    order = models.PositiveIntegerField(default=0, help_text="Ordre d'affichage au sein de la catégorie (0 = en premier)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'price', 'name']
        verbose_name = "Package"
        verbose_name_plural = "Packages"

    def __str__(self):
        return f"{self.name} ({self.get_price_display})"

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        if not self.slug:
            base_slug = slugify(self.name) or "package"
            slug = base_slug
            counter = 1
            while Package.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        if not self.price_display:
            self.price_display = f"{self.price:,}".replace(",", " ") + " FCFA"
        super().save(*args, **kwargs)

    @property
    def get_price_display(self):
        if self.price_display:
            return self.price_display
        return f"{self.price:,}".replace(",", " ") + " FCFA"

    @property
    def get_image_url(self):
        if self.image:
            try:
                return self.image.url
            except ValueError:
                pass
        return None

    @property
    def get_display_thumbnail_url(self):
        """
        URL du visuel à afficher pour ce package (tableau de bord, cartes, modales).
        Renvoie son image propre s'il en a une, sinon l'affiche de sa catégorie parente.
        """
        if self.get_image_url:
            return self.get_image_url
        if self.category:
            return self.category.get_flyer_url
        return None

    @property
    def features(self):
        """
        Convertit features_text en liste d'objets pour les templates :
        [{'icon': '🏊‍♂️', 'name': 'PISCINE', 'desc': '...', 'vip': False}]
        """
        if not self.features_text:
            return []
        result = []
        for line in self.features_text.splitlines():
            line = line.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split('|')]
            if len(parts) == 1:
                result.append({'icon': '✓', 'name': parts[0], 'desc': '', 'vip': False})
            elif len(parts) == 2:
                if len(parts[0]) <= 4:
                    result.append({'icon': parts[0], 'name': parts[1], 'desc': '', 'vip': False})
                else:
                    result.append({'icon': '✓', 'name': parts[0], 'desc': parts[1], 'vip': False})
            elif len(parts) == 3:
                result.append({'icon': parts[0], 'name': parts[1], 'desc': parts[2], 'vip': False})
            else:
                is_vip = parts[3].lower() in ['vip', 'true', '1', 'oui', 'yes']
                result.append({'icon': parts[0], 'name': parts[1], 'desc': parts[2], 'vip': is_vip})
        return result


class WeekendPackage(models.Model):
    title = models.CharField(
        max_length=150, 
        default="WEEK-END DÉTENTE",
        help_text="ex: WEEK-END DÉTENTE"
    )
    duration = models.CharField(
        max_length=150, 
        default="02 Nuitées (Vendredi - Samedi - Dimanche)",
        help_text="ex: 02 Nuitées (Vendredi - Samedi - Dimanche)"
    )
    badge = models.CharField(
        max_length=150, 
        default="🏨 Séjour & Détente Hôtel 4 Étoiles",
        help_text="ex: 🏨 Séjour & Détente Hôtel 4 Étoiles"
    )
    slogan = models.CharField(
        max_length=150, 
        default="Profitez de la différence !!!"
    )
    tagline = models.CharField(
        max_length=350, 
        default="Formule promotionnelle tout compris pour un séjour de détente absolue aux portes de Yaoundé"
    )
    notice = models.CharField(
        max_length=350, 
        blank=True, 
        default="Séjour directement au Complexe United Hôtel ★★★★ (Vendredi au Dimanche - 02 nuitées). Formule sans navette requise."
    )
    features_text = models.TextField(
        blank=True,
        default=(
            "🛏️ | CHAMBRE STANDARD | Chambre tout confort pour 02 nuitées complètes\n"
            "🍽️ | REPAS INCLUS | Restauration gourmande servie durant tout le séjour\n"
            "🏊‍♂️ | PISCINE | Accès illimité à la piscine extérieure du complexe\n"
            "🎬 | CINÉMA | Séances sur grand écran en salle climatisée Dolby\n"
            "🏋️ | FITNESS | Accès à la salle de sport & musculation\n"
            "✨ | COUP D'ÉCLAT | Soin beauté & relaxation visage revigorant | vip"
        ),
        help_text="Prestations incluses au format : Icône | Nom | Description | VIP (optionnel)"
    )

    # 6 Paliers tarifaires en FCFA
    price_single = models.PositiveIntegerField(
        default=130000, 
        help_text="Tarif Single (1 pers.) en FCFA"
    )
    price_couple = models.PositiveIntegerField(
        default=175000, 
        help_text="Tarif Couple (2 pers.) en FCFA"
    )
    price_famille_3 = models.PositiveIntegerField(
        default=225000, 
        help_text="Tarif Famille de 03 personnes en FCFA"
    )
    price_famille_4 = models.PositiveIntegerField(
        default=350000, 
        help_text="Tarif Famille de 04 personnes en FCFA"
    )
    price_famille_5 = models.PositiveIntegerField(
        default=395000, 
        help_text="Tarif Famille de 05 personnes en FCFA"
    )
    price_famille_6 = models.PositiveIntegerField(
        default=515000, 
        help_text="Tarif Famille de 06 personnes en FCFA"
    )

    is_active = models.BooleanField(
        default=True, 
        help_text="Afficher la formule Week-end Détente sur le site public"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Séjour Week-end Détente"
        verbose_name_plural = "Séjours Week-end Détente"

    def __str__(self):
        return f"{self.title} ({self.duration})"

    @property
    def features(self):
        if not self.features_text:
            return []
        result = []
        for line in self.features_text.splitlines():
            line = line.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split('|')]
            if len(parts) == 1:
                result.append({'icon': '✓', 'name': parts[0], 'desc': '', 'vip': False})
            elif len(parts) == 2:
                if len(parts[0]) <= 4:
                    result.append({'icon': parts[0], 'name': parts[1], 'desc': '', 'vip': False})
                else:
                    result.append({'icon': '✓', 'name': parts[0], 'desc': parts[1], 'vip': False})
            elif len(parts) == 3:
                result.append({'icon': parts[0], 'name': parts[1], 'desc': parts[2], 'vip': False})
            else:
                is_vip = parts[3].lower() in ['vip', 'true', '1', 'oui', 'yes']
                result.append({'icon': parts[0], 'name': parts[1], 'desc': parts[2], 'vip': is_vip})
        return result

    @property
    def tiers(self):
        return [
            {
                'id': 'weekend-single',
                'title': 'Single',
                'people': 1,
                'price': self.price_single,
                'price_display': f"{self.price_single:,}".replace(",", " ") + " XFA",
                'desc': '1 personne — 02 nuitées',
                'highlight': False,
            },
            {
                'id': 'weekend-couple',
                'title': 'Couple',
                'people': 2,
                'price': self.price_couple,
                'price_display': f"{self.price_couple:,}".replace(",", " ") + " XFA",
                'desc': '2 personnes — 02 nuitées',
                'highlight': True,
            },
            {
                'id': 'weekend-famille-3',
                'title': 'Famille de 03 personnes',
                'people': 3,
                'price': self.price_famille_3,
                'price_display': f"{self.price_famille_3:,}".replace(",", " ") + " XFA",
                'desc': '3 personnes — 02 nuitées',
                'highlight': False,
            },
            {
                'id': 'weekend-famille-4',
                'title': 'Famille de 04 personnes',
                'people': 4,
                'price': self.price_famille_4,
                'price_display': f"{self.price_famille_4:,}".replace(",", " ") + " XFA",
                'desc': '4 personnes — 02 nuitées',
                'highlight': False,
            },
            {
                'id': 'weekend-famille-5',
                'title': 'Famille de 05 personnes',
                'people': 5,
                'price': self.price_famille_5,
                'price_display': f"{self.price_famille_5:,}".replace(",", " ") + " XFA",
                'desc': '5 personnes — 02 nuitées',
                'highlight': False,
            },
            {
                'id': 'weekend-famille-6',
                'title': 'Famille de 06 personnes',
                'people': 6,
                'price': self.price_famille_6,
                'price_display': f"{self.price_famille_6:,}".replace(",", " ") + " XFA",
                'desc': '6 personnes — 02 nuitées',
                'highlight': False,
            },
        ]


