"""Définition du schéma des features pour le dataset credit-g."""

from typing import List

from .config import TARGET_COL

# Liste des colonnes du dataset credit-g (OpenML)
# On sépare les variables numériques et catégorielles.
# Si besoin, on ajustera après inspection de l'EDA.

NUMERIC_FEATURES: List[str] = [
    "duration",
    "credit_amount",
    "installment_commitment",
    "residence_since",
    "age",
    "existing_credits",
    "num_dependents",
]

CATEGORICAL_FEATURES: List[str] = [
    "checking_status",
    "credit_history",
    "purpose",
    "savings_status",
    "employment",
    "personal_status",
    "other_parties",
    "property_magnitude",
    "other_payment_plans",
    "housing",
    "job",
    "own_telephone",
    "foreign_worker",
]

ALL_FEATURES: List[str] = NUMERIC_FEATURES + CATEGORICAL_FEATURES


def get_feature_names() -> List[str]:
    """Retourne la liste complète des features en entrée du modèle."""
    return ALL_FEATURES


def get_target_name() -> str:
    """Retourne le nom de la variable cible."""
    return TARGET_COL
