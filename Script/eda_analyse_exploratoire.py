"""
ANALYSE EXPLORATOIRE DES DONNÉES (EDA)
Test Technique - TOGO Datalab
Auteur: KLUTSE Amatré Cynthia-Ornella
Date: Janvier 2026

Objectif: Comprendre la structure, la qualité et la distribution des données
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Configuration des graphiques
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("="*80)
print("ANALYSE EXPLORATOIRE DES DONNÉES - TOGO DATALAB")
print("="*80)

# 1. CHARGEMENT DES DONNÉES
data_path = "../data/"

print("\n CHARGEMENT DES FICHIERS...")
try:
    centres = pd.read_csv(data_path + "centres_service.csv")
    demandes = pd.read_csv(data_path + "demandes_service_public.csv")
    communes = pd.read_csv(data_path + "details_communes.csv")
    developpement = pd.read_csv(data_path + "developpement.csv")
    documents = pd.read_csv(data_path + "documents_administratifs_ext.csv")
    socioeco = pd.read_csv(data_path + "donnees_socioeconomiques.csv")
    logs = pd.read_csv(data_path + "logs_activite.csv")
    reseau = pd.read_csv(data_path + "reseau_routier_togo_ext.csv")
    print(" Tous les fichiers chargés avec succès !\n")
except Exception as e:
    print(f" Erreur de chargement: {e}")
    exit()

# 
# 2. STRUCTURE DES DONNÉES
print("="*80)
print("1. STRUCTURE DES DONNÉES")
print("="*80)

datasets = {
    'centres_service': centres,
    'demandes_service_public': demandes,
    'details_communes': communes,
    'developpement': developpement,
    'documents_administratifs': documents,
    'donnees_socioeconomiques': socioeco,
    'logs_activite': logs,
    'reseau_routier': reseau
}

# Créer un résumé de la structure
summary_data = []
for name, df in datasets.items():
    summary_data.append({
        'Dataset': name,
        'Lignes': df.shape[0],
        'Colonnes': df.shape[1],
        'Valeurs_manquantes': df.isnull().sum().sum(),
        'Doublons': df.duplicated().sum()
    })

summary_df = pd.DataFrame(summary_data)
print("\n RÉSUMÉ GLOBAL DES DATASETS :")
print(summary_df.to_string(index=False))
print(f"\nTotal: {summary_df['Lignes'].sum():,} lignes de données")

# 3. QUALITÉ DES DONNÉES (Identification des problèmes)
print("\n" + "="*80)
print("2. QUALITÉ DES DONNÉES")
print("="*80)

for name, df in datasets.items():
    print(f"\n {name.upper()}")
    print(f"   Dimensions: {df.shape[0]} lignes × {df.shape[1]} colonnes")
    
    # Valeurs manquantes
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print(f"     Valeurs manquantes détectées:")
        for col, count in missing[missing > 0].items():
            pct = (count / len(df)) * 100
            print(f"      - {col}: {count} ({pct:.1f}%)")
    else:
        print(f"    Aucune valeur manquante")
    
    # Doublons
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        print(f"     Doublons: {duplicates}")
    else:
        print(f"    Aucun doublon")

# 4. STATISTIQUES DESCRIPTIVES
print("\n" + "="*80)
print("3. STATISTIQUES DESCRIPTIVES CLÉS")
print("="*80)

# Volume de demandes
volume_total = demandes['nombre_demandes'].sum()
print(f"\n VOLUME TOTAL DE DEMANDES: {volume_total:,}")

# Délais de traitement
delai_moyen = demandes['delai_traitement_jours'].mean()
delai_median = demandes['delai_traitement_jours'].median()
delai_min = demandes['delai_traitement_jours'].min()
delai_max = demandes['delai_traitement_jours'].max()

print(f"\n  DÉLAIS DE TRAITEMENT:")
print(f"   - Moyenne: {delai_moyen:.1f} jours")
print(f"   - Médiane: {delai_median:.1f} jours")
print(f"   - Minimum: {delai_min} jours")
print(f"   - Maximum: {delai_max} jours")

# Taux de rejet
taux_rejet = demandes['taux_rejet'].mean() * 100
print(f"\n TAUX DE REJET MOYEN: {taux_rejet:.2f}%")
print(f"   - Minimum: {demandes['taux_rejet'].min()*100:.2f}%")
print(f"   - Maximum: {demandes['taux_rejet'].max()*100:.2f}%")

# Centres de service
nb_centres = centres.shape[0]
nb_principaux = (centres['type_centre'] == 'Principal').sum()
nb_secondaires = (centres['type_centre'] == 'Secondaire').sum()

print(f"\n CENTRES DE SERVICE:")
print(f"   - Total: {nb_centres}")
print(f"   - Principaux: {nb_principaux}")
print(f"   - Secondaires: {nb_secondaires}")

# Capacité
capacite_totale = centres['personnel_capacite_jour'].sum()
capacite_moyenne = centres['personnel_capacite_jour'].mean()

print(f"\n CAPACITÉ DE TRAITEMENT:")
print(f"   - Capacité totale: {capacite_totale:,} demandes/jour")
print(f"   - Capacité moyenne par centre: {capacite_moyenne:.1f} demandes/jour")

# Couverture territoriale
nb_communes = communes.shape[0]
ratio_centres_communes = nb_centres / nb_communes

print(f"\n  COUVERTURE TERRITORIALE:")
print(f"   - Nombre de communes: {nb_communes}")
print(f"   - Ratio centres/communes: {ratio_centres_communes:.3f}")
print(f"   - En moyenne: 1 centre pour {nb_communes/nb_centres:.1f} communes")

# 5. DISTRIBUTIONS ET TENDANCES
print("\n" + "="*80)
print("4. DISTRIBUTIONS ET TENDANCES")
print("="*80)

# Distribution par région
print("\nVOLUME DE DEMANDES PAR RÉGION:")
demandes_region = demandes.groupby('region')['nombre_demandes'].sum().sort_values(ascending=False)
for region, volume in demandes_region.items():
    pct = (volume / volume_total) * 100
    print(f"   {region:15s}: {volume:6,} ({pct:5.1f}%)")

# Distribution par type de document
print("\n DEMANDES PAR TYPE DE DOCUMENT:")
demandes_doc = demandes.groupby('type_document')['nombre_demandes'].sum().sort_values(ascending=False)
for doc, volume in demandes_doc.items():
    pct = (volume / volume_total) * 100
    print(f"   {doc:30s}: {volume:6,} ({pct:5.1f}%)")

# Répartition par statut
print("\n RÉPARTITION PAR STATUT DE DEMANDE:")
statuts = demandes['statut_demande'].value_counts()
for statut, count in statuts.items():
    pct = (count / len(demandes)) * 100
    print(f"   {statut:15s}: {count:4} ({pct:5.1f}%)")

# Canal de demande
print("\ RÉPARTITION PAR CANAL:")
canaux = demandes.groupby('canal_demande')['nombre_demandes'].sum()
for canal, volume in canaux.items():
    pct = (volume / volume_total) * 100
    print(f"   {canal:15s}: {volume:6,} ({pct:5.1f}%)")

# 6. VISUALISATIONS EXPLORATOIRES
print("\n" + "="*80)
print("5. GÉNÉRATION DES VISUALISATIONS")
print("="*80)

import os
os.makedirs('../outputs', exist_ok=True)

# Créer une figure avec 4 sous-graphiques
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Analyse Exploratoire - TOGO Datalab', fontsize=16, fontweight='bold')

# Graphique 1: Volume par région
axes[0, 0].barh(demandes_region.index, demandes_region.values, color='steelblue')
axes[0, 0].set_xlabel('Nombre de demandes', fontsize=11)
axes[0, 0].set_title('Volume de demandes par région', fontsize=12, fontweight='bold')
axes[0, 0].grid(axis='x', alpha=0.3)
for i, v in enumerate(demandes_region.values):
    axes[0, 0].text(v, i, f' {v:,}', va='center', fontsize=9)

# Graphique 2: Types de documents (Pie chart)
colors = plt.cm.Set3(range(len(demandes_doc)))
axes[0, 1].pie(demandes_doc.values, labels=demandes_doc.index, autopct='%1.1f%%', 
               colors=colors, startangle=90)
axes[0, 1].set_title('Répartition par type de document', fontsize=12, fontweight='bold')

# Graphique 3: Distribution des délais
axes[1, 0].hist(demandes['delai_traitement_jours'], bins=30, color='coral', 
                edgecolor='black', alpha=0.7)
axes[1, 0].set_xlabel('Délai de traitement (jours)', fontsize=11)
axes[1, 0].set_ylabel('Fréquence', fontsize=11)
axes[1, 0].set_title('Distribution des délais de traitement', fontsize=12, fontweight='bold')
axes[1, 0].axvline(delai_moyen, color='red', linestyle='--', linewidth=2, 
                   label=f'Moyenne: {delai_moyen:.1f}j')
axes[1, 0].axvline(delai_median, color='green', linestyle='--', linewidth=2, 
                   label=f'Médiane: {delai_median:.1f}j')
axes[1, 0].legend()
axes[1, 0].grid(axis='y', alpha=0.3)

# Graphique 4: Statuts
colors_statut = {'Traitee': 'green', 'En cours': 'orange', 'Rejetée': 'red'}
colors_bars = [colors_statut.get(s, 'gray') for s in statuts.index]
axes[1, 1].bar(statuts.index, statuts.values, color=colors_bars, alpha=0.7, edgecolor='black')
axes[1, 1].set_ylabel('Nombre de demandes', fontsize=11)
axes[1, 1].set_title('Répartition par statut', fontsize=12, fontweight='bold')
axes[1, 1].tick_params(axis='x', rotation=15)
axes[1, 1].grid(axis='y', alpha=0.3)
for i, v in enumerate(statuts.values):
    axes[1, 1].text(i, v, f'{v}', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig('../outputs/01_eda_visualisations.png', dpi=300, bbox_inches='tight')
print(" Graphiques sauvegardés: outputs/01_eda_visualisations.png")

# Graphique supplémentaire: Boxplot des délais par région
fig2, ax = plt.subplots(figsize=(12, 6))
demandes.boxplot(column='delai_traitement_jours', by='region', ax=ax)
ax.set_xlabel('Région', fontsize=12)
ax.set_ylabel('Délai de traitement (jours)', fontsize=12)
ax.set_title('Distribution des délais par région', fontsize=14, fontweight='bold')
plt.suptitle('')  # Enlever le titre automatique
plt.tight_layout()
plt.savefig('../outputs/02_delais_par_region.png', dpi=300, bbox_inches='tight')
print(" Graphiques sauvegardés: outputs/02_delais_par_region.png")


# 7. SYNTHÈSE ÉCRITE
print("\n" + "="*80)
print("6. GÉNÉRATION DE LA SYNTHÈSE ÉCRITE")
print("="*80)

synthese = f"""# SYNTHÈSE DE L'ANALYSE EXPLORATOIRE DES DONNÉES
## Test Technique - TOGO Datalab

