# DÉFINITION DES KPI - TOGO DATALAB
## Tableau des Indicateurs Clés de Performance

**Test Technique - Optimisation du Réseau de Services Publics**  
**Date:** Janvier 2026

---

## KPI 1: Délai Moyen de Traitement (DMT)

| Élément | Description |
|---------|-------------|
| **Nom du KPI** | Délai Moyen de Traitement (DMT) |
| **Objectif métier** | Mesurer l'efficacité du système de traitement des demandes. Un délai réduit améliore la satisfaction usager et réduit la congestion. Permet d'identifier les goulots d'étranglement. |
| **Description / Interprétation** | Nombre moyen de jours entre la soumission d'une demande et sa finalisation. Un DMT >20 jours indique des problèmes de capacité ou d'organisation. **Cible: <15 jours**. Statut actuel: Alerte (22.7j) |
| **Règle de calcul** | DMT = SOMME(délai_traitement × nombre_demandes) / SOMME(nombre_demandes)<br>Pondération par le volume pour tenir compte de l'impact réel |
| **Requête SQL** | ```sql<br>SELECT <br>  d.region,<br>  d.type_document,<br>  SUM(d.delai_traitement_jours * d.nombre_demandes) / SUM(d.nombre_demandes) AS delai_moyen_jours<br>FROM demandes_service_public d<br>WHERE d.statut_demande IN ('Traitee', 'Rejetée')<br>GROUP BY d.region, d.type_document<br>ORDER BY delai_moyen_jours DESC;<br>``` |

---

## KPI 2: Taux d'Utilisation de la Capacité (TUC)

| Élément | Description |
|---------|-------------|
| **Nom du KPI** | Taux d'Utilisation de la Capacité (TUC) |
| **Objectif métier** | Évaluer si les ressources (personnel, guichets) sont optimalement utilisées. Permet d'identifier les centres en surcharge nécessitant renforcement ou les centres sous-utilisés pouvant absorber plus de charge. |
| **Description / Interprétation** | Ratio entre le volume réel traité et la capacité théorique. TUC < 70% = sous-utilisation, TUC 80-95% = optimal, TUC >100% = surcharge. **Cible: 80-95%**. Statut: 🔴 Critique (3.4%) |
| **Règle de calcul** | TUC = (Demandes traitées / Capacité annuelle) × 100<br>Capacité annuelle = personnel_capacite_jour × 250 jours ouvrables |
| **Requête SQL** | ```sql<br>SELECT <br>  c.centre_id,<br>  c.nom_centre,<br>  c.region,<br>  c.personnel_capacite_jour * 250 AS capacite_annuelle,<br>  SUM(l.nombre_traite) AS demandes_traitees,<br>  ROUND((SUM(l.nombre_traite) * 100.0) / (c.personnel_capacite_jour * 250), 2) AS taux_utilisation_pct<br>FROM centres_service c<br>LEFT JOIN logs_activite l ON c.centre_id = l.centre_id<br>WHERE l.type_operation = 'Traitement'<br>GROUP BY c.centre_id, c.nom_centre, c.region, c.personnel_capacite_jour<br>ORDER BY taux_utilisation_pct DESC;<br>``` |

---

## KPI 3: Ratio Population/Centre (RPC)

| Élément | Description |
|---------|-------------|
| **Nom du KPI** | Ratio Population/Centre (RPC) |
| **Objectif métier** | Mesurer l'accessibilité géographique des services. Un RPC élevé signifie que la population doit parcourir de longues distances. Permet de prioriser l'ouverture de nouveaux centres. |
| **Description / Interprétation** | Nombre moyen d'habitants desservis par centre dans une région. RPC >80,000 = couverture insuffisante, RPC <60,000 = bonne couverture. **Cible: <80,000 hab/centre**. Statut: Alerte (117,801) |
| **Règle de calcul** | RPC = Population totale région / Nombre de centres région |
| **Requête SQL** | ```sql<br>SELECT <br>  s.region,<br>  SUM(s.population) AS population_totale,<br>  COUNT(DISTINCT c.centre_id) AS nombre_centres,<br>  ROUND(SUM(s.population) / COUNT(DISTINCT c.centre_id), 0) AS ratio_population_centre<br>FROM donnees_socioeconomiques s<br>LEFT JOIN centres_service c ON s.region = c.region<br>GROUP BY s.region<br>ORDER BY ratio_population_centre DESC;<br>``` |

---

## KPI 4: Indice de Couverture Territoriale (ICT)

