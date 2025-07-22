def generalize(memory):
    generalized = {}

    for pattern, outcomes in memory.items():
        if not outcomes:
            continue

        # Find the most common outcome and its count
        winner, max_count = max(outcomes.items(), key=lambda item: item[1])

        # Keep only the "strong" outcomes
        # A strong outcome is the winner or any outcome that's at least 50% as likely
        strong_outcomes = {
            pred: count for pred, count in outcomes.items()
            if count >= max_count * 0.5 
        }

        # If there are any strong outcomes, add them to the new memory
        if strong_outcomes:
            generalized[pattern] = strong_outcomes

    return generalized