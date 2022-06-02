import os
import os.path
import pandas as pd
from parso import parse


def split_by_variants():
    df = pd.read_csv("./data/conform_SLA.csv")
    df = df.reset_index()

    flows = []
    flow = []
    # First for loop, splitting rows by case_id
    case_id = df['case_id'][0]
    for ind in df.index:
        if case_id != df['case_id'][ind]:
            case_id = df['case_id'][ind]

            flows.append(flow)
            print(flow)
            flow = [' Register Claim']
        else:
            flow.append(df['Activity'][ind])
        # if df['Activity'][ind] == "Register Claim":

        #     print(df['case_id'][ind])
    print(flows)
    # return df


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


split_by_variants()
# print(parse_dataset())
