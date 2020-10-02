DATA_DIR = "data"
PROCESSED_DIR = "processed"
MINIMUM_TRACKING_QUARTERS = 4
FORECLOSURE_TARGET = "foreclosure_status"
DELINQUENCY_TARGET = "delinquency_status"
NON_PREDICTORS = [
    "loan_id",
    "channel",
    "origination_month",
    "origination_year",
    "first_payment_month",
    "first_payment_year",
    "insurance_percentage",
    "insurance_type",
    "relocation_mortgage",
    FORECLOSURE_TARGET,
    DELINQUENCY_TARGET,
    "performance_count"
]
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