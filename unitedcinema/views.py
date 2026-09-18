from django.shortcuts import render
from films.models import Film, WeeklySchedule

def homepage(request):
    cinema_info = {
        'name': 'United Cinema',
        'location': 'Centre administratif de Mbankomo - Yaoundé - Cameroun',
        'phone_primary': '(+237) 680 52 22 22',
        'phone_secondary': '(+237) 222 31 59 00',
        'phone_mobile': '(+237) 651 46 69 38',
        'phone_alt': '(+237) 698 087 777',
        'email_reservation': 'reservations@unitedhotelsgroup.com',
        'email_info': 'info@unitedhotelsgroup.com',
        'slogan': 'Profitez de la différence !!!',
        'address': 'Mbankomo, Quartier Administratif (BP 17 091 Yaoundé, Cameroun)',
    }

    carousel_slides = [
        {
            'image': 'images/slide1_facade.jpg',
            'badge': 'Bienvenue à Mbankomo',
            'title': 'Le Plus Grand Complexe Cinéma & Loisirs',
            'subtitle': 'Salle climatisée, fauteuils grand confort en cuir et technologie 3D DOLBY de dernière génération.',
            'cta_text': 'Découvrir le programme',
            'cta_link': '#now-showing',
        },
        {
            'image': 'images/slide4_spiderman.jpg',
            'badge': 'Événement Exclusif',
            'title': 'Spider-Man: Brand New Day',
            'subtitle': 'Le super-héros revient sur écran géant en 3D immersive. Réservez vos places dès maintenant !',
            'cta_text': 'Voir la fiche film',
            'cta_link': '#now-showing',
        },
        {
            'image': 'images/slide2_ensorceleuses.jpg',
            'badge': 'Sortie Nationale',
            'title': 'Les Ensorceleuses 2',
            'subtitle': 'Sandra Bullock & Nicole Kidman réunies dans une suite ensorcelante à vivre en salle obscure.',
            'cta_text': 'Voir les horaires',
            'cta_link': '#schedule',
        },
        {
            'image': 'images/slide3_insidious.jpg',
            'badge': 'Frissons & Suspense',
            'title': 'Insidious : L’invasion du lointain',
            'subtitle': 'Le mal s’est échappé... Oserez-vous franchir la porte rouge dans nos salles DOLBY Atmos ?',
            'cta_text': 'Voir la fiche film',
            'cta_link': '#now-showing',
        },
        {
            'image': 'images/slide5_tad.jpg',
            'badge': 'Idéal en Famille',
            'title': 'TAD l’explorateur & la lampe magique',
            'subtitle': 'Une aventure hilarante et rythmée qui ravira petits et grands tout au long de la semaine.',
            'cta_text': 'Séances en famille',
            'cta_link': '#schedule',
        },
        {
            'image': 'images/slide6_mutiny.jpg',
            'badge': 'Cinéma Action 2026',
            'title': 'Sensations Fortes au Rendez-vous',
            'subtitle': 'Une programmation riche sélectionnée avec soin par Les Films 26 pour le public camerounais.',
            'cta_text': 'Prochaines sorties',
            'cta_link': '#upcoming-movies',
        },
    ]

    default_now_showing = [
        {
            'id': 'spiderman-brand-new-day',
            'title': 'Spiderman : brand new day',
            'image': 'images/spiderman_brand_new_day.jpg',
            'duration': '2h 15min',
            'age_rating': 'Tous publics',
            'age_badge': 'TP',
            'genre': 'Action / Fantastique',
            'format': '3D / 2D DOLBY',
            'version': 'VF & VOSTF',
            'synopsis': "Peter Parker tente de reconstruire son existence après que ses souvenirs ont été effacés de l'esprit du monde entier. Alors qu'il tente de vivre une vie simple à New York, une nouvelle alliance criminelle et une menace mystique surgissent. Spider-Man doit se dépasser et réinventer ses alliances pour sauver la ville sans révéler son secret.",
        },
        {
            'id': 'insidious-linvasion-du-lointain',
            'title': 'Insidious : l’invasion du lointain',
            'image': 'images/insidious_linvasion_du_lointain.jpg',
            'duration': '1h 48min',
            'age_rating': 'Interdit aux moins de 12 ans',
            'age_badge': '-12',
            'genre': 'Épouvante-Horreur / Frisson',
            'format': '2D DOLBY DIGITAL',
            'version': 'VF',
            'synopsis': "Le mal s'est échappé du Lointain. Lorsque les portes dimensionnelles entre notre réalité et les limbes ténébreuses commencent à se fracturer, une nouvelle famille se retrouve assiégée par des entités démoniaques ancestrales. Seule une plongée terrifiante au cœur des ténèbres permettra de briser la malédiction.",
        },
        {
            'id': 'tad-lexplorateur',
            'title': 'TAD l’explorateur et la lampe magique',
            'image': 'images/tad_lexplorateur.jpg',
            'duration': '1h 30min',
            'age_rating': 'Tous publics',
            'age_badge': 'TP',
            'genre': 'Animation / Aventure / Famille',
            'format': '3D / 2D NUMÉRIQUE',
            'version': 'VF',
            'synopsis': "Tad rêve toujours d'être pris au sérieux par ses pairs archéologues. Lorsqu'il détruit accidentellement un sarcophage et réveille un génie excentrique enfermé dans une lampe magique, il déclenche un sort ancien qui met ses amis en danger. De l'Égypte à Paris, Tad se lance dans une course contre la montre délirante.",
        },
        {
            'id': 'the-dog-stars',
            'title': 'The dog stars',
            'image': 'images/the_dog_stars.jpg',
            'duration': '2h 10min',
            'age_rating': 'Accord parental recommandé (-12 ans)',
            'age_badge': '-12',
            'genre': 'Science-Fiction / Drame',
            'format': '2D DOLBY ATMOS',
            'version': 'VF & VOSTF',
            'synopsis': "Réalisé par Ridley Scott d'après le roman culte de Peter Heller. Dans un futur proche décimé par une terrible épidémie mondiale, Hig vit reclus sur une base aérienne isolée du Colorado avec son chien et un compagnon armé. Lorsqu'une faible transmission radio crépite sur sa radio de bord, l'espoir d'une vie meilleure renaît.",
        },
        {
            'id': 'les-ensorcelleuses-2',
            'title': 'Les ensorcelleuses 2',
            'image': 'images/les_ensorceleuses_2.jpg',
            'duration': '1h 55min',
            'age_rating': 'Tous publics',
            'age_badge': 'TP',
            'genre': 'Fantastique / Comédie dramatique',
            'format': '2D NUMÉRIQUE',
            'version': 'VF',
            'synopsis': "Sandra Bullock et Nicole Kidman reprennent leurs rôles emblématiques des sœurs sorcières Sally et Gillian Owens. Alors qu'une nouvelle génération de la famille Owens commence à manifester de puissants pouvoirs, un serment obscur menace leur héritage. Ensemble, les femmes Owens devront briser le sort qui pèse sur leur lignée.",
        },
    ]

    from films.utils import organize_upcoming_movies

    # 1. Now Showing movies (Actuellement au cinéma)
    now_showing_qs = Film.objects.filter(status='now_showing').order_by('-date')
    now_showing_movies = []
    for film in now_showing_qs:
        poster_url = film.thumb.url if film.thumb else None
        now_showing_movies.append({
            'id': film.slug,
            'title': film.title,
            'image': poster_url,
            'is_media': bool(poster_url),
            'duration': film.date_out if film.date_out else 'À l’affiche',
            'age_rating': 'Tous publics',
            'age_badge': 'TP',
            'genre': film.genre if film.genre else 'Cinéma',
            'format': film.format_type if film.format_type else '2D NUMÉRIQUE',
            'version': 'VF & VOSTF',
            'synopsis': film.synopsis if film.synopsis else 'Film programmé à United Cinema Mbankomo.',
            'slug': film.slug,
            'is_new': True,
        })

    # 2. Upcoming movies (Prochainement) organized strictly in chronological order by date and month
    upcoming_qs = Film.objects.filter(status='upcoming')
    upcoming_groups = organize_upcoming_movies(upcoming_qs)

    # 3. Active Weekly Schedule
    active_schedule = WeeklySchedule.objects.filter(is_active=True).first()

    context = {
        'cinema': cinema_info,
        'carousel_slides': carousel_slides,
        'now_showing_movies': now_showing_movies,
        'upcoming_groups': upcoming_groups,
        'active_schedule': active_schedule,
    }

    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

