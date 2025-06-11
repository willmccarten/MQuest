from anki.collection import Collection
from aqt import mw

# badge thresholds
TIER_THRESHOLDS = [
    (1, "Diamond"),
    (0.80, "Platinum"),
    (0.60, "Gold"),
    (0.33, "Silver"),
    (0.01, "Bronze"),
    (0.00, None),  # No badge yet
]

# Subject deck names
PARENT_DECK = "MileDown's MCAT Decks"
SUBDECKS = [
    "Behavioral",
    "Biochemistry",
    "Biology",
    "Essential Equations",
    "General Chemistry",
    "Organic Chemistry",
    "Physics and Math"
]

def get_full_deck_name(subdeck):
    return f"{PARENT_DECK}::{subdeck}"

def get_total_and_seen_card_counts(deck_name: str):
    """Returns (total_cards, reviewed_cards) for a given deck."""
    col = mw.col
    # All cards in the deck
    total = col.db.scalar(
        "SELECT COUNT(*) FROM cards WHERE did IN (SELECT id FROM decks WHERE name = ?)", deck_name
    )
    # Reviewed cards (learned or graduated)
    seen = col.db.scalar(
        "SELECT COUNT(*) FROM cards WHERE did IN (SELECT id FROM decks WHERE name = ?) AND (type > 0)", deck_name
    )
    return total, seen

def determine_badge_tier(progress: float):
    for threshold, tier in TIER_THRESHOLDS:
        if progress >= threshold:
            return tier
    return None

def get_all_badge_data():
    badge_data = {}

    for subdeck in SUBDECKS:
        full_name = get_full_deck_name(subdeck)
        total, seen = get_total_and_seen_card_counts(full_name)
        progress = seen / total if total else 0.0 
        tier = determine_badge_tier(progress)

        badge_data[subdeck] = {
            "deck_name": full_name,
            "total": total,
            "seen": seen,
            "progress": progress,
            "tier": tier
        }

    return badge_data
