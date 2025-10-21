const { analyzeFoodLabel } = require("./app");

test("Food scanning identifies Chicken Breast and returns correct macros", () => {
  const result = analyzeFoodLabel("Grilled Chicken Breast, Nutrition Facts...");
  expect(result.name).toBe("Chicken Breast");
  expect(result.protein).toBe(31);
  expect(result.carbs).toBe(0);
  expect(result.fat).toBe(3);
});
