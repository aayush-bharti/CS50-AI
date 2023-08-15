import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    
    #variables for the evidence list and the labels list
    evidence = []
    labels = []
    #dictionary for the months that are in the dataset and giving them values
    month = {'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'June': 5, 'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11}
    
    #opens the file
    with open(filename, mode = 'r') as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=',')
        #adds in all the values for the columns in the dataset into the evidence list except the last column
        for row in spamreader:
            evidence.append([
                int(row['Administrative']),
                float(row['Administrative_Duration']),
                int(row['Informational']),
                float(row['Informational_Duration']),
                int(row['ProductRelated']),
                float(row["ProductRelated_Duration"]),
                float(row['BounceRates']),
                float(row['ExitRates']),
                float(row['PageValues']),
                float(row['SpecialDay']),
                month[row['Month']],
                int(row['OperatingSystems']),
                int(row['Browser']),
                int(row['Region']),
                int(row['TrafficType']),
                1 if row['VisitorType'] == "Returning_Visitor" else 0,
                1 if row['Weekend'] == "TRUE" else 0
            ])
            
            #adds the last column into the labels list
            labels.append(1 if row['Revenue'] == "TRUE" else 0)
    
    #returns a tuple of evidence and labels
    return evidence, labels
    
    

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    
    #makes k = 1
    k = 1
    #uses the kNeighborsClassifier and then fits the the data and returns it
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    
    #creates the sensitivity and specificity variables
    sensitivity = 0
    specificity = 0
    
    #variables to keep track of all the positive and negative rates
    positives_total = 0
    negatives_total = 0
    #variables to keep track of all of the correct positive and negative rates
    positives_correct = 0
    negatives_correct = 0
    
    #loops through the lists given
    for actual, predicted in zip(labels, predictions):
        #if the actual label is 1, then it is a positive label
        #increment the total positive variable
        if actual == 1:
            positives_total += 1
            #increment the correct positive variable if predicted correctly
            if actual == predicted:
                positives_correct += 1
        
        #if the actual label is 0, then it is a negative label
        #increment the total negative variable     
        elif actual == 0:
            negatives_total += 1
            #increment the correct negative variable if predicted correctly
            if actual == predicted:
                negatives_correct += 1
            

    #calculate the decimal value based off the correct and total values
    sensitivity = positives_correct/positives_total
    specificity = negatives_correct/negatives_total
    
    #returns them as a tuple
    return sensitivity, specificity
    
    

if __name__ == "__main__":
    main()
