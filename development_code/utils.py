def softmax(distribution):
    """ used to restore probability constraint of summing to 1 when elements are removed """

    summation = sum(distribution)
    return [float(x / summation) for x in distribution]

def difference_to_err_table_position(difference: int) -> int:
    if difference < 0.05 or difference > 0.95:
        raise Exception("Invalid difference")
    elif difference < 0.1:
        return 0
    elif difference < 0.2:
        return 1
    elif difference < 0.3:
        return 2
    elif difference < 0.4:
        return 3
    elif difference < 0.5:
        return 4
    elif difference < 0.6:
        return 5
    elif difference < 0.7:
        return 6
    elif difference < 0.8:
        return 7
    elif difference < 0.9:
        return 8
    else:
        return 9
