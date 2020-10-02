import os
import settings
import pandas as pd
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn import metrics

def read():
    train = pd.read_csv(os.path.join(settings.PROCESSED_DIR, "train.csv"))
    return train

def cross_validate(model, train, target, scaler):
    predictors = train.columns.tolist()
    predictors = [p for p in predictors if p not in settings.NON_PREDICTORS]
    X = scaler.fit_transform(train[predictors])
    y = train[target]
    predictions = model_selection.cross_val_predict(model, X, y, cv=settings.CV_FOLDS)
    # model.fit(X, y)
    return predictions

def train_model(model, train, target, scaler):
    predictors = train.columns.tolist()
    predictors = [p for p in predictors if p not in settings.NON_PREDICTORS]
    X_train, X_test, y_train, y_test = model_selection.train_test_split(train[predictors], train[target], test_size = 0.25, random_state = 0)
    X_train = scaler.fit_transform(X_train)
    model.fit(X_train, y_train)
    return X_test, y_test

def train_and_test_model(model, train, target, scaler):
    X_test, y_test = train_model(model, train, target, scaler)
    X_test = scaler.transform(X_test)
    y_pred = model.predict(X_test)
    return y_test, y_pred

def predict_single_data(model, scaler, borrower_credit_score, debt_to_income_ratio,
    lender, interest_rate, loan_amount, state, zip_code, loan_term=360,
    loan_to_value=80, combined_loan_to_value=80, borrower_count=1,
    first_time_homebuyer=0, loan_purpose=0, property_type=0, unit_count=1,
    occupancy_status=0, product_type=0, co_borrower_credit_score=0):
    X = [[
        lender, interest_rate, loan_amount, loan_term, loan_to_value, combined_loan_to_value,
        borrower_count, debt_to_income_ratio, borrower_credit_score, first_time_homebuyer,
        loan_purpose, property_type, unit_count, occupancy_status, state, zip_code,
        product_type, co_borrower_credit_score
    ]]
    X = scaler.transform(X)
    return model.predict_proba(X)[0][model.classes_.tolist().index(True)]

def compute_metrics_accuracy(target, predictions):
    return metrics.accuracy_score(target, predictions)

def compute_accuracy(target, predictions):
    df = pd.DataFrame({"target": target, "predictions": predictions})
    accurate_positive_data = df[(df["target"] == True) & (df["predictions"] == True)]
    accurate_negative_data = df[(df["target"] == False) & (df["predictions"] == False)]
    return 1.0 * (accurate_positive_data.shape[0] + accurate_negative_data.shape[0]) / df.shape[0]

def compute_false_negatives(target, predictions):
    df = pd.DataFrame({"target": target, "predictions": predictions})
    return 1.0 * df[(df["target"] == True) & (df["predictions"] == False)].shape[0] / df[(df["target"] == True)].shape[0]

def compute_false_positives(target, predictions):
    df = pd.DataFrame({"target": target, "predictions": predictions})
    return 1.0 * df[(df["target"] == False) & (df["predictions"] == True)].shape[0] / df[(df["target"] == False)].shape[0]

def compute_precision(target, predictions, positive):
    df = pd.DataFrame({"target": target, "predictions": predictions})
    return 1.0 * df[(df["target"] == positive) & (df["predictions"] == positive)].shape[0] / df[(df["predictions"] == positive)].shape[0]

def compute_recall(target, predictions, positive):
    df = pd.DataFrame({"target": target, "predictions": predictions})
    return 1.0 * df[(df["target"] == positive) & (df["predictions"] == positive)].shape[0] / df[(df["target"] == positive)].shape[0]

def count_and_print_performance_tabs(target, predictions, positive_phrase, negative_phrase):
    df = pd.DataFrame({"target": target, "predictions": predictions})
    tdtp = df[(df["target"] == True) & (df["predictions"] == True)].shape[0]
    tdfp = df[(df["target"] == True) & (df["predictions"] == False)].shape[0]
    fdtp = df[(df["target"] == False) & (df["predictions"] == True)].shape[0]
    fdfp = df[(df["target"] == False) & (df["predictions"] == False)].shape[0]
    print("# {}-data-{}-prediction = {}".format(positive_phrase, positive_phrase, tdtp))
    print("# {}-data-{}-prediction = {}".format(positive_phrase, negative_phrase, tdfp))
    print("# {}-data-{}-prediction = {}".format(negative_phrase, positive_phrase, fdtp))
    print("# {}-data-{}-prediction = {}".format(negative_phrase, negative_phrase, fdfp))

def compute_and_print_accuracy(target, predictions, target_name, positive_phrase, negative_phrase):
    print("Computing accuracy of the linear regression model for {}".format(target_name))
    print("Accuracy Score from sklearn.metrics: {}".format(compute_metrics_accuracy(target, predictions)))
    print("Accuracy Score: {}".format(compute_accuracy(target, predictions)))
    print("False Positives (error rate on {} data): {}".format(negative_phrase, compute_false_positives(target, predictions)))
    print("False Negatives (error rate on {} data): {}".format(positive_phrase, compute_false_negatives(target, predictions)))
    print("{} Precision: {}".format(positive_phrase, compute_precision(target, predictions, True)))
    print("{} Precision: {}".format(negative_phrase, compute_precision(target, predictions, False)))
    print("{} Recall: {}".format(positive_phrase, compute_recall(target, predictions, True)))
    print("{} Recall: {}".format(negative_phrase, compute_recall(target, predictions, False)))
    count_and_print_performance_tabs(target, predictions, positive_phrase, negative_phrase)

if __name__ == "__main__":
    train = read()

    foreclosure_scaler = StandardScaler()
    foreclosure_model = LogisticRegression(random_state=0, class_weight="balanced")
    # foreclosure_predictions = cross_validate(foreclosure_model, train, settings.FORECLOSURE_TARGET, foreclosure_scaler)
    # compute_and_print_accuracy(train[settings.FORECLOSURE_TARGET], foreclosure_predictions, settings.FORECLOSURE_TARGET, "foreclosure", "non-foreclosure")
    foreclosure_data, foreclosure_predictions = train_and_test_model(foreclosure_model, train, settings.FORECLOSURE_TARGET, foreclosure_scaler)
    compute_and_print_accuracy(foreclosure_data, foreclosure_predictions, settings.FORECLOSURE_TARGET, "foreclosure", "non-foreclosure")

    delinquency_scaler = StandardScaler()
    delinquency_model = LogisticRegression(random_state=0, class_weight="balanced")
    # delinquency_predictions = cross_validate(delinquency_model, train, settings.DELINQUENCY_TARGET, delinquency_scaler)
    # compute_and_print_accuracy(train[settings.DELINQUENCY_TARGET], delinquency_predictions, settings.DELINQUENCY_TARGET, "delinquency", "non-delinquency")
    delinquency_data, delinquency_predictions = train_and_test_model(delinquency_model, train, settings.DELINQUENCY_TARGET, delinquency_scaler)
    compute_and_print_accuracy(delinquency_data, delinquency_predictions, settings.DELINQUENCY_TARGET, "delinquency", "non-delinquency")

