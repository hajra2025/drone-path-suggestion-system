def retrieve_rule(mission):
    if mission == "high risk":
        return "Avoid risky areas even if path is longer."
    elif mission == "low battery":
        return "Choose shortest path to save battery."
    else:
        return "Balance between distance and safety."


def get_weights(mission):
    if mission == "high risk":
        return 1, 100   # VERY HIGH risk penalty
    elif mission == "low battery":
        return 10, 1    # prioritize distance
    else:
        return 3, 5     # balanced