def packages(request):
    cinema_info = {
        'name': 'United Hotel & Cinéma',
        'hotel_stars': 'Hôtel 4 Étoiles ★★★★',
        'location': 'Centre administratif de Mbankomo - Yaoundé - Cameroun',
        'phone_primary': '(+237) 680 52 22 22',
        'phone_secondary': '(+237) 222 31 59 00',
        'phone_mobile': '(+237) 651 46 69 38',
        'phone_alt': '(+237) 698 087 777',
        'whatsapp_number': '237680522222',
        'email_reservation': 'reservations@unitedhotelsgroup.com',
        'email_info': 'info@unitedhotelsgroup.com',
        'slogan': 'Profitez de la différence !!!',
        'address': 'Mbankomo, Quartier Administratif (BP 17 091 Yaoundé, Cameroun)',
    }

    loisir_packages = [
        {
            'id': 'package-loisir',
            'name': 'PACKAGE LOISIR',
            'category': 'loisir',
            'badge': 'Formule Conviviale',
            'price': 5000,
            'price_display': '5 000 FCFA',
            'tagline': 'Idéal pour une journée détente entre amis ou en famille',
            'features': [
                {'name': 'PISCINE', 'icon': '🏊‍♂️', 'desc': 'Accès à la piscine extérieure du complexe'},
                {'name': 'CINÉMA', 'icon': '🎬', 'desc': 'Séance sur grand écran en salle climatisée Dolby'},
                {'name': 'BILLARD', 'icon': '🎱', 'desc': 'Parties de billard dans notre espace détente'},
                {'name': 'SPORT', 'icon': '🏸', 'desc': 'Accès aux équipements sportifs & terrains'},
                {'name': 'BABYFOOT', 'icon': '⚽', 'desc': 'Espace babyfoot en accès libre'},
            ],
            'highlight': False,
            'transport_included': False,
        },
        {
            'id': 'package-evasion',
            'name': 'PACKAGE ÉVASION',
            'category': 'loisir',
            'badge': '⭐ Best-Seller Tout Inclus',
            'price': 10000,
            'price_display': '10 000 FCFA',
            'tagline': 'L’expérience complète avec réalité virtuelle et navette aller-retour',
            'features': [
                {'name': 'PISCINE', 'icon': '🏊‍♂️', 'desc': 'Accès illimité à la piscine'},
                {'name': 'CINÉMA', 'icon': '🎬', 'desc': 'Séance cinéma grand écran au choix'},
                {'name': 'BILLARD', 'icon': '🎱', 'desc': 'Espace billard grand confort'},
                {'name': 'SPORT', 'icon': '🏸', 'desc': 'Activités sportives & fitness'},
                {'name': 'BABYFOOT', 'icon': '⚽', 'desc': 'Babyfoot & jeux conviviaux'},
                {'name': 'JEUX DE RÉALITÉ VIRTUELLE', 'icon': '🥽', 'desc': 'Immersion totale Game Zone VR dernière génération', 'vip': True},
                {'name': 'TRANSPORT ALLER-RETOUR', 'icon': '🚌', 'desc': 'Navette aller-retour (dès 8 pers.) : Hippodrome, Poste centrale, Ahala-barrière', 'vip': True},
            ],
            'highlight': True,
            'transport_included': True,
        },
    ]

    spa_packages = [
        {
            'id': 'pack-1',
            'name': 'PACK I',
            'subtitle': 'Vitalité & Détente',
            'category': 'spa',
            'badge': 'Formule Énergie',
            'price': 7000,
            'price_display': '7 000 FCFA',
            'tagline': 'Remise en forme et purification dans un cadre apaisant',
            'features': [
                {'name': 'FITNESS', 'icon': '🏋️', 'desc': 'Séance en salle de fitness moderne et équipée'},
                {'name': 'HAMMAM / SAUNA', 'icon': '🧖‍♀️', 'desc': 'Bain de vapeur et chaleur détoxifiante'},
                {'name': 'TRANSPORT', 'icon': '🚌', 'desc': 'Navette incluse (dès 8 pers.) : Hippodrome, Poste centrale, Ahala-barrière'},
            ],
            'highlight': False,
            'transport_included': True,
        },
        {
            'id': 'pack-2',
            'name': 'PACK II',
            'subtitle': 'Fraîcheur & Bien-être',
            'category': 'spa',
            'badge': '⭐ Équilibre Parfait',
            'price': 10000,
            'price_display': '10 000 FCFA',
            'tagline': 'Le combo parfait entre baignade, sauna et remise en forme',
            'features': [
                {'name': 'PISCINE', 'icon': '🏊‍♂️', 'desc': 'Baignade et farniente au bord du bassin'},
                {'name': 'HAMMAM / SAUNA', 'icon': '🧖‍♀️', 'desc': 'Détente musculaire profonde et relaxation'},
                {'name': 'FITNESS', 'icon': '🏋️', 'desc': 'Espace cardio-training & musculation'},
                {'name': 'TRANSPORT', 'icon': '🚌', 'desc': 'Navette incluse (dès 8 pers.) : Hippodrome, Poste centrale, Ahala-barrière'},
            ],
            'highlight': True,
            'transport_included': True,
        },
        {
            'id': 'pack-3',
            'name': 'PACK III',
            'subtitle': 'Sérénité & VIP Massage',
            'category': 'spa',
            'badge': '👑 Expérience VIP Spa',
            'price': 15000,
            'price_display': '15 000 FCFA',
            'tagline': 'L’expérience ultime de relaxation avec massage bien-être exclusif',
            'features': [
                {'name': 'FITNESS', 'icon': '🏋️', 'desc': 'Accès complet à la salle de sport'},
                {'name': 'HAMMAM / SAUNA', 'icon': '🧖‍♀️', 'desc': 'Séance décontractante sauna et vapeur'},
                {'name': 'MASSAGE', 'icon': '💆‍♀️', 'desc': 'Massage corporel relaxant dispensé par des mains expertes', 'vip': True},
                {'name': 'TRANSPORT', 'icon': '🚌', 'desc': 'Navette incluse (dès 8 pers.) : Hippodrome, Poste centrale, Ahala-barrière'},
            ],
            'highlight': False,
            'transport_included': True,
        },
    ]

    transport_note = "NB : Le transport est assuré à partir de 8 personnes ! Points de ramassage : Hippodrome (United Hotel International), Poste centrale (Pharmacie la Moisson), Ahala-barrière (Santa Lucia)."

    weekend_detente = {
        'id': 'weekend-detente',
        'name': 'WEEK-END DÉTENTE',
        'duration': '02 Nuitées (Vendredi - Samedi - Dimanche)',
        'badge': '🏨 Séjour & Détente Hôtel 4 Étoiles',
        'slogan': 'Profitez de la différence !!!',
        'tagline': 'Formule promotionnelle tout compris pour un séjour de détente absolue aux portes de Yaoundé',
        'features': [
            {'name': 'CHAMBRE STANDARD', 'icon': '🛏️', 'desc': 'Chambre tout confort pour 02 nuitées complètes'},
            {'name': 'REPAS INCLUS', 'icon': '🍽️', 'desc': 'Restauration gourmande servie durant tout le séjour'},
            {'name': 'PISCINE', 'icon': '🏊‍♂️', 'desc': 'Accès illimité à la piscine extérieure du complexe'},
            {'name': 'CINÉMA', 'icon': '🎬', 'desc': 'Séances sur grand écran en salle climatisée Dolby'},
            {'name': 'FITNESS', 'icon': '🏋️', 'desc': 'Accès à la salle de sport & musculation'},
            {'name': "COUP D'ÉCLAT", 'icon': '✨', 'desc': 'Soin beauté & relaxation visage revigorant', 'vip': True},
        ],
        'tiers': [
            {'id': 'weekend-single', 'title': 'Single', 'people': 1, 'price': 130000, 'price_display': '130 000 XFA', 'desc': '1 personne — 02 nuitées'},
            {'id': 'weekend-couple', 'title': 'Couple', 'people': 2, 'price': 175000, 'price_display': '175 000 XFA', 'desc': '2 personnes — 02 nuitées', 'highlight': True},
            {'id': 'weekend-famille-3', 'title': 'Famille de 03 personnes', 'people': 3, 'price': 225000, 'price_display': '225 000 XFA', 'desc': '3 personnes — 02 nuitées'},
            {'id': 'weekend-famille-4', 'title': 'Famille de 04 personnes', 'people': 4, 'price': 350000, 'price_display': '350 000 XFA', 'desc': '4 personnes — 02 nuitées'},
            {'id': 'weekend-famille-5', 'title': 'Famille de 05 personnes', 'people': 5, 'price': 395000, 'price_display': '395 000 XFA', 'desc': '5 personnes — 02 nuitées'},
            {'id': 'weekend-famille-6', 'title': 'Famille de 06 personnes', 'people': 6, 'price': 515000, 'price_display': '515 000 XFA', 'desc': '6 personnes — 02 nuitées'},
        ],
        'transport_included': False,
    }

    context = {
        'cinema': cinema_info,
        'loisir_packages': loisir_packages,
        'spa_packages': spa_packages,
        'weekend_detente': weekend_detente,
        'all_packages': loisir_packages + spa_packages,
        'transport_note': transport_note,
    }

    return render(request, 'packages.html', context)