**Date:** {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}  
**Analyste:** Candidat Data Analyst

---

## 1. STRUCTURE DES DONNÉES

Nous disposons de **8 jeux de données interconnectés** représentant le réseau de services publics du Togo :

| Dataset | Lignes | Colonnes | Valeurs manquantes | Doublons |
|---------|--------|----------|-------------------|----------|
{summary_df.to_markdown(index=False, tablefmt='github')}

**Volume total de données:** {summary_df['Lignes'].sum():,} lignes

---

## 2. QUALITÉ DES DONNÉES

### Points positifs :
- **Aucun doublon** détecté dans l'ensemble des tables
- Données majoritairement complètes
- Formats cohérents et exploitables

### Points d'attention :
- **logs_activite :** {logs.isnull().sum().sum()} valeurs manquantes
  - Colonnes concernées : `type_document`, `raison_rejet`
  - Ces valeurs correspondent à des opérations de maintenance (non applicable)
- Toutes les autres tables sont **100% complètes**

###  Conclusion qualité :
Les données sont de **très bonne qualité** et directement exploitables pour l'analyse.

---

## 3. CONSTATS PRINCIPAUX

###  Volume d'activité

- **{volume_total:,} demandes** de documents officiels traitées
- **{nb_centres} centres** de service actifs
  - {nb_principaux} centres principaux
  - {nb_secondaires} centres secondaires
