import os
import settings
import categoricals
import pandas as pd
import numpy

def read_acquisition():
    acquisition = pd.read_csv(os.path.join(settings.PROCESSED_DIR, "Acquisition.txt"), sep="|")
    return acquisition

def get_performance_summary():
    performance = {}
    with open(os.path.join(settings.PROCESSED_DIR, "Performance.txt"), 'r') as f:
        for i, line in enumerate(f):
            if i == 0:
                # Skip header row
                continue
            loan_id, delinquency_status, forclosure_date = line.split("|")
            loan_id = int(loan_id)
            if loan_id not in performance:
                performance[loan_id] = {
                    "foreclosure_status": False,
                    "delinquency_status": False,
                    "performance_count": 0
                }
            performance[loan_id]["performance_count"] += 1
            if delinquency_status != "X" and delinquency_status != "0":
                performance[loan_id]["delinquency_status"] = True
            if len(forclosure_date.strip()) > 0:
                performance[loan_id]["foreclosure_status"] = True
    return performance

def get_performance_summary_value(loan_id, key, performance_summary):
    value = performance_summary.get(loan_id, {
        "foreclosure_status": False,
        "delinquency_status": False,
        "performance_count": 0
    })
    return value[key]

def annotate(acquisition, performance_summary):
    acquisition["delinquency_status"] = acquisition["loan_id"].apply(lambda x: get_performance_summary_value(x, "delinquency_status", performance_summary))
    acquisition["foreclosure_status"] = acquisition["loan_id"].apply(lambda x: get_performance_summary_value(x, "foreclosure_status", performance_summary))
    acquisition["performance_count"] = acquisition["loan_id"].apply(lambda x: get_performance_summary_value(x, "performance_count", performance_summary))
    for column in settings.CATEGORICAL_COLUMNS:
        additional_values = filter(lambda x: x not in categoricals.CATEGORICAL_ARRAYS[column], get_unique_values(acquisition, column))
        categoricals.CATEGORICAL_ARRAYS[column].extend(additional_values)
        categoricals.CATEGORICAL_INDEX_MAP[column] = categoricals.array_to_index_map(categoricals.CATEGORICAL_ARRAYS[column])
        #acquisition[column] = acquisition[column].astype('category').cat.codes
        acquisition[column] = pd.Series(map(lambda x:categoricals.CATEGORICAL_INDEX_MAP[column][x], acquisition[column]))

    for start in ["first_payment", "origination"]:
        column = "{}_date".format(start)
        acquisition["{}_year".format(start)] = pd.to_numeric(acquisition[column].str.split('/').str.get(1))
        acquisition["{}_month".format(start)] = pd.to_numeric(acquisition[column].str.split('/').str.get(0))
        del acquisition[column]

    acquisition = acquisition.fillna(-1)
    acquisition = acquisition[acquisition["performance_count"] > settings.MINIMUM_TRACKING_QUARTERS]
    return acquisition

def write(acquisition):
    acquisition.to_csv(os.path.join(settings.PROCESSED_DIR, "train.csv"), index=False)

def get_unique_values(acquisition, column):
    return numpy.unique(acquisition[column])

if __name__ == "__main__":
    acquisition = read_acquisition()
    performance_summary = get_performance_summary()
    acquisition = annotate(acquisition, performance_summary)
    write(acquisition)