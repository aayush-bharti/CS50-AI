import nltk
import sys
import string
import os
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
 
    #create a dictionary to keep the files contents
    files = {}
    
    #loop through the files in the directory
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        #reads the files and maps the filename to the contents
        with open(path, mode = 'r') as file:
            files[filename] = file.read()
            
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    
    #makes the words all lowercase
    document_lower = document.lower()
    #creates a list with the documents words
    words = nltk.word_tokenize(document_lower)
    new_words = []

    #loops through the list of words and adds them to the new set of words if it is not a punctuation or a stop word
    for word in words:
        if word not in string.punctuation and word not in nltk.corpus.stopwords.words("english"):
            new_words.append(word)
    
    return new_words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    
    #create a dictionary to store the word count and idf values 
    word_count = {}
    idf_values = {}
    
    #loop through the documents
    for filename in documents:
        #loops through the set of words in the file
        for word in set(documents[filename]):
            #if the word is in the idf list, add 1 to the value
            if word in word_count:
                word_count[word] += 1
            #if not, add the word to the idf list and make the value 1
            else:
                word_count[word] = 1

    #loop through the words in the idf list
    for word in word_count:
        #calculate the actual idf values from the equation by finding the number of the documents and 
        #dividing it by the number of times the word shows up in the document, and taking a natural log of that
        doc_count = len(documents)
        word_count_val = word_count[word]
        idf_values[word] = math.log(doc_count / word_count_val)
        
    return idf_values


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    
    #creates a dictionary to return
    best_files = {}
    #initialize the tf-idf values to 0
    for file in files:
        best_files[file] = 0
    
    #loops through the words in the query and the files in the dictionary
    for word in query:
        for file in files:
            #if the word is in the file, count how many times it shows up and calculate the tfidf value 
            #add that value to the dictionary
            if word in files[file]:
                tf = files[file].count(word)
                best_files[file] += tf * idfs[word]

    #sort the files based on their tf-idf values and return a list of the top filenames
    sorted_files = [file[0] for file in sorted(best_files.items(), key = lambda val: val[1], reverse = True)][:n]
    
    return sorted_files


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    
    #creates a dictionary to store the values of idf and query term density
    best_sentences = {}
    #initialize the idf and qtd values to 0
    for sentence in sentences:
        best_sentences[sentence] = {}
        best_sentences[sentence]['idf'] = 0
        best_sentences[sentence]['qtd'] = 0
    
    #loops through the words in the query and all the sentences
    for word in query:
        for sentence in sentences:
            #if the word is in the sentence, count how many times it shows up
            #calculate the length of the sentence and then use those to calculate the query term density
            if word in sentences[sentence]:
                word_count = sentences[sentence].count(word)
                sentence_length = len(sentences[sentence])
                term_density = word_count / sentence_length
                
                #add the idf and term density values to the dictionary to their labels
                best_sentences[sentence]['idf'] += idfs[word]
                best_sentences[sentence]['qtd'] += term_density
                
    #sort the sentences based on the sum of the idfs and then the query term density if the idfs are the same
    sorted_sentence = [sentence for sentence in sorted(best_sentences, key = lambda val: (best_sentences[val]['idf'], best_sentences[val]['qtd']), reverse = True)][:n]
    
    return sorted_sentence
    

if __name__ == "__main__":
    main()
