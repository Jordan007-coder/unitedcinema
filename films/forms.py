from django import forms
from . import models

class CreateFilm(forms.ModelForm):
    title = forms.CharField(
        label="Titre du film",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ex: Avatar : De Feu et de Cendres',
            'id': 'id_title',
            'required': True,
        })
    )
    slug = forms.SlugField(
        label="Identifiant URL (Slug)",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control font-mono',
            'placeholder': 'Généré automatiquement à partir du titre',
            'id': 'id_slug',
        }),
        help_text="Généré automatiquement. Vous pouvez le modifier si nécessaire."
    )
    status = forms.ChoiceField(
        label="Statut de programmation",
        choices=models.Film.STATUS_CHOICES,
        initial='now_showing',
        widget=forms.RadioSelect(attrs={
            'class': 'status-radio-input',
        })
    )
    release_date = forms.DateField(
        label="Date de sortie officielle",
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'id': 'id_release_date',
        }),
        help_text="Utilisé pour le classement chronologique automatique des sorties."
    )
    date_out = forms.CharField(
        label="Texte horaire / Séances",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ex: À l’affiche • 2h 15min ou 18 Septembre 2026',
            'id': 'id_date_out',
        })
    )
    genre = forms.CharField(
        label="Genre(s)",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ex: Action / Aventure / Science-Fiction',
            'id': 'id_genre',
        })
    )
    format_type = forms.CharField(
        label="Format de projection",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ex: 3D / 2D DOLBY DIGITAL',
            'id': 'id_format_type',
        })
    )
    synopsis = forms.CharField(
        label="Synopsis & Description",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control form-textarea',
            'placeholder': "Racontez l'intrigue et l'univers du film...",
            'id': 'id_synopsis',
            'rows': 4,
        })
    )
    thumb = forms.ImageField(
        label="Affiche officielle (Poster)",
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-file-input',
            'id': 'id_thumb',
            'accept': 'image/*',
        })
    )

    class Meta:
        model = models.Film
        fields = ['title', 'slug', 'status', 'release_date', 'date_out', 'genre', 'format_type', 'synopsis', 'thumb']


class WeeklyScheduleForm(forms.ModelForm):
    title = forms.CharField(
        label="Titre du programme",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ex: Programme de la Semaine du 11 au 17 Septembre 2026',
            'id': 'id_schedule_title',
        })
    )
    start_date = forms.DateField(
        label="Date de début",
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'id': 'id_start_date',
        })
    )
    end_date = forms.DateField(
        label="Date de fin",
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'id': 'id_end_date',
        })
    )
    poster = forms.ImageField(
        label="Affiche officielle du programme (HD)",
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-file-input',
            'id': 'id_schedule_poster',
            'accept': 'image/*',
        })
    )
    subtitle = forms.CharField(
        label="Sous-titre descriptif",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Consultez l'affiche officielle des séances, horaires et tarifs de la semaine en cours.",
            'id': 'id_schedule_subtitle',
        })
    )
    notice = forms.CharField(
        label="Bandeau d'information / Navette",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ex: 🎬 Navette gratuite Ahala ↔ Mbankomo pour toutes les séances à partir de 18h00 !',
            'id': 'id_schedule_notice',
        })
    )
    price_standard = forms.CharField(
        label="Séance Classique",
        required=False,
        initial="3 000 XAF",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'id_price_standard',
        })
    )
    price_under_12 = forms.CharField(
        label="Moins de 12 ans",
        required=False,
        initial="1 500 XAF",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'id_price_under_12',
        })
    )
    price_glasses_3d = forms.CharField(
        label="Lunettes 3D",
        required=False,
        initial="1 500 XAF",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'id_price_glasses_3d',
        })
    )
    price_premiere = forms.CharField(
        label="Première",
        required=False,
        initial="5 000 XAF",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'id_price_premiere',
        })
    )
    price_avant_premiere = forms.CharField(
        label="Avant-Première",
        required=False,
        initial="5 000 XAF",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'id_price_avant_premiere',
        })
    )
    is_active = forms.BooleanField(
        label="Activer immédiatement ce programme sur le site public",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'custom-task-checkbox',
            'id': 'id_schedule_active',
        })
    )

    class Meta:
        model = models.WeeklySchedule
        fields = [
            'title', 'start_date', 'end_date', 'poster', 'subtitle', 'notice',
            'price_standard', 'price_under_12', 'price_glasses_3d', 
            'price_premiere', 'price_avant_premiere', 'is_active'
        ]


