import os
import os.path
import pandas as pd
from parso import parse


"""
For a lack of better option now, until dataset can be split into its variants in a more efficient way
Split dataset into different variants with Apromore. Afterwards use the following syntax:

-> case_variant_#.csv

each dataset will then be loaded and its case_variant will be added accordingly (the same # as you give the filename)


"""


def parse_dataset(relative_dir="data/variant_files/"):
    for filename in os.listdir(relative_dir):
        if os.path.isfile(os.path.join(relative_dir, filename)):
            df = pd.read_csv(r"./data/variant_files/%s" % (filename))
            variant_id = filename.split("_")[2].split(".")[0]
            df["case_variant"] = variant_id

        return df


print(parse_dataset())
