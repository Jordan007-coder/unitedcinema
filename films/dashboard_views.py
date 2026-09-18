from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from .models import Film, WeeklySchedule
from .forms import CreateFilm

# Access control helpers
def is_admin_or_staff(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser or user.has_perm('films.add_film') or user.has_perm('films.change_film') or user.has_perm('films.delete_film'))

def is_superuser(user):
    return user.is_authenticated and user.is_superuser

def can_add_film(user):
    return user.is_authenticated and (user.is_superuser or user.has_perm('films.add_film'))

def can_change_film(user):
    return user.is_authenticated and (user.is_superuser or user.has_perm('films.change_film'))

def can_delete_film(user):
    return user.is_authenticated and (user.is_superuser or user.has_perm('films.delete_film'))


@login_required(login_url='/accounts/login/')
def dashboard_home(request):
    if not is_admin_or_staff(request.user):
        messages.error(request, "Accès refusé. Cet espace est réservé aux administrateurs.")
        return redirect('home')

    total_movies = Film.objects.count()
    total_users = User.objects.count()
    recent_movies = Film.objects.all().order_by('-date')[:6]
    active_schedule = WeeklySchedule.objects.filter(is_active=True).first()

    context = {
        'total_movies': total_movies,
        'total_users': total_users,
        'recent_movies': recent_movies,
        'active_schedule': active_schedule,
        'can_add': can_add_film(request.user),
        'can_change': can_change_film(request.user),
        'can_delete': can_delete_film(request.user),
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'films/dashboard/dashboard_home.html', context)


@login_required(login_url='/accounts/login/')
def dashboard_movie_list(request):
    if not is_admin_or_staff(request.user):
        messages.error(request, "Accès refusé.")
        return redirect('home')

    query = request.GET.get('q', '').strip()
    if query:
        movies = Film.objects.filter(
            Q(title__icontains=query) | Q(genre__icontains=query) | Q(format_type__icontains=query)
        ).order_by('-date')
    else:
        movies = Film.objects.all().order_by('-date')

    context = {
        'movies': movies,
        'query': query,
        'can_add': can_add_film(request.user),
        'can_change': can_change_film(request.user),
        'can_delete': can_delete_film(request.user),
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'films/dashboard/dashboard_movie_list.html', context)


@login_required(login_url='/accounts/login/')
def dashboard_movie_edit(request, slug):
    if not can_change_film(request.user):
        messages.error(request, "Vous n'avez pas la permission de modifier ce film.")
        return redirect('dashboard:movie_list')

    film = get_object_or_404(Film, slug=slug)

    if request.method == 'POST':
        form = CreateFilm(request.POST, request.FILES, instance=film)
        if form.is_valid():
            updated_film = form.save(commit=False)
            if not updated_film.slug:
                from django.utils.text import slugify
                updated_film.slug = slugify(updated_film.title) or film.slug

            from .utils import parse_movie_date, format_french_date
            if updated_film.status == 'upcoming':
                if updated_film.release_date and not updated_film.date_out:
                    updated_film.date_out = f"Sortie le {format_french_date(updated_film.release_date)}"
                elif updated_film.date_out and not updated_film.release_date:
                    updated_film.release_date = parse_movie_date(updated_film.date_out)
            else:
                if not updated_film.date_out:
                    updated_film.date_out = "À l'affiche"

            updated_film.save()
            messages.success(request, f"Le film « {updated_film.title} » a été mis à jour avec succès !")
            return redirect('dashboard:movie_list')
    else:
        form = CreateFilm(instance=film)

    context = {
        'form': form,
        'film': film,
        'is_edit': True,
        'can_add': can_add_film(request.user),
        'can_change': can_change_film(request.user),
        'can_delete': can_delete_film(request.user),
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'films/dashboard/dashboard_movie_edit.html', context)


@login_required(login_url='/accounts/login/')
def dashboard_movie_delete(request, slug):
    if not can_delete_film(request.user):
        messages.error(request, "Vous n'avez pas la permission de supprimer ce film.")
        return redirect('dashboard:movie_list')

    film = get_object_or_404(Film, slug=slug)

    if request.method == 'POST':
        title = film.title
        film.delete()
        messages.success(request, f"Le film « {title} » a été définitivement supprimé du catalogue.")
        return redirect('dashboard:movie_list')

    context = {
        'film': film,
        'can_add': can_add_film(request.user),
        'can_change': can_change_film(request.user),
        'can_delete': can_delete_film(request.user),
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'films/dashboard/dashboard_movie_delete.html', context)


# ==========================================
# USER & TASK MANAGEMENT (Superuser Only)
# ==========================================

