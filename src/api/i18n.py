# Mini couche i18n FR pour l'UI
# Les clés correspondent aux noms des champs (dataset / modèle)

I18N_FR = {
    "duration": {"label": "Durée du crédit (mois)"},
    "credit_amount": {"label": "Montant du crédit"},
    "installment_commitment": {"label": "Taux d’endettement (1–4)"},
    "residence_since": {"label": "Ancienneté du domicile (1–4)"},
    "age": {"label": "Âge"},
    "existing_credits": {"label": "Crédits existants"},
    "num_dependents": {"label": "Personnes à charge"},
    "checking_status": {
        "label": "Statut du compte courant",
        "values": {
            "no checking": "Aucun compte courant",
            "<0": "Solde inférieur à 0€",
            "0<=X<200": "Solde entre 0€ et 200€",
            ">=200": "Solde supérieur à 200€",
        },
    },
    "credit_history": {
        "label": "Historique de crédit",
        "values": {
            "existing paid": "Crédits existants remboursés",
            "delayed previously": "Retards de paiement antérieurs",
            "critical/other existing credit": "Historique critique",
            "all paid": "Tous les crédits remboursés",
            "no credits/all paid": "Aucun crédit / tous les crédits remboursés",
        },
    },
    "purpose": {
        "label": "Objet du crédit",
        "values": {
            "new car": "Voiture neuve",
            "used car": "Voiture d’occasion",
            "furniture/equipment": "Mobilier / équipement",
            "radio/tv": "Radio / TV",
            "education": "Éducation",
            "business": "Activité professionnelle",
            "domestic appliance": "Appareil électroménager",
            "repairs": "Réparations",
            "other": "Autre",
            "retraining": "Recyclage",
        },
    },
    "savings_status": {
        "label": "Épargne",
        "values": {
            "no known savings": "Aucune épargne connue",
            "500<=X<1000": "Épargne entre 500€ et 1000€",
            ">=1000": "Épargne ≥ 1000€",
            "<100": "Épargne < 100€",
            "100<=X<500": "Épargne entre 100€ et 500€",
        },
    },
    "employment": {
        "label": "Ancienneté professionnelle",
        "values": {
            "unemployed": "Sans emploi",
            "<1": "Moins d’un an",
            "1<=X<4": "Entre 1 et 4 ans",
            "4<=X<7": "Entre 4 et 7 ans",
            ">=7": "Plus de 7 ans",
        },
    },
    "personal_status": {
        "label": "Situation personnelle",
        "values": {
            "male single": "Homme célibataire",
            "male div/sep": "Homme divorcé / séparé",
            "female div/dep/mar": "Femme divorcée / séparée / mariée",
            "male mar/wid": "Homme marié / veuf",
        },
    },
    "other_parties": {
        "label": "Autres garants",
        "values": {
            "none": "Aucun",
            "co applicant": "Co-emprunteur",
            "guarantor": "Garant",
        },
    },
    "property_magnitude": {
        "label": "Patrimoine",
        "values": {
            "real estate": "Immobilier",
            "car": "Véhicule",
            "life insurance": "Assurance-vie",
            "no known property": "Aucun patrimoine connu",
        },
    },
    "other_payment_plans": {
        "label": "Autres plans de paiement",
        "values": {
            "none": "Aucun",
            "bank": "Banque",
            "stores": "Magasins",
        },
    },
    "housing": {
        "label": "Logement",
        "values": {
            "rent": "Location",
            "own": "Propriétaire",
            "for free": "Logé gratuitement",
        },
    },
    "job": {
        "label": "Profession",
        "values": {
            "unskilled resident": "Non qualifié (résident)",
            "skilled": "Employé qualifié",
            "high qualif/self emp/mgmt": "Cadre / indépendant",
            "unemp/unskilled non res": "chômeur / non qualifié sans domicile fixe",
        },
    },
    "own_telephone": {
        "label": "Téléphone personnel",
        "values": {
            "none": "Aucun",
            "yes": "Oui",
        },
    },
    "foreign_worker": {
        "label": "Travailleur étranger",
        "values": {
            "yes": "Oui",
            "no": "Non",
        },
    },
}
