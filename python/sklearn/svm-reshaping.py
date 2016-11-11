from sklearn import svm
import numpy as np


def train(samples, labels):
    clf = svm.SVC()
    clf.fit(samples, labels)
    return clf


def predict(classifier, input_):
    return classifier.predict(input_)


if __name__ == '__main__':
    # 5x5
    board = [
        [-1, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, -1, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 0, -1, 0, 0],
    ]
    # make sure board size is as expected
    assert len(board) == 5
    for row in board:
        assert len(row) == 5
    # samples are list of game states
    samples = np.array([board, board])  # possibly more features
    labels = ["foo", "bar"]

    # reshape samples so that it's not 3D anymore but 2D instead
    d2_samples = samples.reshape((len(samples), 5*5))

    clf = train(d2_samples, labels)

    input_ = [
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, -1, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 0, -1, 0, 0],
    ]
    d2_input = np.array(input_).reshape((1, 5*5))

    prediction = predict(clf, d2_input)
    print(prediction)
