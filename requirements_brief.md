# **Cahier des Charges**

## **Partie 1 : Développement de l'API avec FastAPI**

### **Objectifs**

* Exposer le modèle de classification permettant de prédire l'éligibilité à un prêt.  
* Garantir la sécurité de l'API en mettant en place un système d'authentification.  
* Enregistrer toutes les demandes dans une base de données pour analyses statistiques.  
* Permettre aux utilisateurs de changer leur mot de passe après la première connexion.

### **Technologies utilisées**

* **Langage** : Python  
* **Framework** : FastAPI  
* **Base de données** : SQLModel (basé sur SQLAlchemy et Pydantic)  
* **Authentification** : JWT (JSON Web Token) avec OAuth2

### **Fonctionnalités**

#### **1\. Authentification et gestion des utilisateurs**

* Seul un administrateur peut créer un compte utilisateur.  
* Un utilisateur doit activer son compte et changer son mot de passe lors de la première connexion.  
* Utilisation de JWT pour l'authentification des requêtes.

#### **2\. Endpoints de l'API**

| Méthode | URL | Description | Accès |
| ----- | ----- | ----- | ----- |
| POST | /auth/login | Connexion et récupération du token | Tous | David
| POST | /auth/activation | Activation du compte et changement du mot de passe | Utilisateur | David
| POST | /auth/logout | Déconnexion | Utilisateur | David
| GET | /loans/predict | Prédiction d'éligibilité à un prêt | Utilisateur | --> Dorothée
| POST | /loans/request | Soumission d'une demande de prêt | Utilisateur | --> Dorothée
| GET | /loans/history | Historique des demandes | Utilisateur | --> Dorothée
| GET | /admin/users | Liste des utilisateurs | Admin | Sami
| POST | /admin/users | Création d'un utilisateur | Admin | Sami

#### **3\. Sécurité**

* Hachage et salage des mots de passe.  
* JWT avec expiration des tokens.  
* Vérification des permissions selon les rôles (Admin, Utilisateur).

#### **4\. Base de données**

* Table `users`: Stocke les informations des utilisateurs (email, mot de passe hashé, rôle, état d'activation, etc.).  
* Table `loan_requests`: Stocke les demandes de prêt avec leur statut et l'identifiant du demandeur.

---

## **Partie 2 : Développement de l'application bancaire avec Django**

### **Objectifs**

* Créer un site web permettant aux entreprises de demander des prêts.  
* Intégrer un espace client et un espace conseiller bancaire.  
* Permettre une interaction entre les clients et les conseillers via un chat intégré.  
* Publier des actualités sur la banque.

### **Technologies utilisées**

* **Langage** : Python  
* **Framework** : Django  
* **Base de données** : PostgreSQL / SQLite  
* **Frontend** : HTML, CSS, JavaScript (Bootstrap ou Tailwind)  
* **WebSocket** : Django Channels (pour le chat en temps réel)

### **Fonctionnalités**

#### **1\. Espace client**

* Inscription et connexion sécurisée.  
* Consultation des actualités de la banque.  
* Formulaire de demande de prêt.  
* Affichage du statut des demandes de prêt.  
* Messagerie instantanée avec le conseiller bancaire assigné.

#### **2\. Espace conseiller bancaire**

* Liste des demandes de prêts assignées.  
* Validation ou refus manuel des demandes validées par l'IA.  
* Gestion de la communication avec les clients via un chat.  
* Possibilité d’écrire une actualité

#### **3\. Sécurité**

* Authentification Django avec gestion des permissions.  
* Protection contre les attaques XSS et CSRF.  
* Chiffrement des mots de passe.

#### **4\. Base de données**

* Table `users`: Stocke les informations des clients et conseillers.  
* Table `loan_requests`: Stocke les demandes de prêt et leur statut.  
* Table `messages`: Stocke les messages échangés entre clients et conseillers.  
* Table `news`: Stocke les actualités publiées sur la page d’accueil.

