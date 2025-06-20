from anki.collection import Collection
from aqt import mw
from aqt.utils import showInfo
import json
import os

_config_path = os.path.join(os.path.dirname(__file__), "rank_config.json")
ADDON_DIR = os.path.dirname(__file__)
WELCOME_PATH = os.path.join(ADDON_DIR, "welcome_config.json")

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
    try:
        with open(_config_path, "r") as f:
            data = json.load(f)
            print(f"[DEBUG] Loaded last_rank from file: {data.get('last_rank', '')}")
            return data.get("last_rank", "")
    except FileNotFoundError:
        print("[DEBUG] rank_config.json not found. Defaulting to empty last_rank.")
        return ""
    except json.JSONDecodeError as e:
        print(f"[DEBUG] JSON decode error: {e}")
        return ""

def set_last_rank(rank):
    try:
        with open(_config_path, "w") as f:
            json.dump({"last_rank": rank}, f)
            print(f"[DEBUG] Saved last_rank to file: {rank}")
    except Exception as e:
        print(f"[DEBUG] Error writing rank_config.json: {e}")

def get_rank_progress_range(xp: int):
    current_min = 0
    next_max = 0

    for i, (threshold, _) in enumerate(RANKS):
        if xp >= threshold:
            current_min = threshold
            if i + 1 < len(RANKS):
                next_max = RANKS[i + 1][0]
            else:
                next_max = threshold  # Final rank — bar should be full
    return current_min, next_max

def has_seen_welcome():
    try:
        with open(WELCOME_PATH, "r") as f:
            data = json.load(f)
            print("[DEBUG] Read welcome_config:", data)
            return data.get("welcome_shown", False)
    except FileNotFoundError:
        print("[DEBUG] welcome_config.json not found. Assuming first run.")
        return False

def set_welcome_shown():
    data = {"welcome_shown": True}
    with open(WELCOME_PATH, "w") as f:
        json.dump(data, f)
        print("[DEBUG] Saved welcome_config:", data)
