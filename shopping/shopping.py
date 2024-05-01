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
    """
    evidence = []
    labels = []

    with open(filename) as file:
        lines = csv.DictReader(file)
        for line in lines:
            # Nearest Neighbour Classification Support
            for colName in ['Administrative', 'Informational', 'ProductRelated', 'OperatingSystems', 'Browser', 'Region', 'TrafficType']:
                line[colName] = int(line[colName])

            for colName in ['Administrative_Duration', 'Informational_Duration', 'ProductRelated_Duration', 'BounceRates', 'ExitRates','PageValues', 'SpecialDay']:
                line[colName] = float(line[colName])

            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            if line['Month'] in months:
                line['Month'] = months.index(line['Month'])
            else:
                raise ValueError("INVALID MONTH FROM CSV")

            if line['VisitorType'] == 'Returning_Visitor':
                line['VisitorType'] = 1
            elif line['VisitorType'] == 'New_Visitor' or line['VisitorType'] == 'Other':
                line['VisitorType'] = 0
            else:
                raise ValueError("INVALID CSV VISITORTYPE")

            if line['Weekend'] == 'TRUE':
                line['Weekend'] = 1
            elif line['Weekend'] == 'FALSE':
                line['Weekend'] = 0
            else:
                raise ValueError("INVALID CSV WEEKEND")
                
            if line['Revenue'] == 'TRUE':
                line['Revenue'] = 1
            elif line['Revenue'] == 'FALSE':
                line['Revenue'] = 0
            else:
                raise ValueError("INVALID CSV REVENUE")

            # Getting Evidence and Labels from CSV
            currEvidence = list(line.values())
            currLabel = currEvidence.pop(-1)

            # Pushing Evidence and Labels to output lists
            evidence.append(currEvidence)
            labels.append(currLabel)

    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)

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
    sensitivity = 0
    specificity = 0

    for i in range(len(labels)):
        if predictions[i] == labels[i]:
            if predictions[i] == 1:
                sensitivity += 1
            else:
                specificity += 1
    
    actualPositive = labels.count(1)
    actualNegative = labels.count(0)

    return (sensitivity/actualPositive, specificity/actualNegative)


if __name__ == "__main__":
    main()
