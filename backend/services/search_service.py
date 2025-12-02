from typing import Dict, List

from backend.services.nutrition_service import _load_food_library, _rating_from_score, _score_macros


def _health_score(item: dict) -> float:
    macros = item.get("macros", {}).copy()
    if item.get("processing_level") == "ultra":
        macros["processing_penalty"] = macros.get("processing_penalty", 0) + 20
    return _score_macros(macros)


def _build_result(item: dict) -> Dict:
    score = _health_score(item)
    return {
        "name": item["name"],
        "health_score": round(score, 1),
        "rating": _rating_from_score(score),
        "macros": item.get("macros"),
        "alternatives": item.get("alternatives", []),
        "tags": item.get("tags", []),
    }


def search_foods(query: str) -> List[Dict]:
    query_lower = query.lower()
    results = []
    for item in _load_food_library():
        haystack = " ".join(
            [
                item.get("name", ""),
                " ".join(item.get("ingredients", [])),
                " ".join(item.get("tags", [])),
            ]
        ).lower()
        if query_lower in haystack:
            results.append(_build_result(item))
    results.sort(key=lambda x: x["health_score"], reverse=True)
    return results


def recommend_from_labels(labels: List[str]) -> List[Dict]:
    """Map Rekognition labels to curated catalog suggestions."""
    tokens = {label.lower() for label in labels}
    matches = []
    for item in _load_food_library():
        searchable = {
            item.get("name", "").lower(),
            *[tag.lower() for tag in item.get("tags", [])],
            *[ingredient.lower() for ingredient in item.get("ingredients", [])],
        }
        if tokens & searchable:
            matches.append(_build_result(item))
    matches.sort(key=lambda x: x["health_score"], reverse=True)
    return matches[:10]

