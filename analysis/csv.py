from os import path
import set_of_parliament_members as sopm

def launch_analysis(data_file):
    # directory = path.dirname(path.dirname(__file__))
    # path_to_file = path.join(directory, "data", data_file)

    # with open(path_to_file, "r") as f:
    #     preview = f.readline()

    # print("Yeah! We managed to read the file. Here is a preview: {}".format(preview))
    sopm.launch_analysis(data_file)


if __name__ == "__main__":
    launch_analysis("current_mps.csv")
