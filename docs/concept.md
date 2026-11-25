# Document de concept — *Les Lanterniers* (titre provisoire)

> Version 0.1 — proposition de départ, tout est discutable.

## 1. Pitch

Le royaume d'**Aldara** est rongé par **la Brume**, un brouillard vivant qui efface les terres,
les souvenirs et ceux qui s'y perdent. Seules les **Lanternes d'Aube**, forgées dans un cristal
ancien, peuvent la repousser.

Les joueurs incarnent des **Lanterniers**, une confrérie d'aventuriers qui s'enfonce dans la Brume
pour retrouver des villages disparus, sauver des égarés et percer le secret de son origine.

**Pourquoi c'est bien adapté au format :**
- La Brume justifie naturellement le **plateau modulaire** : les tuiles se révèlent au fur et à mesure
  que la lumière avance — l'application dit quelle tuile poser et ce qu'on y découvre.
- La **lumière de la Lanterne** est une ressource commune qui s'épuise : c'est le **chronomètre**
  de la partie, idéal pour tenir en ~1 h et créer de la tension.

## 2. Public et format

| Critère | Choix |
|---|---|
| Joueurs | 1 à 6 (coopératif) |
| Âge | 10 ans et + |
| Durée | ~1 h par scénario, scénarios enchaînables en campagne |
| Matériel | Tuiles modulaires, cartes, figurines, dés d4/d6/d8/d10/d12/d20 |
| Application | Indispensable (MJ autonome) ; mode MJ incarné disponible |

## 3. Boucle de jeu

1. **Mise en place** : l'appli indique la tuile de départ, les figurines et les cartes à préparer.
2. **Tour des Héros** : chaque héros dispose de **2 actions** parmi :
   - *Se déplacer* · *Attaquer* · *Fouiller* · *Interagir* (PNJ, objet, porte…) · *Compétence*
3. **Tour de la Brume** (géré par l'appli) :
   - la Lanterne perd de la lumière ;
   - les ennemis s'activent (l'appli indique leurs mouvements et attaques) ;
   - un éventuel événement narratif survient.
4. On recommence jusqu'à la victoire (objectif du scénario) ou la défaite
   (Lanterne éteinte, ou tous les héros à terre).

## 4. Résolution des actions (dés)

Système simple, lisible dès 10 ans, mais qui fait rouler tous les dés :

- **Test** : `d20 + Caractéristique ≥ Difficulté` (Facile 8 · Normal 12 · Difficile 16 · Héroïque 20).
- **3 caractéristiques** : **Force**, **Agilité**, **Esprit** (de +0 à +5).
- **20 naturel** = réussite critique · **1 naturel** = complication narrative (l'appli décide).
- **Dégâts** : selon l'arme / le sort → d4 (dague) · d6 (épée courte) · d8 (épée) · d10 (hache) · d12 (arme lourde / grand sort).
- **Défense** : chaque héros a une valeur d'Armure qui sert de difficulté aux attaques ennemies.

Les joueurs lancent de vrais dés et **saisissent le résultat dans l'appli** (ou cochent « réussi / raté »
pour aller vite). Les jets des ennemis sont faits par l'appli.

## 5. Les héros (6 classes de départ)

| Classe | Rôle | Idée de compétence |
|---|---|---|
| **Gardien** | Protecteur | *Rempart* : subit les dégâts à la place d'un allié adjacent |
| **Lame** | Agile, furtif | *Ombre* : se déplace sans provoquer les ennemis |
| **Arcaniste** | Magie offensive | *Éclat d'Aube* : dégâts de zone qui repoussent la Brume |
| **Sylvain** | Nature, soins | *Sève* : soigne et retire un état |
| **Chasseur** | Distance, pièges | *Œil vif* : relance un dé d'attaque à distance |
| **Porte-Lanterne** | Soutien, lumière | *Ranimer* : rend de la lumière à la Lanterne |

Chaque héros a une **fiche** (caractéristiques, PV, armure) et un **deck de compétences** qui
grandit au fil de la campagne.

## 6. Le matériel

- **Tuiles** : forêt, ruines, village, caverne, marais… (formats hexagonaux ou carrés, à décider)
- **Cartes** : Compétences · Équipement · Trésors · États (empoisonné, aveuglé…) · Ennemis (référence)
- **Figurines** : 6 héros + ennemis (Égarés, Rôdeurs de Brume, Bêtes, Boss)
- **Jetons** : PV, lumière, portes, coffres, objectifs
- **Dés** : un set complet d4 → d20 par joueur (ou à partager)

## 7. L'application

### Mode MJ autonome (principal)
- Narration (texte + voix/ambiance sonore à terme)
- Instructions de pose des tuiles et des figurines
- Intelligence des ennemis, événements, dialogues à choix
- Suivi : lumière de la Lanterne, PV des ennemis, objectifs, tour en cours
- **Adaptation automatique** au nombre de joueurs (1 à 6) : nombre d'ennemis, PV, lumière
- Sauvegarde de campagne (progression, inventaire, choix narratifs)

### Mode MJ incarné
- L'appli devient un tableau de bord pour le MJ : script du scénario, stats des ennemis,
  tirages aléatoires, possibilité de modifier/ignorer ce que propose l'appli.

### Technique (proposition)
- **Application web (PWA)** : fonctionne sur téléphone, tablette et PC, installable, utilisable hors ligne.
- **TypeScript** pour le code.
- **Scénarios décrits en fichiers de données** (JSON/YAML) séparés du moteur : on peut écrire
  du contenu sans toucher au code.
- **Simulateur** pour tester l'équilibrage (milliers de parties automatiques).

## 8. Structure d'un scénario (~1 h)

1. **Introduction** narrative (2 min)
2. **Exploration** : 4 à 6 tuiles à révéler, rencontres, fouilles (30 min)
3. **Rebondissement** : choix moral ou événement (5 min)
4. **Climax** : combat de boss ou épreuve finale (15 min)
5. **Épilogue** : récompenses, conséquences pour la campagne (5 min)

Premier scénario envisagé : **« Le Village qui n'existait plus »** — retrouver les habitants
de Brumeval, disparus dans la nuit.

## 9. Feuille de route

1. ✅ Concept (ce document)
2. ⬜ Règles de base détaillées (livret v0.1)
3. ⬜ Contenu du 1er scénario + liste des tuiles/cartes nécessaires
4. ⬜ Prototype de l'appli (moteur + 1er scénario jouable)
5. ⬜ Matériel imprimable (print & play) pour tester en vrai
6. ⬜ Simulations d'équilibrage + tests de parties
7. ⬜ Campagne complète, mode MJ incarné, ambiance sonore

## 10. Questions ouvertes

- Titre définitif et nom de l'univers ?
- Tuiles **hexagonales** ou **carrées** ?
- PV des héros suivis **sur fiche physique** ou **dans l'appli** ?
- Mort d'un héros : simplement « à terre » (réanimable) ou conséquences permanentes en campagne ?
- Ton : plutôt lumineux/aventure ou plus sombre ?
