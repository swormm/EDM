# Ecole Directe Moyenne

Ce script permet aux utilisateurs de se connecter à la plateforme [Ecole Directe](https://www.ecoledirecte.com) et d'accéder à diverses informations telles que les moyennes des notes, l'emploi du temps, et le cahier de texte. Il utilise l'API d'Ecole Directe pour récupérer les données.

## Fonctionnalités

- **Connexion à Ecole Directe** : Authentification sécurisée avec prise en charge de l'authentification à double facteur (2FA).
- **Moyenne des Notes** : Calcul et affichage des moyennes des notes par période et par matière.
- **Emploi du Temps** : Affichage de l'emploi du temps pour la journée actuelle.
- **Cahier de Texte** : Affichage des devoirs et autres informations à faire pour chaque matière.
- **Interface Utilisateur** : Utilisation de la bibliothèque `rich` pour afficher les données de manière claire et organisée.

## Prérequis

Avant de pouvoir utiliser ce script, vous devez avoir installé les modules Python suivants :

- `requests`
- `rich`
- `inquirer`
- `pandas`
- `tabulate`

Vous pouvez installer ces modules avec la commande suivante :

```bash
pip install requests rich inquirer pandas tabulate
```

## Utilisation

1. Clonez ce dépôt ou téléchargez directement le script.

   ```bash
   git clone https://github.com/sworm/EDM.git
   cd EDM
   ```

2. Assurez-vous que toutes les dépendances nécessaires sont installées :
```bash
pip install -r requirements.txt
```
3. Executer main.py et entrez votre nom d'utilisateur et votre mot de passe Ecole Directe lorsque cela vous est demandé.
4. Une fois connecté, vous pouvez choisir parmi les options suivantes :

   - **1 - Emploi du temps** : Affiche l'emploi du temps de la journée.
   - **2 - Moyenne des Notes** : Calcule et affiche la moyenne des notes pour chaque matière et période.
   - **3 - Cahier de texte** : Affiche les devoirs et les documents associés pour chaque matière.
   - **4 - Exit** : Quitte le programme.
