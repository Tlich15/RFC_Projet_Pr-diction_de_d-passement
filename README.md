# 🚀 RFC - Projet Prédiction de Dépassement Mensuel

## 📋 Description du Projet

Application complète (Backend + Frontend) pour la prédiction de dépassement mensuel des clients RFC.

### 🎯 Objectifs
- Analyser la consommation mensuelle des clients (historique sur plusieurs années)
- Identifier les clients avec dépassements récurrents
- Prédire les dépassements pour les 2 prochains mois (modèles ARIMA et Prophet)
- Fournir des visualisations claires et interactives
- Exposer les données via une API REST

### 📊 Sources de Données
- `DATA_Prêt_Années_Combiner.xlsx` → Données historiques de consommation client (3 ans)
- `Reporting_Visualisation.xlsx` → Prédictions R et résumé clients
- `Predictions_2mois_R.xlsx` → Résultats modèles ARIMA/Prophet

## 🏗️ Architecture du Projet

```
RFC_Projet_Pr-diction_de_d-passement/
├── 📁 backend/           # API FastAPI Python
├── 📁 frontend-rfc/      # Interface Angular
└── 📄 README.md          # Documentation principale
```

## 🐍 Backend - FastAPI

### Technologies
- **FastAPI** - Framework web moderne et rapide
- **Pandas** - Manipulation des données Excel
- **Matplotlib** - Génération de graphiques
- **Uvicorn** - Serveur ASGI

### Fonctionnalités
- ✅ API REST complète
- ✅ Chargement automatique des données Excel
- ✅ Endpoints pour clients, prédictions, visualisations
- ✅ Génération de graphiques PNG
- ✅ CORS configuré pour le développement

### Installation et Lancement
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Endpoints API
- `GET /health` - Statut de l'API
- `GET /clients/` - Liste des clients
- `GET /clients/history?client={nom}` - Historique d'un client
- `GET /clients/predictions?client={nom}` - Prédictions d'un client
- `GET /predictions/` - Toutes les prédictions
- `GET /visualizations/client-history.png?client={nom}` - Graphique historique
- `GET /data/status` - Statut des fichiers de données

## 🌐 Frontend - Angular

### Technologies
- **Angular 17** - Framework frontend moderne
- **TypeScript** - Langage de programmation
- **SCSS** - Styles avancés
- **Angular Material** - Composants UI

### Fonctionnalités
- ✅ Interface professionnelle RFC
- ✅ Gestion des clients avec pagination
- ✅ Affichage des prédictions
- ✅ Modal d'historique intégré
- ✅ Recherche et filtrage en temps réel
- ✅ Design responsive et moderne
- ✅ Navigation fluide entre composants

### Installation et Lancement
```bash
cd frontend-rfc
npm install
npm start
```

### Pages
- **Clients** (`/clients`) - Liste paginée avec recherche
- **Prédictions** (`/predictions`) - Tableau des prédictions avec historique

## 🚀 Démarrage Rapide

### 1. Cloner le Repository
```bash
git clone https://github.com/Tlich15/RFC_Projet_Pr-diction_de_d-passement.git
cd RFC_Projet_Pr-diction_de_d-passement
```

### 2. Lancer le Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 3. Lancer le Frontend
```bash
cd frontend-rfc
npm install
npm start
```

### 4. Accéder à l'Application
- **Frontend** : http://localhost:4200
- **API Backend** : http://localhost:8000
- **Documentation API** : http://localhost:8000/docs

### Quelques Images Sur Notre Application 
<img width="1270" height="754" alt="Capture d’écran 2025-08-19 à 11 27 22 AM" src="https://github.com/user-attachments/assets/6bde57f0-5e58-4bfd-bbe7-69fc0b15d08f" />

<img width="1436" height="715" alt="Capture d’écran 2025-08-19 à 10 24 56 AM" src="https://github.com/user-attachments/assets/d9ba01a4-6906-472f-8909-b78ff2d26745" />

<img width="1436" height="699" alt="Capture d’écran 2025-08-19 à 11 17 48 AM" src="https://github.com/user-attachments/assets/2b8f460e-a37e-43b1-9112-51c29da1c60a" />

<img width="1436" height="699" alt="Capture d’écran 2025-08-19 à 11 18 01 AM" src="https://github.com/user-attachments/assets/d59c3dc6-a486-4324-9bb4-0df668e469c0" />

<img width="1436" height="693" alt="Capture d’écran 2025-08-19 à 11 18 21 AM" src="https://github.com/user-attachments/assets/0ef14a53-bc1f-4944-b41e-ed52b3640fdd" />

<img width="1436" height="693" alt="Capture d’écran 2025-08-19 à 11 18 36 AM" src="https://github.com/user-attachments/assets/ec5d2783-9f03-4c3e-a05b-09a0c9d48b00" />

<img width="1436" height="693" alt="Capture d’écran 2025-08-19 à 11 19 05 AM" src="https://github.com/user-attachments/assets/4e7c7df4-e6a0-42b7-87c9-d05d9a983fbf" />








## 📁 Structure des Données

Placez vos fichiers Excel dans le dossier `backend/data/` :
- `DATA_Prêt_Années_Combiner.xlsx`
- `Reporting_Visualisation.xlsx`
- `Predictions_2mois_R.xlsx`

## 🔧 Configuration

### Variables d'Environnement
```bash
# Backend
APP_CORS_ORIGINS=http://localhost:4200,http://127.0.0.1:4200

# Frontend
# Modifier api.service.ts si nécessaire pour changer l'URL du backend
```

## 📱 Fonctionnalités Principales

### 🔍 Recherche et Filtrage
- Recherche en temps réel des clients
- Filtrage des prédictions par client
- Pagination limitée à 10 éléments par page

### 📊 Visualisations
- Graphiques d'historique client générés dynamiquement
- Modal intégré pour afficher les graphiques
- Interface responsive pour tous les appareils

### 🔄 Navigation
- Navigation fluide entre clients et prédictions
- Boutons de retour et liens contextuels
- Historique de navigation préservé

## 🛠️ Développement

### Ajouter de Nouvelles Fonctionnalités
1. **Backend** : Créer de nouveaux endpoints dans `backend/app/routers/`
2. **Frontend** : Ajouter de nouveaux composants dans `frontend-rfc/src/app/features/`
3. **Tests** : Utiliser les fichiers `.spec.ts` existants

### Structure des Composants
```
frontend-rfc/src/app/
├── core/           # Services partagés (API, etc.)
├── features/       # Composants métier
│   ├── clients/   # Gestion des clients
│   └── predictions/ # Gestion des prédictions
└── shared/         # Composants réutilisables
```

## 📈 Roadmap

- [ ] Export des données en Excel/CSV
- [ ] Graphiques interactifs avec Chart.js
- [ ] Authentification utilisateur
- [ ] Dashboard avec métriques
- [ ] Notifications en temps réel
- [ ] Tests automatisés complets

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est développé pour RFC Tunisie.

## 📞 Support

Pour toute question ou support, contactez l'équipe de développement RFC.

---

**Développé avec ❤️ pour RFC Tunisie** 🇹🇳 
