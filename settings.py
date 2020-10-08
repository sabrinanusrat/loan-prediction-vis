DATA_DIR = "data"
PROCESSED_DIR = "processed"
MINIMUM_TRACKING_QUARTERS = 4
FORECLOSURE_TARGET = "foreclosure_status"
DELINQUENCY_TARGET = "delinquency_status"
'''
NON_PREDICTORS = [
    "loan_id",
    "origination_month",
    #"origination_year",
    "first_payment_month",
    "first_payment_year",
    "insurance_percentage",
    "insurance_type",
    "relocation_mortgage",
    FORECLOSURE_TARGET,
    DELINQUENCY_TARGET,
    "performance_count",
    "channel",
    "seller",
    "original_unpaid_pricipal_balance",
    #"property_state",
    #"zip",
    #"first_time_homebuyer",
    #"loan_purpose",
    #"loan_term",
    #"property_type",
    #"unit_count",
    #"occupancy_status",
    "product_type"
    #"co_borrower_credit_score",
    #"borrower_count"
]
'''
PREDICTORS = {
    FORECLOSURE_TARGET: [
        "interest_rate",
        "loan_term",
        "loan_to_value",
        "combined_loan_to_value",
        "debt_to_income_ratio",
        "borrower_credit_score",
        "property_type",
        "occupancy_status",
        "property_state",
        "zip",
        "co_borrower_credit_score"
    ],
    DELINQUENCY_TARGET: [
        #"loan_id",
        #"channel",
        #"seller",
        #"origination_year",
        "interest_rate",
        #"original_unpaid_pricipal_balance",
        "loan_term",
        "loan_to_value",
        "combined_loan_to_value",
        #"borrower_count",
        "debt_to_income_ratio",
        "borrower_credit_score",
        #"first_time_homebuyer",
        #"loan_purpose",
        "property_type",
        #"unit_count",
        "occupancy_status",
        "property_state",
        "zip",
        #"product_type",
        "co_borrower_credit_score"
    ]
}
CATEGORICAL_COLUMNS = [
    "channel",
    "seller",
    "first_time_homebuyer",
    "loan_purpose",
    "property_type",
    "occupancy_status",
    "property_state",
    "product_type"
]
CV_FOLDS = 3