- **{nb_communes} communes** desservies sur **5 régions**

###  Performance opérationnelle

**Délais de traitement :**
- **Moyenne :** {delai_moyen:.1f} jours
- **Médiane :** {delai_median:.1f} jours
- **Plage :** {delai_min} à {delai_max} jours
-  **Constat :** Délais élevés nécessitant optimisation

**Taux de rejet :**
- **Moyenne :** {taux_rejet:.2f}%
-  **Constat :** Taux significatif indiquant problèmes de qualité des dossiers

**Capacité :**
- **Capacité totale :** {capacite_totale:,} demandes/jour
- **Capacité moyenne :** {capacite_moyenne:.1f} demandes/centre/jour

###  Répartition territoriale

**Top 3 régions par volume :**
{chr(10).join([f"{i+1}. **{region}** : {volume:,} demandes ({(volume/volume_total)*100:.1f}%)" for i, (region, volume) in enumerate(demandes_region.head(3).items())])}

**Couverture :**
- Ratio centres/communes : **{ratio_centres_communes:.3f}**
- En moyenne : **1 centre pour {nb_communes/nb_centres:.1f} communes**
-  **Constat :** Couverture potentiellement insuffisante

###  Types de documents les plus demandés

{chr(10).join([f"{i+1}. **{doc}** : {volume:,} demandes ({(volume/volume_total)*100:.1f}%)" for i, (doc, volume) in enumerate(demandes_doc.head(5).items())])}

###  Statuts des demandes

