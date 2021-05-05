import pandas as pd
import numpy as np

INPUT_DATA_DIR = "./input/"
OUTPUT_DATA_DIR = "./output/"

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 50)

def get_values_from_list_a_minus_b(a, b):
    return np.setdiff1d(a,b)

#read
col_list = [
        "id",
        "userId",
        "activity_id",
        "response",
        "item",
        "flag",
        "question",
        "activity_end_time",
    ]
df = pd.read_csv(INPUT_DATA_DIR + "teacher1.csv", usecols=col_list)
categories_df = pd.read_csv(INPUT_DATA_DIR + "categories.csv")

#get domain cateogories
categories_df["question"] = categories_df["Domain"]
categories_df["question"] = categories_df["question"].str.lower()
df["question"] = df["question"].str.lower()
df = pd.merge(df, categories_df, on="question", how="left")

#parse response values
df["response_value"] = df["response"].str.split(": ").str[1]
df["response_value"] = pd.to_numeric(df["response_value"], errors="coerce")

#pivot by student
df["learner_id"] = df.loc[df["question"] == "learner id"]["response"]
df = df.sort_values(by=["id","learner_id"])
df["learner_id"] = df["learner_id"].ffill()
print(df.head(50))
pivoted = pd.pivot_table(df, index=["learner_id","activity_end_time"], values=["response_value"], columns=["Category","question"])
print(pivoted.head(50))
pivoted.to_csv(OUTPUT_DATA_DIR + 'teacher1_output.csv')

# #rename columns
# df["Question"] = df["question"]
# df["Response"] = df["response_value"]
# df["Student ID"] = df["learner_id"]

# #remove student id and comment lines
# df = df[df["question"] != "Learner ID"]
# df = df[df["question"] != "Comment"]

# #export
# header = ["Question", "Response", "Student ID"]
# df.to_csv(OUTPUT_DATA_DIR + 'teacher1_output.csv', columns = header, index=False)