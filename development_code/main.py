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

rankings_pairs, counter = do_next_step(None, counter)

## Step 2: Calculate the 𝛥measure

err_table, counter = do_next_step(rankings_pairs, counter)

## Step 3: Implement Team-Draft Interleaving (5pts) and Probabilistic Interleaving (35 points)

interleaving_dictionary, counter = do_next_step(err_table, counter)

## Step 4: Simulate User Clicks (40 points)

click_models, counter = do_next_step([3], counter)

## Step 5: Simulate Interleaving Experiment

resulting_dictionary, counter = do_next_step([interleaving_dictionary, {"probabilistic": click_models[0], "random": click_models[1]}], counter)

## Step 6: Compute Sample Size

filled_in_table, counter = do_next_step(resulting_dictionary, counter)

print("#######\n\n\nFINAL RESULT\n\n\n{}".format(filled_in_table))

# Step 7: Analysis (20 points) (notebook only)
