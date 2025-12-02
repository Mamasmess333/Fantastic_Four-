import random
from typing import Dict, List, Optional, Tuple

from backend.services.nutrition_service import _load_food_library

MEAL_SLOTS = ["breakfast", "lunch", "dinner"]


def _filter_library(goal: str, budget: Tuple[float, float], preferences: List[str], allergies: List[str]):
    low, high = budget
    library = []
    for item in _load_food_library():
        price = item.get("price", 0)
        if price < low or price > high:
            continue
        if allergies and any(allergen in item.get("ingredients", []) for allergen in allergies):
            continue
        if preferences and not any(pref in item.get("tags", []) for pref in preferences):
            continue
        library.append(item)
    return library or _load_food_library()


def generate_meal_plan(
    *,
    goal: str,
    budget: Tuple[float, float],
    preferences: Optional[List[str]] = None,
    allergies: Optional[List[str]] = None,
    days: int = 3,
) -> Dict:
    prefs = preferences or []
    allergy_list = allergies or []
    pool = _filter_library(goal, budget, prefs, allergy_list)
    random.seed(goal + str(budget))

    plan_days = []
    total_cost = 0.0

    for day in range(days):
        meals = []
        for slot in MEAL_SLOTS:
            choice = random.choice(pool)
            recipes = choice.get("recipes") or [None]
            if isinstance(recipes, list):
                recipe = recipes[0]
            else:
                recipe = recipes

            meals.append(
                {
                    "slot": slot,
                    "item": choice["name"],
                    "macros": choice.get("macros"),
                    "recipe": recipe,
                    "price": choice.get("price"),
                }
            )
            total_cost += choice.get("price", 0)
        plan_days.append({"day": day + 1, "meals": meals})

    return {
        "goal": goal,
        "budget": {"min": budget[0], "max": budget[1]},
        "days": plan_days,
        "estimated_cost": round(total_cost, 2),
        "average_cost_per_day": round(total_cost / days, 2),
    }