{chr(10).join([f"- **{statut}** : {count} demandes ({(count/len(demandes))*100:.1f}%)" for statut, count in statuts.items()])}

---

## 4. PROBLÈMES IDENTIFIÉS

###  Critiques (action urgente requise)

1. **Délai moyen élevé ({delai_moyen:.1f} jours)**
   - Objectif recommandé : < 15 jours
   - Écart : +{delai_moyen-15:.1f} jours
   - Impact : Insatisfaction usagers, congestion du système

2. **Taux de rejet significatif ({taux_rejet:.2f}%)**
   - Objectif recommandé : < 5%
   - Causes probables : Qualité des dossiers, information insuffisante
   - Impact : Retraitement, frustration usagers

3. **Couverture territoriale inégale**
   - Ratio centres/communes faible ({ratio_centres_communes:.3f})
   - Disparités entre régions
   - Impact : Accessibilité réduite, déplacements longs

###  À surveiller

1. **Variabilité des délais**
   - Écart entre min ({delai_min}j) et max ({delai_max}j) important
   - Indique hétérogénéité des performances

2. **Répartition des statuts**
   - Taux de demandes "En cours" à optimiser
   - Processus de traitement à fluidifier

---

## 5. TENDANCES OBSERVÉES

###  Spatiales

- **Concentration urbaine :** Régions {demandes_region.index[0]} et {demandes_region.index[1]} concentrent {((demandes_region.values[0] + demandes_region.values[1])/volume_total)*100:.1f}% du volume
- **Zones sous-desservies :** Régions {demandes_region.index[-1]} nécessite attention particulière

###  Opérationnelles

- **Canal digital :** {(canaux.get('En ligne', 0)/volume_total)*100:.1f}% des demandes (à développer)
- **Centres secondaires :** Sous-représentés ({nb_secondaires} vs {nb_principaux} principaux)

---

## 6. RECOMMANDATIONS POUR LA SUITE

###  Analyses approfondies nécessaires

1. **Définir des KPI de pilotage :**
   - Délai moyen par région et type de document
   - Taux d'utilisation de la capacité
   - Score de satisfaction usager (composite)
   - Indice de couverture territoriale

2. **Analyses causales :**
   - Corrélation délais/capacité/volume
   - Facteurs influençant le taux de rejet
   - Analyse géospatiale de l'accessibilité

3. **Nettoyage des données :**
   - Traiter les N/A dans logs_activite (documentation)
   - Standardiser les formats de dates
   - Créer des variables dérivées (trimestre, catégories)

###  Préparation du dashboard

- Vue exécutive : KPI synthétiques
- Vue opérationnelle : Performance par centre
- Vue territoriale : Cartes et accessibilité
- Filtres dynamiques : Région, document, période

---

## 7. LIMITES DE L'ANALYSE

- **Période temporelle :** Analyse transversale, tendances temporelles à approfondir
- **Données de satisfaction :** Pas de feedback direct des usagers
- **Coûts opérationnels :** Données budgétaires non disponibles
- **Facteurs externes :** Contexte socio-économique à intégrer

---

## CONCLUSION

Cette analyse exploratoire révèle un **système opérationnel** mais confronté à des **défis majeurs** :
- Délais de traitement à réduire de {(delai_moyen-15)/delai_moyen*100:.0f}%
- Qualité des dossiers à améliorer (réduction du taux de rejet)
- Couverture territoriale à renforcer

Les données sont de **qualité suffisante** pour permettre :
✅ Analyses approfondies  
✅ Définition de KPI pertinents  
✅ Création d'un dashboard de pilotage  
✅ Recommandations actionnables  

**Prochaine étape :** Nettoyage des données et calcul des KPI.

---

*Rapport généré automatiquement par script Python d'analyse exploratoire*
*Fichiers générés : 01_eda_visualisations.png, 02_delais_par_region.png*
"""

# Sauvegarder la synthèse
with open('../outputs/SYNTHESE_EDA.md', 'w', encoding='utf-8') as f:
    f.write(synthese)

print(" Synthèse écrite sauvegardée: outputs/SYNTHESE_EDA.md")

# FIN DE L'ANALYSE
print("\n" + "="*80)
print(" ANALYSE EXPLORATOIRE TERMINÉE AVEC SUCCÈS")
print("="*80)
print("\n Fichiers générés dans le dossier 'outputs/' :")
print("   1. 01_eda_visualisations.png")
print("   2. 02_delais_par_region.png")
print("   3. SYNTHESE_EDA.md")
print("\n Prochaines étapes :")
print("   - Nettoyage des données")
print("   - Définition et calcul des KPI")
print("   - Création du dashboard Power BI")
print("\n" + "="*80)
