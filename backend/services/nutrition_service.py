import json
import math
import random
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Tuple

RATING_LEVELS = ["Bad", "Mid", "Good"]


@lru_cache
def _load_food_library() -> List[dict]:
    data_path = Path(__file__).resolve().parents[1] / "data" / "food_library.json"
    if not data_path.exists():
        return []
    with data_path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def _score_macros(macros: Dict[str, float]) -> float:
    sugar = macros.get("sugar", 0)
    sodium = macros.get("sodium", 0)
    fiber = macros.get("fiber", 0)
    protein = macros.get("protein", 0)
    processing_penalty = macros.get("processing_penalty", 0)

    score = 50 + protein * 2 + fiber * 3 - sugar * 1.5 - (sodium / 100) * 2
    score -= processing_penalty
    return max(0, min(100, score))


def _rating_from_score(score: float) -> str:
    if score >= 70:
        return "Good"
    if score >= 45:
        return "Mid"
    return "Bad"


def _match_foods_from_labels(labels: List[str], text: Optional[str]) -> List[dict]:
    tokens = set(label.lower() for label in labels)
    if text:
        tokens.update(token.strip(",.") for token in text.lower().split())
    matches = []
    for item in _load_food_library():
        ingredients = set(item.get("ingredients", []))
        if any(ing in tokens for ing in ingredients) or item["name"].lower() in tokens:
            matches.append(item)
    return matches or _load_food_library()[:2]


def summarize_analysis(
    *,
    labels: List[str],
    text: Optional[str],
    user_goal: Optional[str],
    budget: Optional[Tuple[float, float]],
) -> Dict:
    matches = _match_foods_from_labels(labels, text)
    reasons = []
    alternatives = []
    average_price = 0
    combined_macros = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0, "fiber": 0, "sugar": 0, "sodium": 0}

    for match in matches:
        macros = match.get("macros", {})
        for key in combined_macros:
            combined_macros[key] += macros.get(key, 0)
        average_price += match.get("price", 0)
        if match.get("alternatives"):
            alternatives.extend(match["alternatives"])

        if macros.get("sugar", 0) > 25:
            reasons.append(f"{match['name']} is very high in sugar ({macros['sugar']}g).")
        if macros.get("sodium", 0) > 700:
            reasons.append(f"{match['name']} exceeds the sodium limit ({macros['sodium']}mg).")
        if match.get("processing_level") == "ultra":
            reasons.append(f"{match['name']} is ultra-processed with additives {', '.join(match['additives'])}.")

    if matches:
        average_price /= len(matches)
        for key in combined_macros:
            combined_macros[key] = round(combined_macros[key] / len(matches), 1)

    score = _score_macros({**combined_macros, "processing_penalty": 10 if reasons else 0})
    rating = _rating_from_score(score)

    if not reasons:
        reasons.append("Balanced macros and low additives detected.")
    if user_goal == "budget" and budget:
        low, high = budget
        if average_price > high:
            reasons.append(f"Average price ${average_price:.2f} exceeds your budget.")
            rating = "Mid"

    alternative_choice = alternatives[:3] or ["Swap sugary drinks with infused water", "Add leafy greens for fiber"]
    suggestion = random.choice(alternative_choice)

    return {
        "rating": rating,
        "score": round(score, 1),
        "detected_items": [item["name"] for item in matches],
        "macros": combined_macros,
        "reasons": reasons,
        "suggestion": suggestion,
        "estimated_price": round(average_price, 2),
    }

