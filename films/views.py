from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.text import slugify
from .models import Film, WeeklySchedule
from . import forms

def filmlist(request):
    films = Film.objects.all().order_by('-date')
    return render(request, 'films/film_list.html', {'films': films})

def film_details(request, slug):
    film = get_object_or_404(Film, slug=slug)
    related_films = Film.objects.exclude(id=film.id).order_by('-date')[:4]
    return render(request, 'films/film_detail.html', {'film': film, 'related_films': related_films})

def film_create(request):
    if not (request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff or request.user.has_perm('films.add_film'))):
        messages.error(request, "Accès restreint : vous devez être connecté avec un compte administrateur autorisé pour ajouter un film.")
        return redirect('/accounts/login/?next=' + request.path)

    if request.method == 'POST':
        form = forms.CreateFilm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            
            # Associate with logged-in user or first available user
            if request.user.is_authenticated:
                instance.author = request.user
            else:
                default_user = User.objects.first()
                if not default_user:
                    default_user = User.objects.create_user(username='admin', password='password123')
                instance.author = default_user
            
            # Ensure slug exists and is unique
            chosen_slug = instance.slug.strip() if instance.slug else ''
            if not chosen_slug:
                chosen_slug = slugify(instance.title) or 'nouveau-film'
            
            base_slug = chosen_slug
            counter = 1
            while Film.objects.filter(slug=chosen_slug).exists():
                chosen_slug = f"{base_slug}-{counter}"
                counter += 1
            instance.slug = chosen_slug
            
            from .utils import parse_movie_date, format_french_date

            # Intelligent date analysis according to status
            if instance.status == 'upcoming':
                if instance.release_date and not instance.date_out:
                    instance.date_out = f"Sortie le {format_french_date(instance.release_date)}"
                elif instance.date_out and not instance.release_date:
                    instance.release_date = parse_movie_date(instance.date_out)
            else:
                if not instance.date_out:
                    instance.date_out = "À l'affiche"

            if not instance.format_type:
                instance.format_type = "2D NUMÉRIQUE"
            if not instance.genre:
                instance.genre = "Cinéma"

            instance.save()
            status_desc = "en salle" if instance.status == 'now_showing' else "prochainement"
            messages.success(request, f"Le film « {instance.title} » a été ajouté avec succès ({status_desc}) !")
            return redirect('films:details', slug=instance.slug)
    else:
        form = forms.CreateFilm()

    return render(request, 'films/film_create.html', {'form': form})

def schedule_update(request):
    if not (request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff)):
        messages.error(request, "Accès restreint : vous devez être administrateur pour modifier la programmation de la semaine.")
        return redirect('/accounts/login/?next=' + request.path)

    current_schedule = WeeklySchedule.objects.filter(is_active=True).first() or WeeklySchedule.objects.first()

    if request.method == 'POST':
        form = forms.WeeklyScheduleForm(request.POST, request.FILES, instance=current_schedule)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.save()
            if schedule.is_active:
                WeeklySchedule.objects.exclude(id=schedule.id).update(is_active=False)
            messages.success(request, "✨ Le programme officiel de la semaine a été mis à jour avec succès !")
            return redirect('/#schedule-row')
    else:
        form = forms.WeeklyScheduleForm(instance=current_schedule)

    context = {
        'form': form,
        'schedule': current_schedule,
        'is_edit': bool(current_schedule),
    }
    return render(request, 'films/schedule_form.html', context)

