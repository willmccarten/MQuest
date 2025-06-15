from anki.collection import Collection
from aqt import mw
from aqt.utils import showInfo

# badge thresholds
TIER_THRESHOLDS = [
    (1, "Diamond"),
    (0.75, "Gold"),
    (0.50, "Silver"),
    (0.25, "Bronze"),
    (0.05, "Wood"),
    (0.00, None),  # No badge yet
]

# Subject deck names
PARENT_DECK = "AnKing-MCAT::MileDown's MCAT Decks"
SUBDECKS = [
    "Behavioral",
    "Biochemistry",
    "Biology",
    "Essential Equations",
    "General Chemistry",
    "Organic Chemistry",
    "Physics and Math"
]

TIER_XP = {
    "Wood": 1,
    "Bronze": 2,
    "Silver": 3,
    "Gold": 4,
    "Diamond": 5,
    None: 0
}

RANKS = [
    (0, "Baby Gator"),
    (5, "Spry Sophomore"),
    (10, "Jolly Junior"),
    (15, "Senior Gator"),
    (20, "Hearty Hoya"),
    (25, "Mighty Med Student"),
    (30, "Remarkable Resident"),
    (35, "Dr. White Coat Champion")
]


def get_full_deck_name(subdeck):
    return f"{PARENT_DECK}::{subdeck}"

def get_total_and_seen_card_counts(deck_name: str):
    """Returns (total_cards, reviewed_cards) for a given deck name."""
    col = mw.col
    deck_id = col.decks.id(deck_name)

    total = col.db.scalar(
        "SELECT COUNT(*) FROM cards WHERE did = ?", deck_id
    )
    seen = col.db.scalar(
        "SELECT COUNT(*) FROM cards WHERE did = ? AND type > 0", deck_id
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

def calculate_total_xp(badge_data):
    xp = 0
    for badge in badge_data.values():
        tier = badge["tier"]
        xp += TIER_XP.get(tier, 0)
    return xp

def get_current_rank(xp):
    current = RANKS[0][1]
    for threshold, rank in RANKS:
        if xp >= threshold:
            current = rank
    return current

def get_next_rank_info(xp):
    for i, (threshold, rank) in enumerate(RANKS):
        if xp < threshold:
            next_rank = rank
            next_threshold = threshold
            return next_rank, next_threshold
    return None, None  # edge case of at top rank

def get_last_rank():
    config = mw.addonManager.getConfig(__name__) or {}
    return config.get("last_rank", "")

def set_last_rank(rank):
    config = mw.addonManager.getConfig(__name__) or {}
    config["last_rank"] = rank
    mw.addonManager.writeConfig(__name__, config)