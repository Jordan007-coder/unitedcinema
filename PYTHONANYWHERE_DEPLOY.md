# Guide de Déploiement : United Cinema & Hôtel sur PythonAnywhere

Ce guide détaille toutes les étapes pour mettre en ligne votre site web sur **PythonAnywhere**.

---

## 1. Réponse sur PostgreSQL : Est-il obligatoire ?

> **NON, absolument pas !**  
> Contrairement à d'autres plateformes comme Heroku ou Render (où les conteneurs sont réinitialisés et perdent les fichiers locaux), **sur PythonAnywhere le stockage est 100% persistant**.
>
> - **SQLite (`db.sqlite3`) fonctionne parfaitement en production** sur PythonAnywhere pour un site de cinéma/hôtel.
> - Vous conservez ainsi **toutes vos données déjà créées** (films, affiches, plannings, comptes admin) sans avoir besoin d'exporter ou convertir une base de données.
> - Si un jour votre trafic devenait énorme, PythonAnywhere intègre nativement une base **MySQL** gratuite en un clic. PostgreSQL n'est donc pas du tout nécessaire.

---

## 2. Préparations déjà effectuées dans le projet

1. **`STATIC_ROOT` configuré :** Permet à `python manage.py collectstatic` de regrouper tous les fichiers CSS, JS et images des packages dans le dossier `staticfiles/`.
2. **`CSRF_TRUSTED_ORIGINS` configuré :** Autorise les requêtes sécurisées depuis `https://*.pythonanywhere.com` (évite les erreurs 403 sur les formulaires).
3. **`SECRET_KEY` & `DEBUG` adaptables :** `DEBUG` peut être basculé facilement en `False` via variable d'environnement.
4. **`MEDIA_ROOT` configuré :** Tous les posters de films téléversés par l'administration restent dans le dossier `media/`.

---

## 3. Déploiement étape par étape sur PythonAnywhere

### Étape 1 : Créer votre compte
1. Rendez-vous sur [https://www.pythonanywhere.com/](https://www.pythonanywhere.com/) et créez un compte (option *Beginner* gratuite pour tester avec l'URL `votre_pseudo.pythonanywhere.com`).

---

### Étape 2 : Mettre le code sur PythonAnywhere

**Option A (Recommandée - Via Git / GitHub) :**
1. Poussez votre projet local sur GitHub (dépôt public ou privé).
2. Dans le Dashboard PythonAnywhere, ouvrez une console **Bash** et tapez :
   ```bash
   git clone https://github.com/votre-compte/unitedcinema.git
   cd unitedcinema
   ```

**Option B (Via fichier ZIP) :**
1. Compressez le dossier de votre projet en `unitedcinema.zip`.
2. Dans l'onglet **Files** de PythonAnywhere, téléversez le zip dans votre répertoire personnel (`/home/votre_pseudo/`).
3. Dans la console Bash, décompressez :
   ```bash
   unzip unitedcinema.zip -d unitedcinema
   ```

---

### Étape 3 : Créer l'environnement virtuel et installer les dépendances

Dans la console **Bash** de PythonAnywhere :

```bash
# Se placer dans le dossier du projet
cd ~/unitedcinema

# Créer un environnement virtuel Python 3.10
mkvirtualenv unitedcinema-env --python=/usr/bin/python3.10

# Installer les dépendances
pip install -r requirements.txt
```

---

### Étape 4 : Rassembler les fichiers statiques et vérifier la base de données

Toujours dans la console Bash (avec le virtualenv activé) :

```bash
# Rassembler les fichiers statiques (CSS, JS, affiches)
python manage.py collectstatic --noinput

# Vérifier que les migrations sont appliquées
python manage.py migrate

# (Optionnel) Créer un super-administrateur si vous ne l'avez pas déjà :
python manage.py createsuperuser
```

---

### Étape 5 : Configurer l'application Web sur PythonAnywhere

1. Allez dans l'onglet **Web** du tableau de bord PythonAnywhere.
2. Cliquez sur **"Add a new web app"**.
3. Choisissez votre nom de domaine (`votre_pseudo.pythonanywhere.com`).
4. Choisissez **"Manual configuration"** (NE PAS choisir Django directement, car nous avons déjà un projet existant).
5. Choisissez **Python 3.10**.
6. Une fois créée, complétez les sections suivantes sur la page :

#### A. Virtualenv
Dans le champ **Virtualenv**, entrez :
```text
/home/votre_pseudo/.virtualenvs/unitedcinema-env
```
*(Remplacez `votre_pseudo` par votre nom d'utilisateur PythonAnywhere).*

#### B. Code directory & Working directory
- **Source code :** `/home/votre_pseudo/unitedcinema`
- **Working directory :** `/home/votre_pseudo/unitedcinema`

#### C. Fichier de configuration WSGI
Cliquez sur le lien bleu du fichier WSGI (ex: `/var/www/votre_pseudo_pythonanywhere_com_wsgi.py`).  
Supprimez tout son contenu et remplacez-le par :

```python
import os
import sys

# Chemin vers votre projet
path = '/home/votre_pseudo/unitedcinema'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'unitedcinema.settings'
os.environ['DJANGO_DEBUG'] = 'False'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
*(Remplacez bien `votre_pseudo` par votre nom d'utilisateur).* Cliquez sur **Save**.

#### D. Fichiers Statiques et Médias (Section "Static files")
Dans l'onglet **Web**, descendez à la section **Static files** et ajoutez ces deux lignes :

| URL | Directory |
|---|---|
| `/static/` | `/home/votre_pseudo/unitedcinema/staticfiles` |
| `/media/` | `/home/votre_pseudo/unitedcinema/media` |

---

### Étape 6 : Lancer et Tester le site !

1. En haut de l'onglet **Web**, cliquez sur le gros bouton vert **"Reload votre_pseudo.pythonanywhere.com"**.
2. Ouvrez votre navigateur et rendez-vous sur `https://votre_pseudo.pythonanywhere.com/`.
3. Testez la page d'accueil, le catalogue des films, la page `/packages/` et l'interface d'administration `/admin/`.
