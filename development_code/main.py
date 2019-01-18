import numpy as np
from saver import Saver
from rankings_step import RankingsStep
from err_step import ERRStep
from interleavings_step import InterleavingsStep
from user_clicks_simulation_step import UserClicksSimulationStep
from interleavings_simulation_step import InterleavingSimulationStep
from sample_size_step import SampleSizeStep

save_and_load = Saver("data/")

## Step 0 : Loading data

data = save_and_load.load_data_model_1()

steps = [
    RankingsStep(1, "Simulate Rankings of Relevance for E and P", data),
    ERRStep(2, "Calculate the 𝛥measure", data),
    InterleavingsStep(3, "Implement Team-Draft Interleaving and Probabilistic Interleaving ", data),
    UserClicksSimulationStep(4, "Simulate User Clicks", data),
    InterleavingSimulationStep(5, "Simulate Interleaving Experiment", data),
    SampleSizeStep(6, "Compute Sample Size", data),
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
