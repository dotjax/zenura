def generalize(memory):
    generalized = {}

    for pattern, outcomes in memory.items():
        total = sum(outcomes.values())
        if total < 3:
            # Too sparse to generalize usefully
            continue

        # Example: Build averaged weights for stronger generalization
        average_prediction = int(round(
            sum(pred * count for pred, count in outcomes.items()) / total
        ))

        # Store generalized pattern
        generalized[pattern] = {
            average_prediction: total
        }

    return generalized
