from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # Implying that A is a Knight or Knave but not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),

    # The Sentence
    Or(And(AKnight, AKnave), Not(And(AKnight, AKnave))),

    # Implying that if A is a Knight, his sentence is true
    Implication(AKnight, And(AKnight, AKnave)),
    # Implying that if A is a Knave, his sentence is false
    Implication(AKnave, Not(And(AKnight, AKnave))),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Implying that A is a Knight or Knave but not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    # Implying that B is a Knight or Knave but not both
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),

    # The Sentence
    Or(And(AKnave, BKnave),
        Not(And(AKnave, BKnave))),

    # Implying that if A is a Knight, his sentence is true
    Implication(AKnight, And(AKnave, BKnave)),
    # Implying that if A is a Knave, his sentence is false
    Implication(AKnave, Not(And(AKnave, BKnave))),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # Implying that A is a Knight or Knave but not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    # Implying that B is a Knight or Knave but not both
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),

    # The Sentences
    # A
    Or(Or(And(AKnave, BKnave), And(AKnight, BKnight)),
        Not(Or(And(AKnave, BKnave), And(AKnight, BKnight)))),
    # B
    Or(Or(And(AKnave, BKnight), And(AKnight, BKnave)),
        Not(Or(And(AKnave, BKnight), And(AKnight, BKnave)))),

    # Implying that if A is a Knight, his sentence is true
    Implication(AKnight, Or(And(AKnave, BKnave), And(AKnight, BKnight))),
    # Implying that if A is a Knave, his sentence is false
    Implication(AKnave, Not(Or(And(AKnave, BKnave), And(AKnight, BKnight)))),

    # Implying that if B is a Knight, his sentence is true
    Implication(BKnight, Or(And(AKnave, BKnight), And(AKnight, BKnave))),
    # Implying that if B is a Knave, his sentence is false
    Implication(BKnave, Not(Or(And(AKnave, BKnight), And(AKnight, BKnave)))),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # Implying that A is a Knight or Knave but not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    # Implying that B is a Knight or Knave but not both
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    # Implying that C is a Knight or Knave but not both
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),

    # The sentences
    # A
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),

    # B (first sentence)
    # If B is a Knight, A said "I am a Knave"
    Implication(BKnight, 
        And(
            # If A is a Knight, he said the Truth, which means he is a Knave, which isn't possible
            Implication(AKnight, AKnave),
            # If A is a Knave, he told a lie
            Implication(AKnave, AKnight)
        )
    ),
    # If B is a Knave, A said "I am a Knight"
    Implication(BKnave,
        And(
            # If A is a Knight, he said the Truth
            Implication(AKnight, AKnight),
            # If A is a Knave, he told a lie
            Implication(AKnave, Not(AKnight))
        )
    ),

    # B (second sentence)
    # If B is a Knight, C is a Knave
    Implication(BKnight, CKnave),
    # If B is a Knave, C is not a Knave
    Implication(BKnave, Not(CKnave)),

    # C
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight))

)

# Problem Structure
for c in ['A', 'B', 'C']:
    # Implying that if a Character is a certain role, it is not the other
    knowledge0.add(Implication(Symbol(f"{c}Knight"), Not(Symbol(f"{c}Knave"))))
    knowledge0.add(Implication(Symbol(f"{c}Knave"), Not(Symbol(f"{c}Knight"))))
    knowledge1.add(Implication(Symbol(f"{c}Knight"), Not(Symbol(f"{c}Knave"))))
    knowledge1.add(Implication(Symbol(f"{c}Knave"), Not(Symbol(f"{c}Knight"))))
    knowledge2.add(Implication(Symbol(f"{c}Knight"), Not(Symbol(f"{c}Knave"))))
    knowledge2.add(Implication(Symbol(f"{c}Knave"), Not(Symbol(f"{c}Knight"))))
    knowledge3.add(Implication(Symbol(f"{c}Knight"), Not(Symbol(f"{c}Knave"))))
    knowledge3.add(Implication(Symbol(f"{c}Knave"), Not(Symbol(f"{c}Knight"))))


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
