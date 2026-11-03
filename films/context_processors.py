from .models import Film, WeeklySchedule

def reservation_movies(request):
    """
    Context processor making all available movies and weekly schedule 
    accessible across all templates for the reservation modal dropdown.
    """
    now_showing = Film.objects.filter(status='now_showing').order_by('-date')
    upcoming = Film.objects.filter(status='upcoming').order_by('release_date')
    all_films = Film.objects.all().order_by('status', 'title')
    active_schedule = WeeklySchedule.objects.filter(is_active=True).first()
    
    return {
        'res_now_showing': now_showing,
        'res_upcoming': upcoming,
        'res_all_films': all_films,
        'global_active_schedule': active_schedule,
    }
