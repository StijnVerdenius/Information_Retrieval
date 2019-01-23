from functools import lru_cache
import numpy as np
import math

def softmax(distribution):
    """ used to restore probability constraint of summing to 1 when elements are removed """

    summation = sum(distribution)
    return [float(x / summation) for x in distribution]

@lru_cache(maxsize=3200)
def difference_to_err_table_position(difference: float) -> int:
    # if difference < 0.05 or 
    if difference > 0.95:
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

def initialize_err_table():
    err_table = {
        0: [],
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
        7: [],
        8: [],
        9: []
    }

    return err_table

def split_to_chunks(list_to_split, chunks_size):
    """Yield successive n-sized chunks from l."""
    chunks = []
    for i in range(0, len(list_to_split), chunks_size):
        chunks.append(list_to_split[i:i + chunks_size])
    
    return chunks

def average_chunks(list_to_split, max_chunks):
    chunks_size = math.ceil(len(list_to_split) / max_chunks)
    chunks = split_to_chunks(list_to_split, chunks_size)

    result = []
    for chunk in chunks:
        chunk_average = np.average(chunk)
        result.append(chunk_average)

    return result
