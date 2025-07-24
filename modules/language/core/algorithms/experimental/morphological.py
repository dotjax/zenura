import random

# Define basic operators and expectations
allowed_ops = [
    ("x + y", lambda x, y: x + y),
    ("x - y", lambda x, y: x - y),
    ("x ^ y", lambda x, y: x ^ y),
    ("x & y", lambda x, y: x & y),
    ("x | y", lambda x, y: x | y),
]

expectations = [
    ("z % 2 == 0", lambda z: z % 2 == 0),
    ("z > 100", lambda z: z > 100),
    ("z == 0", lambda z: z == 0),
    ("z < 128", lambda z: z < 128),
]

# Observed triplets (x, y → z)
observed = [
    (5, 3, 8),
    (10, 2, 12),
    (4, 1, 5),
    (7, 7, 0),
    (100, 28, 128),
]

# Rule factories
def make_if(op, target):
    return lambda x, y: op(x, y) == target

def make_then(exp):
    return lambda z: exp(z)

# Rule generator
def generate_rules():
    rules = []
    for op_label, op in allowed_ops:
        for exp_label, exp in expectations:
            for target in range(0, 256, 16):  # 0 to 255 in steps
                rules.append({
                    "op_label": op_label,
                    "target": target,
                    "exp_label": exp_label,
                    "if": make_if(op, target),
                    "then": make_then(exp),
                    "strength": 128
                })
    return rules

# Rule evaluator
def evaluate_rules(rules, observed):
    for rule in rules:
        score = 0
        for x, y, z in observed:
            if rule["if"](x, y):
                if rule["then"](z):
                    score += 1
                else:
                    score -= 1
        rule["strength"] = max(0, min(255, rule["strength"] + score))
    return rules

# Rule mutator
def mutate_rule(rule):
    new = rule.copy()
    choice = random.choice(["target_shift", "expectation_change"])
    if choice == "target_shift":
        delta = random.choice([-8, -4, 4, 8])
        new_target = max(0, min(255, new["target"] + delta))
        op_func = dict(allowed_ops)[new["op_label"]]
        new["target"] = new_target
        new["if"] = make_if(op_func, new_target)
    elif choice == "expectation_change":
        new["exp_label"], exp_func = random.choice(expectations)
        new["then"] = make_then(exp_func)
    new["strength"] = 128
    return new

# Rule compressor (deduplicator)
def compress_rules(rules):
    seen = set()
    unique = []
    for r in rules:
        key = (r["op_label"], r["target"], r["exp_label"])
        if key not in seen:
            seen.add(key)
            unique.append(r)
    return unique

# Rule evolution pass
def evolve(rules):
    survivors = [r for r in rules if r["strength"] >= 32]
    mutated = [mutate_rule(r) for r in survivors if random.random() < 0.3]
    return compress_rules(survivors + mutated)

# Run the system
rules = generate_rules()
for _ in range(10):  # 10 evolution cycles
    rules = evaluate_rules(rules, observed)
    rules = evolve(rules)

# Print top surviving rules
print("\nTop Surviving Rules:\n")
top_rules = sorted(rules, key=lambda r: -r["strength"])[:10]
for r in top_rules:
    print(f"Strength: {r['strength']:3} | IF ({r['op_label']} == {r['target']}) THEN ({r['exp_label']})")
