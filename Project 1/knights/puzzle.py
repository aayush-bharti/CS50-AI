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
    # TODO
    
    #A can be a knight or a knave but cannot be both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))), 
    
    #if A is a knight, it is both a knight and a knave
    Implication(AKnight, And(AKnight, AKnave)),
    
    #if A is a knave, it is not both a knight and a knave
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO
    
    #A can be a knight or a knave but cannot be both 
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),

    #B can be a knight or a knave but cannot be both
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    
    #if A is a knight, they're both knaves
    Implication(AKnight, And(AKnave, BKnave)),
    
    #if A is a knave, they're not both knights
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # TODO
    
    #A can be a knight or a knave but cannot be both 
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),

    #B can be a knight or a knave but cannot be both 
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    
    #if A is a knight, they are both the same kind/knights
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    
    #if A is a knave, they are not the same kind/A is a knave, B is a knight
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    
    #if B is a knight, they are different kinds/B is a knight, A is a knave
    Implication(BKnight, Or(And(AKnave, BKnight), And(AKnight, BKnave))),
    
    #if B is a knave, they are not different kinds/B is a knave, A is a knave 
    Implication(BKnave, Not(Or(And(AKnave, BKnight), And(AKnight, BKnave))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # TODO
    #if b is a knight, a said its a knave, c is a knave, a is a knave
    #if b is a knave, a said its a knight, c is a knight, a is a knight
    #if c is a knight, a is a knight, b is a knave, a said its a knight
    #if c is a knave, a is a knave, b is a knight, a said its a knave
    
    
    #A can be a knight or a knave but cannot be both 
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),

    #B can be a knight or a knave but cannot be both 
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    
    #C can be a knight or a knave but cannot be both 
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),

    #if A is a knight, it can be either a knight or a knave
    Implication(AKnight, Or(AKnight, AKnave)),
    
    #if A is a knave, it cannot be a knight or a knave
    Implication(AKnave, Not(Or(AKnight, AKnave))),
    
    #if B is a knight, then A says it is a knave, then if A is a knight, it is a knave, or if A is a knave, it is not a knave
    Implication(BKnight, Or(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)))),
    
    #if B is a knight, then C is a knave
    Implication(BKnight, CKnave),
    
    #if B is a knave, then A says it is a knight, then if A is a knight, it is a knight, or if A is a knave, it is not a knight
    Implication(BKnave, Or(Implication(AKnight, AKnight), Implication(AKnave, Not(AKnight)))),
    
    #if B is a knave, then C is not a knave/is a knight
    Implication(BKnave, Not(CKnave)),
    
    #if C is a knight, then A is a knight
    Implication(CKnight, AKnight), 
    
    #if C is a knave, then A is not a knight/is a knave
    Implication(CKnave, Not(AKnight))
)


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
