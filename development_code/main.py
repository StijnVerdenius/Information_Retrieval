

import numpy as np
from saver import Saver
from step1 import Step1
from step2 import Step2
from step3 import Step3
from step4 import Step4
from step5 import Step5
from step6 import Step6


save_and_load = Saver("data/")



## Step 0 : Loading data


data = save_and_load.load_data_model_1()

steps = [
Step1(1, "Simulate Rankings of Relevance for E and P", data),
Step2(2, "Calculate the 𝛥measure", data),
Step3(3, "Implement Team-Draft Interleaving and Probabilistic Interleaving ", data),
Step4(4, "Simulate User Clicks", data),
Step5(5, "Simulate Interleaving Experiment", data),
Step6(6, "Compute Sample Size", data),
]

counter = 0

def do_next_step(input_list, counter):
    step_output = steps[counter].do_step(input_list)
    counter += 1
    return step_output, counter

## Step 1: Simulate Rankings of Relevance for E and P


some_output, counter = do_next_step(["some input", "other input"], counter)


## Step 2: Calculate the 𝛥measure



some_output, counter = do_next_step(["some input", "other input"], counter)


## Step 3: Implement Team-Draft Interleaving (5pts) and Probabilistic Interleaving (35 points)


some_output, counter = do_next_step(["some input", "other input"], counter)

## Step 4: Simulate User Clicks (40 points)


some_output, counter = do_next_step(["some input", "other input"], counter)

## Step 5: Simulate Interleaving Experiment


some_output, counter = do_next_step(["some input", "other input"], counter)

## Step 6: Compute Sample Size


some_output, counter = do_next_step(["some input", "other input"], counter)

# Step 7: Analysis (20 points) (notebook only)