class PackageCategoryForm(forms.ModelForm):
    name = forms.CharField(
        label="Nom de la Catégorie",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ex: Formule Week-end Détente, Packages Loisirs & Évasion...',
            'id': 'id_cat_name',
        })
    )
    slug = forms.SlugField(
        label="Identifiant URL (Slug)",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control font-mono',
            'placeholder': 'ex: weekend-detente (généré automatiquement)',
            'id': 'id_cat_slug',
        })
    )
    badge = forms.CharField(
        label="Badge / Étiquette d'en-tête",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ex: 🏨 Séjour & Détente Hôtel 4 Étoiles, ⭐ Best-Seller',
            'id': 'id_cat_badge',
        })
    )
    subtitle = forms.CharField(
        label="Sous-titre / Phrase d'accroche",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ex: Formule tout compris pour un séjour de détente absolue aux portes de Yaoundé',
            'id': 'id_cat_subtitle',
        })
    )
    notice = forms.CharField(
        label="Bandeau d'information / Remarque",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ex: Séjour directement au Complexe United Hôtel ★★★★ (Vendredi au Dimanche - 02 nuitées).',
            'id': 'id_cat_notice',
        })
    )
    flyer_image = forms.ImageField(
        label="Grande Affiche / Flyer Officiel de la Catégorie",
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control file-input-visible',
            'id': 'id_cat_flyer_image',
            'accept': 'image/*',
        }),
        help_text="Affiche officielle grand format affichée à côté des packages (zoomable et téléchargeable sur le site public)."
    )
    flyer_title = forms.CharField(
        label="Titre de l'affiche (ex: Flyer Week-end Détente)",
        required=False,
        initial="Affiche Officielle",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'id_cat_flyer_title',
        })
    )
    layout_type = forms.ChoiceField(
        label="Disposition des cartes de packages",
        choices=models.PackageCategory.LAYOUT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control res-select',
            'id': 'id_cat_layout_type',
        })
    )
    order = forms.IntegerField(
        label="Ordre d'affichage de la catégorie",
        required=False,
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'id_cat_order',
            'min': 0,
        })
    )
    is_active = forms.BooleanField(
        label="Catégorie active (visible sur le site public)",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'custom-task-checkbox',
            'id': 'id_cat_active',
        })
    )

    class Meta:
        model = models.PackageCategory
        fields = [
            'name', 'slug', 'badge', 'subtitle', 'notice',
            'flyer_image', 'flyer_title', 'layout_type', 'order', 'is_active'
        ]


class PackageForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        label="Catégorie de rattachement (Formule parente)",
        queryset=models.PackageCategory.objects.all(),
        required=True,
        empty_label="-- Sélectionner une catégorie --",
        widget=forms.Select(attrs={
            'class': 'form-control res-select',
            'id': 'id_package_category',
        }),
        help_text="Sélectionnez le groupe auquel ce package appartient (ex : Packages Loisirs & Évasion, Spa & Bien-être, Week-end Détente)."
    )
    name = forms.CharField(
        label="Nom du Package / Formule",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ex: PACK SINGLE, PACK COUPLE, PACK II...',
            'id': 'id_package_name',
        })
    )
    slug = forms.SlugField(
        label="Identifiant URL (Slug)",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control font-mono',
            'placeholder': 'ex: pack-single (généré automatiquement si vide)',
            'id': 'id_package_slug',
        }),
        help_text="Identifiant unique pour la sélection et réservation. Laisser vide pour générer automatiquement."
    )
    subtitle = forms.CharField(
        label="Sous-titre descriptif",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ex: 1 personne, 2 personnes, Fraîcheur & Bien-être...',
            'id': 'id_package_subtitle',
        })
    )
    badge = forms.CharField(
        label="Badge / Étiquette mise en avant",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ex: Formule Conviviale, ⭐ Best-Seller Tout Inclus, 👑 VIP',
            'id': 'id_package_badge',
        })
    )
    price = forms.IntegerField(
        label="Tarif (FCFA)",
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'ex: 5000, 130000',
            'id': 'id_package_price',
            'min': 0,
            'step': 500,
        }),
        help_text="Montant numérique en FCFA (ex: 5000 ou 130000)."
    )
    price_display = forms.CharField(
        label="Texte d'affichage du prix",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ex: 130 000 FCFA (calculé automatiquement si vide)',
            'id': 'id_package_price_display',
        }),
        help_text="Laisser vide pour générer automatiquement à partir du tarif numérique."
    )
    tagline = forms.CharField(
        label="Slogan / Phrase d'accroche",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ex: Idéal pour une journée détente entre amis ou en famille',
            'id': 'id_package_tagline',
        })
    )
    image = forms.ImageField(
        label="Image / Affiche Illustrative du Package (Champ Image)",
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control file-input-visible',
            'id': 'id_package_image',
            'accept': 'image/*',
        }),
        help_text="Téléversez ici le fichier photo ou affiche propre à ce package. Ce champ est dédié exclusivement au fichier image."
    )
    features_text = forms.CharField(
        label="Prestations et activités incluses",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control form-textarea',
            'placeholder': (
                "Une prestation par ligne au format : Icône | Nom | Description | VIP (optionnel)\n"
                "Exemples :\n"
                "🏊‍♂️ | PISCINE | Accès extérieur au bassin\n"
                "🎬 | CINÉMA | Séance grand écran Dolby au choix\n"
                "🥽 | VR | Réalité virtuelle Game Zone | vip\n"
                "🚌 | TRANSPORT | Navette aller-retour (dès 8 pers.) | vip"
            ),
            'id': 'id_package_features',
            'rows': 7,
        }),
        help_text="Format : Icône | Nom | Description | vip (ou simplement une ligne par prestation)."
    )
    highlight = forms.BooleanField(
        label="Mettre en avant ce package (Bordure dorée & Badge)",
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'custom-task-checkbox',
            'id': 'id_package_highlight',
        })
    )
    transport_included = forms.BooleanField(
        label="Navette de transport aller-retour incluse (dès 8 pers.)",
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'custom-task-checkbox',
            'id': 'id_package_transport',
        })
    )
    is_active = forms.BooleanField(
        label="Activer ce package (visible sur le site public)",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'custom-task-checkbox',
            'id': 'id_package_active',
        })
    )
    order = forms.IntegerField(
        label="Ordre d'affichage",
        required=False,
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'id_package_order',
            'min': 0,
        }),
        help_text="0 s'affiche en premier, 1 ensuite, etc."
    )

    class Meta:
        model = models.Package
        fields = [
            'category', 'name', 'slug', 'subtitle', 'badge',
            'price', 'price_display', 'tagline', 'image', 'features_text',
            'highlight', 'transport_included', 'is_active', 'order'
        ]


class WeekendPackageForm(forms.ModelForm):
    title = forms.CharField(
        label="Titre de la formule",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'id_weekend_title',
        })
    )
    duration = forms.CharField(
        label="Durée du séjour",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'id_weekend_duration',
        })
    )
    badge = forms.CharField(
        label="Badge / Étiquette",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'id_weekend_badge',
        })
    )
    tagline = forms.CharField(
        label="Slogan / Phrase d'accroche",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'id_weekend_tagline',
        })
    )
    notice = forms.CharField(
        label="Bandeau informatif de réservation",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'id_weekend_notice',
        })
    )
    features_text = forms.CharField(
        label="Prestations et services inclus (une par ligne)",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control form-textarea',
            'id': 'id_weekend_features',
            'rows': 6,
        }),
        help_text="Format : Icône | Nom | Description | VIP (optionnel)"
    )
    price_single = forms.IntegerField(
        label="Tarif Single (1 pers.) en FCFA",
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 5000})
    )
    price_couple = forms.IntegerField(
        label="Tarif Couple (2 pers.) en FCFA",
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 5000})
    )
    price_famille_3 = forms.IntegerField(
        label="Tarif Famille de 03 pers. en FCFA",
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 5000})
    )
    price_famille_4 = forms.IntegerField(
        label="Tarif Famille de 04 pers. en FCFA",
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 5000})
    )
    price_famille_5 = forms.IntegerField(
        label="Tarif Famille de 05 pers. en FCFA",
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 5000})
    )
    price_famille_6 = forms.IntegerField(
        label="Tarif Famille de 06 pers. en FCFA",
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 5000})
    )
    is_active = forms.BooleanField(
        label="Activer ce forfait sur le site public",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'custom-task-checkbox'})
    )

    class Meta:
        model = models.WeekendPackage
        fields = [
            'title', 'duration', 'badge', 'tagline', 'notice', 'features_text',
            'price_single', 'price_couple', 'price_famille_3',
            'price_famille_4', 'price_famille_5', 'price_famille_6',
            'is_active'
        ]


