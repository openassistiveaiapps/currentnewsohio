# ---- Rule-based system ----
def rule_based_classifier(number):
    if number % 2 == 0:
        return "Even"
    else:
        return "Odd"

# Demo
numbers = [1, 2, 3, 4, 5, 6]
for n in numbers:
    print(f"{n} ➝ {rule_based_classifier(n)}")
