# SoftDeskSupport-API

Projet de formation OpenClassrooms "Devenez développeur d'applications Python"

## Prérequis

Pour exécuter ce projet, vous devez avoir les outils suivants installés :
- **Python** : Version 3.14 ou supérieure.
- **Poetry 2.0** : Gestionnaire de dépendances et d'environnements virtuels pour Python.
- **Git** : Outil de contrôle de version pour cloner le dépôt.
- **Terminal** : Un terminal comme Command Prompt (Windows), Terminal (macOS), ou un shell Linux.

## Installer et lancer l'API

### 1. Cloner ce dépôt Github en local

Dans votre terminal, à l'emplacement voulu tapez :
```bash
git clone https://github.com/redaabdi/SoftDeskSupport-API/
cd SoftDeskSupport-API
```

### 2. Activer poetry et installer les dépendances

- Sous Windows :
  ```bash
  poetry install
  ```
- Sous macOS / Linux :
  ```bash
  poetry install
  ```


Activez-le :
- Sous Windows :
  ```bash
  Invoke-Expression (poetry env activate)
  ```
- Sous macOS / Linux :
  ```bash
  eval $(poetry env activate)
  ```

### 3. Lancer le serveur

```bash
cd SoftDeskSupportAPI
python manage.py runserver
```

### 4. Utiliser l'api à travers des requêtes

A l'aide de Postman ou d'un autre outil, faites les requêtes sans oublier le préfixe "http://127.0.0.1:8000/"

|  # | Point de terminaison d'API                                                | Méthode HTTP | URL                                           |
|  1 | Connexion du user (obtenir les tokens)                                    | `POST`       | `api/login/`                                  |
|  2 | Obtenir un nouvel access token à partir du refresh token                  | `POST`       | `api/login/refresh/`                          |
|  3 | Inscription du user                                                       | `POST`       | `api/signup/`                                 |
|  4 | Afficher le profil du user connecté                                       | `GET`        | `api/profile/`                                |
|  5 | Modifier le profil du user connecté                                       | `PUT/PATCH`  | `api/profile/`                                |
|  6 | Supprimer le profil du user connecté                                      | `DELETE`     | `api/profile/`                                |
|  7 | Afficher la liste des projets dont le user est contributeur               | `GET`        | `api/projects/`                               |
|  8 | Créer un projet                                                           | `POST`       | `api/projects/`                               |
|  9 | Afficher les détails d'un projet dont le user est contributeur            | `GET`        | `api/projects/{id}/`                          |
| 10 | Mettre à jour un projet                                                   | `PUT/PATCH`  | `api/projects/{id}/`                          |
| 11 | Supprimer un projet                                                       | `DELETE`     | `api/projects/{id}/`                          |
| 12 | Afficher la liste de tous les contributeurs (users) d'un projet (project) | `GET`        | `api/projects/{id}/contributors/`             |
| 13 | Ajouter un contributeur (user) à un projet                                | `POST`       | `api/projects/{id}/contributors/`             |
| 14 | Afficher un contributeur d'un projet                                      | `GET`        | `api/projects/{id}/contributors/{id}`         |
| 15 | Supprimer un contributeur d'un projet                                     | `DELETE`     | `api/projects/{id}/contributors/{id}`         |
| 16 | Afficher la liste des problèmes (issues) liés à un projet (project)       | `GET`        | `api/projects/{id}/issues/`                   |
| 17 | Créer un problème dans un projet                                          | `POST`       | `api/projects/{id}/issues/`                   |
| 18 | Afficher un problème d'un projet via son id                               | `GET`        | `api/projects/{id}/issues/{id}`               |
| 19 | Mettre à jour un problème dans un projet                                  | `PUT/PATCH`  | `api/projects/{id}/issues/{id}`               |
| 20 | Supprimer un problème d'un projet                                         | `DELETE`     | `api/projects/{id}/issues/{id}`               |
| 21 | Afficher les commentaires liés à un problème (issue)                      | `GET`        | `api/projects/{id}/issues/{id}/comments/`     |
| 22 | Créer un commentaire sur un problème                                      | `POST`       | `api/projects/{id}/issues/{id}/comments/`     |
| 23 | Afficher un commentaire (comment) via son id                              | `GET`        | `api/projects/{id}/issues/{id}/comments/{id}` |
| 24 | Modifier un commentaire                                                   | `PUT/PATCH`  | `api/projects/{id}/issues/{id}/comments/{id}` |
| 25 | Supprimer un commentaire                                                  | `DELETE`     | `api/projects/{id}/issues/{id}/comments/{id}` |



## Crédits

Réda Abdi pour le projet 10, dans le cadre de la formation « Développeur d'applications Python » de OpenClassrooms.
