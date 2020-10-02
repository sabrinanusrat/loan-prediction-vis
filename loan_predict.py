from flask import Flask, render_template, request
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from prediction_model import read, train_model, predict_single_data
from categoricals import CATEGORICAL_INDEX_MAP
from selections import ALL_SELECTION_OTIONS
import settings

foreclosure_scaler = StandardScaler()
foreclosure_model = LogisticRegression(random_state=0, class_weight="balanced")
delinquency_scaler = StandardScaler()
delinquency_model = LogisticRegression(random_state=0, class_weight="balanced")

app = Flask(__name__)
#cols = ['age', 'sex', 'bmi', 'children', 'smoker', 'region']

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict',methods=['GET','POST'])
def predict():
    #int_features = [x for x in request.form.values()]
    #final = np.array(int_features)
    #data_unseen = pd.DataFrame([final], columns = cols)
    #prediction = predict_model(model, data=data_unseen, round = 0)
    #prediction = int(prediction.Label[0])
    #prediction =10
    
    if 'annual_income' not in request.form:
        return render_template('predict_page.html', pred='', options=ALL_SELECTION_OTIONS)
    
    lender = get_categorical_value('lender', 'seller')
    interest_rate = float(request.form['interest_rate'])
    property_value = int(request.form['val'])
    down_payment = int(request.form['down_payment'])
    loan_amount = (property_value * (100-down_payment))/100
    loan_term = int(request.form['loan_term'])*12 if 'loan_term' in request.form else 360
    loan_to_value = 100 - down_payment
    combined_loan_to_value = loan_to_value
    borrower_count = 2 if len(request.form['co_borrower_credit_score'])>0 and int(request.form['co_borrower_credit_score'])>0 else 1
    income = int(request.form['annual_income'])
    monthly_interest = interest_rate / 12.0
    monthly_payment = 1.0 * loan_amount * (monthly_interest * (1.0 + monthly_interest) ** loan_term) / ((1.0 + monthly_interest) ** loan_term - 1.0)
    debt_to_income_ratio = int(1.0 * monthly_payment / (income / 12.0))
    borrower_credit_score = int(request.form['borrower_credit_score'])
    first_time_homebuyer = get_categorical_value('first_time_homebuyer', 'first_time_homebuyer')
    loan_purpose = get_categorical_value('loan_purpose', 'loan_purpose')
    property_type = get_categorical_value('property_type', 'property_type')
    unit_count = int(request.form['unit_count']) if len(request.form['unit_count'])>0 else 1
    occupancy_status = get_categorical_value('occupancy_status', 'occupancy_status')
    state = get_categorical_value('property_state', 'property_state')
    zip_code = int(request.form["zip"])/100
    product_type = 0
    co_borrower_credit_score = int(request.form['co_borrower_credit_score']) if len(request.form['co_borrower_credit_score'])>0 else 0

    foreclosure_probability = predict_single_data(foreclosure_model, foreclosure_scaler,
        borrower_credit_score, debt_to_income_ratio, lender, interest_rate, loan_amount,
        state, zip_code, loan_term, loan_to_value, combined_loan_to_value, borrower_count,
        first_time_homebuyer, loan_purpose, property_type, unit_count, occupancy_status,
        product_type, co_borrower_credit_score
    )
    delinquency_probability = predict_single_data(delinquency_model, delinquency_scaler,
        borrower_credit_score, debt_to_income_ratio, lender, interest_rate, loan_amount,
        state, zip_code, loan_term, loan_to_value, combined_loan_to_value, borrower_count,
        first_time_homebuyer, loan_purpose, property_type, unit_count, occupancy_status,
        product_type, co_borrower_credit_score
    )

    print('foreclosure_probability ({}) = {}', type(foreclosure_probability), foreclosure_probability)
    print('delinquency_probability ({}) = {}', type(delinquency_probability), delinquency_probability)
    pred = form_prediction_result(foreclosure_probability, delinquency_probability)
    return render_template('predict_page.html', pred=pred, options=ALL_SELECTION_OTIONS)

def get_categorical_value(element, category):
    if request.form[element] in CATEGORICAL_INDEX_MAP[category]:
        return CATEGORICAL_INDEX_MAP[category][request.form[element]]
    else:
        return 0

def form_prediction_result(foreclosure_probability, delinquency_probability):
    foreclosure_probability_percentage = int(100*foreclosure_probability)
    delinquency_probability_percentage = int(100*delinquency_probability)
    result = '<div class="box centered"><h4>Prediction</h4>'
    result += '<section>foreclosure probability = {}%</section>'.format(foreclosure_probability_percentage)
    result += '<section>delinquency probability = {}%</section>'.format(delinquency_probability_percentage)
    result += '<br>';
    if foreclosure_probability_percentage > 10:
        result += '<label class="alarm">There is a significant risk that your house will be foreclosed on during the loan term. Consider purchasing a less expensive house or getting a better interest rate.</label>'
    elif delinquency_probability_percentage > 40:
        result += '<label class="warning">There is minimal risk for your house to be foreclosed on, but you will be in risk of missing one or more mortgage payments during your loan term, unless you have some emergency savings.</label>'
    else:
        result += '<label class="thumbsup">Your loan amount looks safe with minimal risk of foreclosure or delinquency.</label>'

    return result

    
    
@app.route('/vis',methods=['GET','POST'])
def vis1():
    #int_features = [x for x in request.form.values()]
    #final = np.array(int_features)
    #data_unseen = pd.DataFrame([final], columns = cols)
    #prediction = predict_model(model, data=data_unseen, round = 0)
    #prediction = int(prediction.Label[0])
    #prediction =10
    
    #return render_template('loan_home.html',pred='Expected Bill will be {}'.format(prediction))
    return render_template('vis1.html')    

@app.route('/predict_api',methods=['POST'])
def predict_api():
    data = request.get_json(force=True)
    data_unseen = pd.DataFrame([data])
    prediction = predict_model(model, data=data_unseen)
    output = prediction.Label[0]
    return jsonify(output)

if __name__ == '__main__':
    train = read()
    train_model(foreclosure_model, train, settings.FORECLOSURE_TARGET, foreclosure_scaler)
    train_model(delinquency_model, train, settings.DELINQUENCY_TARGET, delinquency_scaler)

    app.run(debug=True, host='0.0.0.0', port=5775, use_reloader=False)





