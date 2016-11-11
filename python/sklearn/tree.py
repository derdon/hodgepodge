from sklearn import tree


def predict(classifier, features, labels, sample):
    clf = classifier.fit(features, labels)
    return clf.predict(sample)


def translate_labels(labels):
    mapping = {
        'apple': 0,
        'orange': 1,
    }
    return [mapping[label] for label in labels]


def main():
    features = [[140, 1], [130, 1], [150, 0], [170, 0]]
    orig_labels = ["apple", "apple", "orange", "orange"]
    labels = translate_labels(orig_labels)
    classifier = tree.DecisionTreeClassifier()
    samples = [[160, 0]]
    prediction = predict(classifier, features, labels, samples)
    return prediction

if __name__ == '__main__':
    print(main())
