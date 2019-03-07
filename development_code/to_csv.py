from saver import Saver
import utils

def average_experiment_dict(experiment_dict):
    max_chunks = 250
    for i in range(10):
        if len(experiment_dict[i]) > 0:
            experiment_dict[i] = utils.average_chunks(experiment_dict[i], max_chunks)

    return experiment_dict

saver = Saver("data/")

final = saver.load_python_obj("Final result")
percentages1 = average_experiment_dict(saver.load_python_obj("experiment1"))
percentages2 = average_experiment_dict(saver.load_python_obj("experiment2"))
percentages3 = average_experiment_dict(saver.load_python_obj("experiment3"))
percentages4 = average_experiment_dict(saver.load_python_obj("experiment4"))

result = {"pbm" : {"probabilistic_interleaving" : percentages1, "team_draft" : percentages3}, "random" : {"probabilistic_interleaving" : percentages2, "team_draft" : percentages4}}

output_file_1 = open("data/impressions.csv", "w")

for click_model in final:
    for interleaving in final[click_model]:

        output_file_1.write("{},-,{},\n".format(click_model, interleaving))
        output_file_1.write("\n")
        output_file_1.write("bin,max,min,median,stdev,mean,whole_list,\n")

        for bin in final[click_model][interleaving]:

            listbuilder = ""
            for element in final[click_model][interleaving][bin]["list"]:
                listbuilder = listbuilder + str(element) + ","

            max = final[click_model][interleaving][bin]["max"]
            min = final[click_model][interleaving][bin]["min"]
            median = final[click_model][interleaving][bin]["median"]
            mean = final[click_model][interleaving][bin]["mean"]
            stdev = final[click_model][interleaving][bin]["std"]

            bin_output = "{},{},{},{},{},{},{},\n".format(bin, max, min, median, stdev, mean, listbuilder)
            output_file_1.write(bin_output)

        output_file_1.write("\n")
        output_file_1.write("\n")


output_file_1.close()


output_file_2 = open("data/wins.csv", "w")

for click_model in result:
    for interleaving in result[click_model]:

        output_file_2.write("{},-,{},\n".format(click_model, interleaving))
        output_file_2.write("\n")
        output_file_2.write("bin,whole_list,\n")

        for bin in result[click_model][interleaving]:

            listbuilder = ""
            for element in result[click_model][interleaving][bin]:
                listbuilder = listbuilder + str(element) + ","

            bin_output = "{},{},\n".format(bin, listbuilder)

            output_file_2.write(bin_output)

        output_file_2.write("\n")
        output_file_2.write("\n")


output_file_2.close()
