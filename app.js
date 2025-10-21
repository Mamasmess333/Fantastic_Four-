//simulates scanning food label 
function analyzeFoodLabel(labelText) {
  if (labelText.includes("Chicken")) {
    return { name: "Chicken Breast", protein: 31, carbs: 0, fat: 3 };
  } else {
    return { name: "Unknown", protein: 0, carbs: 0, fat: 0 };
  }
}

//simulates validating login
function validateLogin(email, password) {
  return email === "test@bitewise.com" && password === "1234"
    ? "success"
    : "error";
}

//simulates generating meal plan
function generateMealPlan(goal) {
  if (goal.includes("budget")) {
    return ["Oatmeal", "Chicken & Rice", "Veggie Stir Fry"];
  }
  return [];
}

//simulates saving food items
function saveToLog(foodItem, log = []) {
  log.push(foodItem);
  return log;
}

module.exports = {
  analyzeFoodLabel,
  validateLogin,
  generateMealPlan,
  saveToLog,
};

