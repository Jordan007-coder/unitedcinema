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
