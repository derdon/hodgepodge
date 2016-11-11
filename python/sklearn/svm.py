from sklearn import svm


def train(samples, features, labels):
    X = [samples, features]
    y = labels
    clf = svm.SVC()
    clf.fit(X, y)
    return clf


def predict(classifier, input_):
    return classifier.predict(input_)


def main(samples, features, labels, input_):
    clf = train(samples, features, labels)
    prediction = predict(clf, input_)
    return prediction


if __name__ == '__main__':
    samples = [0, 0]
    features = [1, 1]
    labels = [0, 1]
    input_ = [[2., 2.]]
    print(main(samples, features, labels, input_))
