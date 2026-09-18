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
