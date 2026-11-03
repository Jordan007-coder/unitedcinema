import re
import datetime

FRENCH_MONTHS = {
    'janvier': 1, 'janv': 1, 'jan': 1,
    'fevrier': 2, 'février': 2, 'fevr': 2, 'fev': 2,
    'mars': 3, 'mar': 3,
    'avril': 4, 'avr': 4,
    'mai': 5,
    'juin': 6,
    'juillet': 7, 'juil': 7,
    'aout': 8, 'août': 8,
    'septembre': 9, 'sept': 9, 'sep': 9,
    'octobre': 10, 'oct': 10,
    'novembre': 11, 'nov': 11,
    'decembre': 12, 'décembre': 12, 'dec': 12,
}

FRENCH_MONTH_NAMES = [
    '', 'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
    'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
]

FRENCH_MONTH_ABBR = [
    '', 'JAN', 'FÉV', 'MAR', 'AVR', 'MAI', 'JUIN',
    'JUIL', 'AOÛT', 'SEPT', 'OCT', 'NOV', 'DÉC'
]

def parse_movie_date(val):
    """
    Intelligently analyzes a date input (string or date object)
    and returns a valid datetime.date object for chronological ordering.
    """
    if not val:
        return None
    if isinstance(val, datetime.date):
        return val
    if isinstance(val, datetime.datetime):
        return val.date()

    text = str(val).strip().lower()

    # 1. Try ISO format: YYYY-MM-DD
    match = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})', text)
    if match:
        year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
        try:
            return datetime.date(year, month, day)
        except ValueError:
            pass

    # 2. Try DD/MM/YYYY or DD-MM-YYYY
    match = re.search(r'(\d{1,2})[/\.-](\d{1,2})[/\.-](\d{4})', text)
    if match:
        day, month, year = int(match.group(1)), int(match.group(2)), int(match.group(3))
        try:
            return datetime.date(year, month, day)
        except ValueError:
            pass

    # 3. Try textual format: "18 septembre 2026" or "02 octobre 2026"
    match = re.search(r'(\d{1,2})\s+([a-zéû]+)\s+(\d{4})', text)
    if match:
        day = int(match.group(1))
        month_word = match.group(2)
        year = int(match.group(3))
        # Normalize accents
        norm_month = month_word.replace('é', 'e').replace('û', 'u').replace('ô', 'o')
        if norm_month in FRENCH_MONTHS:
            month = FRENCH_MONTHS[norm_month]
            try:
                return datetime.date(year, month, day)
            except ValueError:
                pass

    # 4. Try month and year without day: "octobre 2026" -> defaults to 1st of month
    match = re.search(r'([a-zéû]+)\s+(\d{4})', text)
    if match:
        month_word = match.group(1)
        year = int(match.group(2))
        norm_month = month_word.replace('é', 'e').replace('û', 'u').replace('ô', 'o')
        if norm_month in FRENCH_MONTHS:
            return datetime.date(year, FRENCH_MONTHS[norm_month], 1)

    return None

def format_french_date(d):
    """Formats date as: '18 septembre 2026'"""
    if not d:
        return ""
    month_name = FRENCH_MONTH_NAMES[d.month].lower()
    day_str = f"{d.day:02d}"
    return f"{day_str} {month_name} {d.year}"

def format_date_badge(d):
    """Formats date for card badge: '18 SEPT'"""
    if not d:
        return "SORTIE"
    month_abbr = FRENCH_MONTH_ABBR[d.month]
    return f"{d.day:02d} {month_abbr}"

def get_month_label(d):
    """Formats month group header: 'Septembre 2026'"""
    if not d:
        return "Prochainement"
    return f"{FRENCH_MONTH_NAMES[d.month]} {d.year}"

def organize_upcoming_movies(movies_qs):
    """
    Analyzes, sorts, and chronologically groups upcoming movies by month & year.
    Returns a list of groups:
    [
        {
            'month_label': 'Septembre 2026',
            'month_key': (2026, 9),
            'movies': [movie_dict_1, movie_dict_2, ...]
        },
        ...
    ]
    """
    processed = []
    default_future = datetime.date(2099, 12, 31)

    for film in movies_qs:
        # Determine date
        parsed_d = None
        if hasattr(film, 'release_date') and film.release_date:
            parsed_d = film.release_date
        elif hasattr(film, 'date_out') and film.date_out:
            parsed_d = parse_movie_date(film.date_out)

        sort_date = parsed_d or default_future
        
        # Build friendly display fields
        display_date = format_french_date(parsed_d) if parsed_d else (getattr(film, 'date_out', '') or 'Prochainement')
        date_badge = format_date_badge(parsed_d) if parsed_d else 'SORTIE'
        month_label = get_month_label(parsed_d) if parsed_d else 'Dates à confirmer'
        month_key = (parsed_d.year, parsed_d.month) if parsed_d else (2099, 12)

        poster_url = None
        if hasattr(film, 'thumb') and film.thumb:
            poster_url = film.thumb.url
        elif hasattr(film, 'image') and film.image:
            poster_url = film.image

        movie_dict = {
            'id': getattr(film, 'slug', '') or getattr(film, 'id', ''),
            'slug': getattr(film, 'slug', ''),
            'title': film.title,
            'image': poster_url,
            'is_media': bool(getattr(film, 'thumb', None)),
            'duration': getattr(film, 'date_out', 'Prochainement') or 'Prochainement',
            'format': getattr(film, 'format_type', '2D NUMÉRIQUE') or '2D NUMÉRIQUE',
            'genre': getattr(film, 'genre', 'Cinéma') or 'Cinéma',
            'synopsis': getattr(film, 'synopsis', ''),
            'release_date': display_date,
            'date_badge': date_badge,
            'age_badge': 'TP',
            'age_rating': 'Tous publics',
            'exact_date': sort_date,
            'month_label': month_label,
            'month_key': month_key,
        }
        processed.append(movie_dict)

    # Sort strictly in chronological order by exact release date
    processed.sort(key=lambda m: (m['exact_date'], m['title']))

    # Group by month preserving chronological order
    groups_dict = {}
    for movie in processed:
        mk = movie['month_key']
        if mk not in groups_dict:
            groups_dict[mk] = {
                'month_label': movie['month_label'],
                'month_key': mk,
                'movies': []
            }
        groups_dict[mk]['movies'].append(movie)

    # Return list of month groups ordered chronologically
    sorted_groups = sorted(groups_dict.values(), key=lambda g: g['month_key'])
    return sorted_groups
