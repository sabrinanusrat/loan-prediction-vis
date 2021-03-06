import os
import settings
import pandas as pd

HEADERS = {
    "Acquisition": [
        "loan_id",
        "channel",
        "seller",
        "interest_rate",
        "original_unpaid_pricipal_balance",
        "loan_term",
        "origination_date",
        "first_payment_date",
        "loan_to_value",
        "combined_loan_to_value",
        "borrower_count",
        "debt_to_income_ratio",
        "borrower_credit_score",
        "first_time_homebuyer",
        "loan_purpose",
        "property_type",
        "unit_count",
        "occupancy_status",
        "property_state",
        "zip",
        "insurance_percentage",
        "product_type",
        "co_borrower_credit_score",
        "insurance_type",
        "relocation_mortgage"
    ],
    "Performance": [
        "loan_id",
        "reporting_period",
        "servicer_name",
        "interest_rate",
        "current_unpaid_principal_balance",
        "loan_age",
        "months_to_maturity",
        "adjusted_months_to_maturity",
        "maturity_date",
        "msa",
        "delinquency_status",
        "modification_flag",
        "zero_balance_code",
        "zero_balance_date",
        "last_paid_installment_date",
        "foreclosure_date",
        "disposition_date",
        "foreclosure_costs",
        "property_repair_costs",
        "recovery_costs",
        "misc_costs",
        "tax_costs",
        "sale_proceeds",
        "credit_enhancement_proceeds",
        "repurchase_proceeds",
        "other_foreclosure_proceeds",
        "non_interest_bearing_upb",
        "principal_forgiveness_upb",
        "repurchase_proceeds_flag",
        "principal_write_off_amount",
        "servicing_activity"
    ]
}

SELECT = {
    "Acquisition": [
        "loan_id",
        "channel",
        "seller",
        "interest_rate",
        "original_unpaid_pricipal_balance",
        "loan_term",
        "origination_date",
        "first_payment_date",
        "loan_to_value",
        "combined_loan_to_value",
        "borrower_count",
        "debt_to_income_ratio",
        "borrower_credit_score",
        "first_time_homebuyer",
        "loan_purpose",
        "property_type",
        "unit_count",
        "occupancy_status",
        "property_state",
        "zip",
        "insurance_percentage",
        "product_type",
        "co_borrower_credit_score"
    ],
    "Performance": [
        "loan_id",
        "delinquency_status",
        "foreclosure_date"
    ]
}

def concatenate(prefix="Acquisition"):
    files = os.listdir(settings.DATA_DIR)
    full = []
    for f in files:
        if not f.startswith(prefix):
            continue

        data = pd.read_csv(os.path.join(settings.DATA_DIR, f), sep="|", header=None, names=HEADERS[prefix], index_col=False, dtype='unicode')
        data = data[SELECT[prefix]]
        full.append(data)

    full = pd.concat(full, axis=0)

    full.to_csv(os.path.join(settings.PROCESSED_DIR, "{}.txt".format(prefix)), sep="|", header=SELECT[prefix], index=False)

if __name__ == "__main__":
    concatenate("Acquisition")
    concatenate("Performance")
