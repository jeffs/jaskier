import random

Forms = {
    "One-part": ["A"],
    "Binary":   ["A", "B"],
    "Ternary":  ["A", "B", "A"],
    "Arch":     ["A", "B", "C", "B", "A"],
    "Sonata":   ["A", "B", "A"],
    "Ballade1": ["A", "B", "C", "D", "C", "D", "E", "F", "A", "B"],
    "Ballade2": ["A", "B", "C", "D", "C", "D", "E", "A", "B", "A", "B"],
    "Ballade3": ["A", "B", "A", "B", "C", "D", "E"],
    "Rondo":    ["A", "B", "A", "C", "A", "D", "A", "E", "A", "F"],
    "Verse-chorus": ["Intro", "A", "B", "A", "C", "B", "C", "B"],
}

def pick_random_form():
    name = random.choice(list(Forms))
    return (name, Forms[name])