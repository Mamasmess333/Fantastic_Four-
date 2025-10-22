def test_mock_meal_plan():
    
    def generate_meal_plan(goal="lose fat"):
        if goal == "lose fat":
            return ["Oatmeal with berries", "Grilled chicken salad", "Steamed veggies"]
        elif goal == "gain muscle":
            return ["Protein smoothie", "Salmon with rice", "Greek yogurt"]
        else:
            return ["Balanced breakfast", "Mixed lunch", "Light dinner"]
    
    plan = generate_meal_plan("gain muscle")

    assert isinstance(plan, list)
    assert "Protein smoothie" in plan
    assert len(plan) == 3
