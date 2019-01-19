def softmax(distribution):
    """ used to restore probability constraint of summing to 1 when elements are removed """

    summation = sum(distribution)
    return [float(x / summation) for x in distribution]