| Élément | Description |
|---------|-------------|
| **Nom du KPI** | Indice de Couverture Territoriale (ICT) |
| **Objectif métier** | Évaluer la densité du maillage administratif. Identifier les régions avec trop peu de centres par rapport au nombre de communes. Guide la stratégie d'expansion du réseau. |
| **Description / Interprétation** | Ratio centres/communes. ICT < 0.3 = couverture faible (>3 communes par centre), ICT > 0.5 = bonne couverture. **Cible: >0.3**. Statut: 🟡 Attention (0.297) |
| **Règle de calcul** | ICT = Nombre de centres / Nombre de communes |
| **Requête SQL** | ```sql<br>SELECT <br>  cm.region,<br>  COUNT(DISTINCT cm.commune_id) AS nombre_communes,<br>  COUNT(DISTINCT c.centre_id) AS nombre_centres,<br>  ROUND(COUNT(DISTINCT c.centre_id) * 1.0 / COUNT(DISTINCT cm.commune_id), 3) AS indice_couverture<br>FROM details_communes cm<br>LEFT JOIN centres_service c ON cm.region = c.region<br>GROUP BY cm.region<br>ORDER BY indice_couverture ASC;<br>``` |

---

## KPI 5: Taux de Satisfaction Usager (TSU)

| Élément | Description |
|---------|-------------|
| **Nom du KPI** | Taux de Satisfaction Usager (TSU) |
| **Objectif métier** | Mesurer la qualité perçue du service de manière composite. Combine délais, rejets et temps d'attente pour un indicateur global de l'expérience usager. Permet d'identifier les centres problématiques. |
| **Description / Interprétation** | Score composite pondéré: délai (40%), taux rejet (30%), temps attente (30%). TSU <60% = service insatisfaisant, TSU >75% = bon service. **Cible: >75%**. Statut: 🟡 Attention (42.1%) |
| **Règle de calcul** | TSU = (0.40 × Score_délai) + (0.30 × Score_rejet) + (0.30 × Score_attente)<br>Score_délai = MAX(0, 100 - (délai_moyen - 15) × 4)<br>Score_rejet = MAX(0, 100 - taux_rejet × 20)<br>Score_attente = MAX(0, 100 - (temps_attente - 45) × 2) |
| **Requête SQL** | ```sql<br>SELECT <br>  c.centre_id,<br>  c.nom_centre,<br>  c.region,<br>  ROUND(AVG(l.delai_effectif), 1) AS delai_moyen,<br>  ROUND(AVG(l.nombre_rejete * 100.0 / NULLIF(l.nombre_traite, 0)), 2) AS taux_rejet_pct,<br>  ROUND(AVG(l.temps_attente_moyen_minutes), 1) AS temps_attente_moyen,<br>  ROUND(<br>    0.40 * GREATEST(0, 100 - (AVG(l.delai_effectif) - 15) * 4) +<br>    0.30 * GREATEST(0, 100 - AVG(l.nombre_rejete * 100.0 / NULLIF(l.nombre_traite, 0)) * 20) +<br>    0.30 * GREATEST(0, 100 - (AVG(l.temps_attente_moyen_minutes) - 45) * 2),<br>  2) AS taux_satisfaction_pct<br>FROM centres_service c<br>LEFT JOIN logs_activite l ON c.centre_id = l.centre_id<br>WHERE l.type_operation = 'Traitement'<br>GROUP BY c.centre_id, c.nom_centre, c.region<br>ORDER BY taux_satisfaction_pct ASC;<br>``` |

---

## KPI 6: Taux de Rejet Global (TRG)

| Élément | Description |
|---------|-------------|
| **Nom du KPI** | Taux de Rejet Global (TRG) |
| **Objectif métier** | Identifier les problèmes de qualité des dossiers et les besoins en accompagnement des usagers. Un TRG élevé génère des coûts (retraitement) et de l'insatisfaction. Guide les campagnes d'information. |
| **Description / Interprétation** | Pourcentage de demandes rejetées. TRG >10% = problèmes majeurs, TRG 5-10% = attention requise, TRG <5% = acceptable. **Cible: <5%**. Statut: 🔴 Critique (49.16%) |
| **Règle de calcul** | TRG = (Nombre demandes rejetées / Total demandes traitées) × 100 |
| **Requête SQL** | ```sql<br>SELECT <br>  d.region,<br>  d.type_document,<br>  COUNT(*) AS total_demandes,<br>  SUM(CASE WHEN d.statut_demande = 'Rejetée' THEN 1 ELSE 0 END) AS demandes_rejetees,<br>  ROUND(SUM(CASE WHEN d.statut_demande = 'Rejetée' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS taux_rejet_pct<br>FROM demandes_service_public d<br>WHERE d.statut_demande IN ('Traitee', 'Rejetée')<br>GROUP BY d.region, d.type_document<br>ORDER BY taux_rejet_pct DESC;<br>``` |

