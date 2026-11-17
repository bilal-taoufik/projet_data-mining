# Workflow - EduSmart

Ce document définit les règles Git à respecter par l'ensemble des membres du groupe pour travailler sur le projet **EduSmart**.

**Règle principale : aucun push direct sur `main` ou `dev`. Toutes les modifications doivent passer par une branche dédiée et une Pull Request.**

## 1 - Organisation des branches

Le projet utilise deux branches principales :

| Branche | Rôle |
|---|---|
| `main` | Version stable et validée du projet |
| `dev` | Branche d'intégration permettant de tester les modifications de l'ensemble du groupe |

Chaque nouvelle modification doit être réalisée sur une nouvelle branche créée à partir de `main`.

### Convention de nommage

| Préfixe | Utilisation | Exemple |
|---|---|---|
| `feat/` | Ajouter une nouvelle fonctionnalité | `feat/collecte-instacart` |
| `refact/` | Restructurer ou améliorer du code existant sans changer son comportement | `refact/collecte-api` |
| `docs/` | Ajouter ou modifier de la documentation | `docs/readme` |

**Une modification = une nouvelle branche.**

## 2 - Workflow Git

### Étape 1 - Se placer sur `main`

Avant de commencer une modification, récupérer la dernière version du projet :

```bash
git checkout main
git pull origin main
```

### Étape 2 - Créer une nouvelle branche

Choisir le préfixe correspondant au travail à réaliser.

**Nouvelle fonctionnalité :**

```bash
git checkout -b feat/nom-fonctionnalite
```

**Refactorisation :**

```bash
git checkout -b refact/nom-refactorisation
```

**Documentation :**

```bash
git checkout -b docs/nom-document
```

### Étape 3 - Effectuer les modifications

Développer la fonctionnalité ou modifier les fichiers nécessaires.

Une fois le travail terminé, vérifier les fichiers modifiés :

```bash
git status
```

Ajouter les modifications :

```bash
git add .
```

Créer un commit avec un message clair :

```bash
git commit -m "feat: ajout de la collecte Open Food Facts"
```

### Étape 5 - Envoyer la branche sur GitHub

Une fois le commit créé, envoyer la branche distante :

```bash
git push -u origin feat/collecte-openfoodfacts
```

Adapter le nom à la branche utilisée.

**Ne jamais effectuer de `git push origin main` ou `git push origin dev` directement.**

## 4. Pull Request vers `dev`

Après avoir envoyé la branche sur GitHub :

1. Ouvrir le dépôt GitHub.
2. Cliquer sur **Compare & pull request**.
3. Sélectionner `dev` comme branche de destination (*base*).
4. Vérifier que la branche source (*compare*) est bien votre branche de travail.
5. Ajouter un titre et une description des modifications.
6. Créer la Pull Request.

La branche `dev` permet de regrouper les travaux des différents membres du groupe.

## 5. Tests sur `dev`

Une fois les modifications fusionnées dans `dev`, le groupe doit vérifier que :

- Le projet démarre correctement.
- Les nouvelles fonctionnalités fonctionnent.
- Les modifications ne cassent pas les fonctionnalités existantes.
- Les scripts et les dépendances sont compatibles.
- Les éventuels conflits ou bugs sont corrigés.

Si un problème est détecté, il doit être corrigé sur une nouvelle branche, puis intégré à `dev` via une Pull Request.

## 6. Pull Request de `dev` vers `main`

Lorsque toutes les modifications ont été testées et validées, créer une nouvelle Pull Request sur GitHub :

```text
base: main
compare: dev
```

Après validation par le groupe, fusionner `dev` dans `main`.

La branche `main` doit toujours contenir une version stable du projet.

## 7. Schéma du workflow

```text
main
 │
 ├── feat/collecte-instacart ─────┐
 │                                │
 ├── feat/collecte-openfoodfacts ─┤
 │                                │
 ├── refact/collecte-api ─────────┼── Pull Requests
 │                                │        │
 └── docs/readme ─────────────────┘        ▼
                                         dev
                                          │
                                    Tests du groupe
                                          │
                                    Validation OK
                                          │
                                    Pull Request
                                          ▼
                                         main
```

## 8. Règles à respecter

1. Toujours partir de `main` pour créer une nouvelle branche.
2. Toujours créer une branche pour chaque modification.
3. Respecter les préfixes `feat/`, `refact/` et `docs/`.
4. Utiliser des messages de commit clairs avec les préfixes correspondants.
5. Ne jamais pousser directement sur `main` ou `dev`.
6. Toujours créer une Pull Request vers `dev`.
7. Tester les modifications sur `dev` avant toute intégration dans `main`.
8. Fusionner `dev` vers `main` uniquement après validation du groupe.
9. Ne jamais ajouter de mots de passe, de clés API ou de fichier `.env` contenant des secrets dans Git.

## 9. Récapitulatif des commandes

```bash
# Se placer sur main et récupérer la dernière version
git checkout main
git pull origin main

# Créer une branche
git checkout -b feat/nom-fonctionnalite

# Ajouter les modifications
git add .

# Créer un commit
git commit -m "feat: description de la modification"

# Envoyer la branche sur GitHub
git push -u origin feat/nom-fonctionnalite
```

Ensuite, sur GitHub :

**Pull Request → `dev` → Tests → Pull Request `dev` vers `main`.**

---

**Toute contribution doit respecter ce workflow afin de garantir une collaboration organisée et un projet stable.**