import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""


NONTERMINALS = """
S -> NP VP | S Conj S | S Conj VP
NP -> N | Det N | AP N | NP PP | Conj NP
VP -> V | VP Adv | V NP | V PP | Adv VP
AP -> Adj | Adj AP | Det AP
PP -> P NP | PP NP | PP PP
"""
#S = Sentence
#NP = Noun Phrase
#VP = Verb Phrase
#AP = Adjective Phrase
#PP = Prepositional Phrase



grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    
    #make all the words in the sentence lower case
    lower_sentence = sentence.lower()
    #use the tokenize function to split the words into a list
    words = nltk.word_tokenize(lower_sentence)
    new_words = []
    
    #loop through all the words in the list
    for word in words:
        #loop through the letters in the word
        for letter in word:
            #if there is a letter in the word from the alphabet, add the word to the new list
            if letter.isalpha():
                new_words.append(word)
                break
    
    return new_words
    
    
def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    
    #variable to return the list of noun phrase chunks
    np_list = []
    
    #loop through the subtrees of a parented tree
    for subtrees in nltk.ParentedTree.convert(tree).subtrees():
        #if the subtree is a 'N'/noun, add the parent of that subtree to the list since it must be a noun phrase
        if subtrees.label() == 'N':
            parent = subtrees.parent()
            np_list.append(parent)
    
    return np_list



if __name__ == "__main__":
    main()