@login_required(login_url='/accounts/login/')
def dashboard_user_list(request):
    if not is_superuser(request.user):
        messages.error(request, "Espace strictement réservé au superadministrateur.")
        return redirect('dashboard:home')

    users = User.objects.all().order_by('-is_superuser', '-is_staff', 'username')
    
    # Gather tasks for each user
    users_with_tasks = []
    ct = ContentType.objects.get_for_model(Film)
    
    for u in users:
        perms = u.user_permissions.filter(content_type=ct).values_list('codename', flat=True)
        tasks = []
        if u.is_superuser:
            tasks.append("Super Administrateur (Tous les droits)")
        else:
            if 'add_film' in perms:
                tasks.append("Ajouter des films")
            if 'change_film' in perms:
                tasks.append("Modifier des films")
            if 'delete_film' in perms:
                tasks.append("Supprimer des films")
            if u.is_staff and not tasks:
                tasks.append("Consultation Tableau de bord")
            if not tasks:
                tasks.append("Spectateur / Aucun droit spécial")
        
        users_with_tasks.append({
            'user': u,
            'tasks': tasks,
            'has_add': 'add_film' in perms or u.is_superuser,
            'has_change': 'change_film' in perms or u.is_superuser,
            'has_delete': 'delete_film' in perms or u.is_superuser,
        })

    context = {
        'users_data': users_with_tasks,
        'is_superuser': True,
    }
    return render(request, 'films/dashboard/dashboard_user_list.html', context)


@login_required(login_url='/accounts/login/')
def dashboard_user_create(request):
    if not is_superuser(request.user):
        messages.error(request, "Seul le superadministrateur peut créer des utilisateurs avec des tâches personnalisées.")
        return redirect('dashboard:home')

    ct = ContentType.objects.get_for_model(Film)
    perm_add = Permission.objects.get(content_type=ct, codename='add_film')
    perm_change = Permission.objects.get(content_type=ct, codename='change_film')
    perm_delete = Permission.objects.get(content_type=ct, codename='delete_film')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        password_confirm = request.POST.get('password_confirm', '').strip()

        task_add = 'task_add_film' in request.POST
        task_change = 'task_change_film' in request.POST
        task_delete = 'task_delete_film' in request.POST
        task_staff = 'task_staff_access' in request.POST or task_add or task_change or task_delete

        errors = []
        if not username:
            errors.append("Le nom d'utilisateur est requis.")
        elif User.objects.filter(username=username).exists():
            errors.append(f"Un utilisateur avec le nom « {username} » existe déjà.")

        if not password:
            errors.append("Le mot de passe est obligatoire.")
        elif len(password) < 6:
            errors.append("Le mot de passe doit contenir au moins 6 caractères.")
        elif password != password_confirm:
            errors.append("Les deux mots de passe ne correspondent pas.")

        if errors:
            for err in errors:
                messages.error(request, err)
        else:
            # Create user
            new_user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            new_user.is_staff = task_staff
            new_user.save()

            # Assign checked tasks
            assigned_tasks = []
            if task_add:
                new_user.user_permissions.add(perm_add)
                assigned_tasks.append("Ajouter des films")
            if task_change:
                new_user.user_permissions.add(perm_change)
                assigned_tasks.append("Modifier des films")
            if task_delete:
                new_user.user_permissions.add(perm_delete)
                assigned_tasks.append("Supprimer des films")

            task_summary = ", ".join(assigned_tasks) if assigned_tasks else "Accès tableau de bord basique"
            messages.success(request, f"L'utilisateur « {username} » a été créé avec succès ! Tâches assignées : {task_summary}.")
            return redirect('dashboard:user_list')

    context = {
        'is_superuser': True,
    }
    return render(request, 'films/dashboard/dashboard_user_create.html', context)


@login_required(login_url='/accounts/login/')
def dashboard_user_delete(request, user_id):
    if not is_superuser(request.user):
        messages.error(request, "Accès refusé.")
        return redirect('dashboard:home')

    user_to_delete = get_object_or_404(User, id=user_id)

    # Security check: Superuser cannot delete himself
    if user_to_delete == request.user:
        messages.error(request, "Vous ne pouvez pas supprimer votre propre compte superadministrateur !")
        return redirect('dashboard:user_list')

    if user_to_delete.username.lower() == 'jordan':
        messages.error(request, "Le compte superadministrateur principal 'Jordan' ne peut pas être supprimé.")
        return redirect('dashboard:user_list')

    if request.method == 'POST':
        uname = user_to_delete.username
        user_to_delete.delete()
        messages.success(request, f"L'utilisateur « {uname} » a été supprimé.")
        return redirect('dashboard:user_list')

    context = {
        'target_user': user_to_delete,
        'is_superuser': True,
    }
    return render(request, 'films/dashboard/dashboard_user_delete.html', context)