---

## KPI BONUS: Score d'Urgence d'Intervention (SUI)

| Élément | Description |
|---------|-------------|
| **Nom du KPI** | Score d'Urgence d'Intervention (SUI) |
| **Objectif métier** | Prioriser objectivement les centres nécessitant une intervention urgente. Combine surcharge, délais, rejets et infrastructure pour guider l'allocation des ressources limitées. |
| **Description / Interprétation** | Score composite sur 100: surcharge (40%), délais (30%), rejets (20%), équipement (10%). SUI >70 = intervention urgente, SUI 50-70 = surveillance, SUI <50 = stable. **Cible: <70**. |
| **Règle de calcul** | SUI = (0.40 × Score_surcharge) + (0.30 × Score_délai) + (0.20 × Score_rejet) + (0.10 × Score_équipement)<br>Scores normalisés sur 100 pour chaque dimension |
| **Requête SQL** | ```sql<br>SELECT <br>  c.centre_id,<br>  c.nom_centre,<br>  c.region,<br>  ROUND(<br>    0.40 * (CASE WHEN AVG(l.nombre_traite) > c.personnel_capacite_jour THEN 100 <br>                 ELSE (AVG(l.nombre_traite) / c.personnel_capacite_jour) * 100 END) +<br>    0.30 * (AVG(l.delai_effectif) / 45.0 * 100) +<br>    0.20 * (AVG(l.nombre_rejete * 100.0 / NULLIF(l.nombre_traite, 0))) +<br>    0.10 * (CASE WHEN c.equipement_numerique = 'Limite' THEN 100 <br>                 WHEN c.equipement_numerique = 'Partiel' THEN 60 ELSE 20 END),<br>  2) AS score_urgence_intervention<br>FROM centres_service c<br>LEFT JOIN logs_activite l ON c.centre_id = l.centre_id<br>WHERE l.type_operation = 'Traitement'<br>GROUP BY c.centre_id, c.nom_centre, c.region, c.personnel_capacite_jour, c.equipement_numerique<br>ORDER BY score_urgence_intervention DESC;<br>``` |

---

## SYNTHÈSE DES KPI

| # | KPI | Valeur Actuelle | Cible | Statut | Priorité |
|---|-----|-----------------|-------|--------|----------|
| 1 | Délai Moyen Traitement | 22.39 jours | <15j | 🔴 | P1 |
| 2 | Taux Utilisation Capacité | 3.4% | 80-95% | 🔴 | P1 |
| 3 | Ratio Population/Centre | 117,801 | <80,000 | 🔴 | P2 |
| 4 | Indice Couverture | 0.297 | >0.3 | 🟡 | P2 |
| 5 | Satisfaction Usager | 42.1% | >75% | 🟡 | P1 |
| 6 | Taux Rejet Global | 49.16% | <5% | 🔴 | P1 |
| BONUS | Score Urgence | 64.0 | <70 | 🟢 | - |

**Légende Statut:**
- 🔴 Rouge: Critique - Action urgente
- 🟡 Orange: Attention - Surveillance accrue
- 🟢 Vert: Conforme - Maintenir

**Légende Priorité:**
- P1: Action immédiate (0-3 mois)
- P2: Action moyen terme (3-12 mois)

---

## NOTES MÉTHODOLOGIQUES

### Fréquence de calcul recommandée:
- **Hebdomadaire:** KPI 1, 5, 6 (opérationnels)
- **Mensuelle:** KPI 2, 7 (ressources)
- **Trimestrielle:** KPI 3, 4 (stratégiques)

### Seuils d'alerte:
- 🔴 Rouge: Performance < 60% de la cible
- 🟡 Orange: Performance 60-80% de la cible
- 🟢 Vert: Performance > 80% de la cible

### Sources de données:
- `demandes_service_public`: Volume, délais, rejets
- `centres_service`: Capacité, localisation
- `logs_activite`: Performance opérationnelle réelle
- `details_communes`: Données territoriales
- `donnees_socioeconomiques`: Population

### Utilisation dans Power BI:
Ces KPI peuvent être implémentés comme **mesures DAX** dans Power BI:
- Les requêtes SQL servent de référence pour la logique
- Les calculs sont adaptables en DAX
- Utiliser des tables de calcul pour les scores composites

---

