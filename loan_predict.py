from flask import Flask, render_template, request
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from prediction_model import read, train_model, predict_single_data
from categoricals import CATEGORICAL_INDEX_MAP
from selections import ALL_SELECTION_OTIONS
import settings
from sklearn.svm import LinearSVC

foreclosure_scaler = StandardScaler()
foreclosure_model = LogisticRegression(random_state=0, class_weight="balanced")
#foreclosure_model = LinearSVC(random_state=0, class_weight="balanced")
delinquency_scaler = StandardScaler()
delinquency_model = LogisticRegression(random_state=0, class_weight="balanced")
#delinquency_model = LinearSVC(random_state=0, class_weight="balanced")

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
        return render_template('predict_page.html', pred='', options=ALL_SELECTION_OTIONS, selections=get_default_selections(), recommendations=[])
    
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
    debt_to_income_ratio = compute_dti(income, loan_amount, interest_rate, loan_term)
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

    #print('foreclosure_probability ({}) = {}', type(foreclosure_probability), foreclosure_probability)
    #print('delinquency_probability ({}) = {}', type(delinquency_probability), delinquency_probability)
    
    pred = form_prediction_result(foreclosure_probability, delinquency_probability)
    
    if(get_pred_Status(foreclosure_probability)==1):

        recommendations=[]

        result_property_low, result_property_high = find_optimum_price(foreclosure_model, foreclosure_scaler,
        borrower_credit_score, debt_to_income_ratio, lender, interest_rate, loan_amount/2,
        state, zip_code, loan_term, loan_to_value, combined_loan_to_value, borrower_count,
        first_time_homebuyer, loan_purpose, property_type, unit_count, occupancy_status,
        product_type, co_borrower_credit_score, income, 40000, property_value)

        print("prinint optimum values for property_value")
        print(result_property_low)
        print(result_property_high)

        if(result_property_low!=-1):
            value_array, prob_array=create_array_for_chart('property_value', result_property_low, property_value, foreclosure_model, foreclosure_scaler,
            borrower_credit_score, debt_to_income_ratio, lender, interest_rate, loan_amount,
            state, zip_code, loan_term, loan_to_value, combined_loan_to_value, borrower_count,
            first_time_homebuyer, loan_purpose, property_type, unit_count, occupancy_status,
            product_type, co_borrower_credit_score, income)

            recommendations.append({'param': 'property_value','values': value_array, 'probs': prob_array, 'text': 'If you get a property of value '+ str(result_property_low) +"%, your chance of foreclosure will go down to "+ str(int(100*prob_array[0]))+'%.'})


        result_interest_rate_low, result_interest_rate_high = find_optimum_interest_rate(foreclosure_model, foreclosure_scaler,
        borrower_credit_score, debt_to_income_ratio, lender, interest_rate, loan_amount,
        state, zip_code, loan_term, loan_to_value, combined_loan_to_value, borrower_count,
        first_time_homebuyer, loan_purpose, property_type, unit_count, occupancy_status,
        product_type, co_borrower_credit_score, income, 2.3, interest_rate)

        print("prinint optimum values for interest_rate")
        print(result_interest_rate_low)
        print(result_interest_rate_high)

        if(result_interest_rate_low!=-1):
            value_array, prob_array=create_array_for_chart('interest_rate', result_interest_rate_low, interest_rate, foreclosure_model, foreclosure_scaler,
            borrower_credit_score, debt_to_income_ratio, lender, interest_rate, loan_amount,
            state, zip_code, loan_term, loan_to_value, combined_loan_to_value, borrower_count,
            first_time_homebuyer, loan_purpose, property_type, unit_count, occupancy_status,
            product_type, co_borrower_credit_score, income)

            recommendations.append({'param': 'interest_rate','values': value_array, 'probs': prob_array, 'text': 'If you get an interest rate of '+ str("{:.2f}".format(result_interest_rate_low)) +"%, your chance of foreclosure will go down to "+ str(int(100*prob_array[0]))+'%.'})

        result_credit_score_low, result_credit_score_high = find_optimum_credit_score(foreclosure_model, foreclosure_scaler,
        borrower_credit_score, debt_to_income_ratio, lender, interest_rate, loan_amount,
        state, zip_code, loan_term, loan_to_value, combined_loan_to_value, borrower_count,
        first_time_homebuyer, loan_purpose, property_type, unit_count, occupancy_status,
        product_type, co_borrower_credit_score, income, borrower_credit_score, 850)

        print("prinint optimum values for borrower_credit_score")
        print(result_credit_score_low)
        print(result_credit_score_high)

        if(result_credit_score_low!=-1):
            value_array, prob_array=create_array_for_chart('borrower_credit_score', borrower_credit_score, result_credit_score_high, foreclosure_model, foreclosure_scaler,
            borrower_credit_score, debt_to_income_ratio, lender, interest_rate, loan_amount,
            state, zip_code, loan_term, loan_to_value, combined_loan_to_value, borrower_count,
            first_time_homebuyer, loan_purpose, property_type, unit_count, occupancy_status,
            product_type, co_borrower_credit_score, income)

            recommendations.append({'param': 'borrower_credit_score','values': value_array, 'probs': prob_array, 'text': 'If your credit scrore increases to '+ str(result_credit_score_high) +", your chance of foreclosure will go down to "+ str(int(100*prob_array[-1]))+'%.'})


        find_optimum_bank(foreclosure_model, foreclosure_scaler,
        borrower_credit_score, debt_to_income_ratio, lender, interest_rate, loan_amount,
        state, zip_code, loan_term, loan_to_value, combined_loan_to_value, borrower_count,
        first_time_homebuyer, loan_purpose, property_type, unit_count, occupancy_status,
        product_type, co_borrower_credit_score)

    return render_template('predict_page.html', pred=pred, options=ALL_SELECTION_OTIONS, selections=request.form, recommendations=recommendations)

def create_array_for_chart(param, low, high, foreclosure_model, foreclosure_scaler,
    borrower_credit_score, debt_to_income_ratio, lender, interest_rate, loan_amount,
    state, zip_code, loan_term, loan_to_value, combined_loan_to_value, borrower_count,
    first_time_homebuyer, loan_purpose, property_type, unit_count, occupancy_status,
    product_type, co_borrower_credit_score, income):

    value_array=[]
    prob_list=[]

    if(param=='interest_rate'):
        
        while(low<high):
            new_debt_to_income_ratio = compute_dti(income, loan_amount, low, loan_term)

            foreclosure_probability = predict_single_data(foreclosure_model, foreclosure_scaler,
                borrower_credit_score, new_debt_to_income_ratio, lender, low, loan_amount,
                state, zip_code, loan_term, loan_to_value, combined_loan_to_value, borrower_count,
                first_time_homebuyer, loan_purpose, property_type, unit_count, occupancy_status,
                product_type, co_borrower_credit_score
            )
            value_array.append(low)
            prob_list.append(foreclosure_probability)
            low=low+0.2

    elif(param=='property_value'):
        while(low<high):
            
            down_payment=100.0-loan_to_value
            new_loan_amount = (low * (100.0-down_payment))/100.0
            new_debt_to_income_ratio = compute_dti(income, new_loan_amount, interest_rate, loan_term)

            foreclosure_probability = predict_single_data(foreclosure_model, foreclosure_scaler,
                borrower_credit_score, new_debt_to_income_ratio, lender, low, new_loan_amount,
                state, zip_code, loan_term, loan_to_value, combined_loan_to_value, borrower_count,
                first_time_homebuyer, loan_purpose, property_type, unit_count, occupancy_status,
                product_type, co_borrower_credit_score
            )
            value_array.append(low)
            prob_list.append(foreclosure_probability)
            low=low+20000
    elif(param=='borrower_credit_score'):
        while(low<high):
            
            foreclosure_probability = predict_single_data(foreclosure_model, foreclosure_scaler,
                borrower_credit_score, debt_to_income_ratio, lender, low, loan_amount,
                state, zip_code, loan_term, loan_to_value, combined_loan_to_value, borrower_count,
                first_time_homebuyer, loan_purpose, property_type, unit_count, occupancy_status,
                product_type, co_borrower_credit_score
            )
            value_array.append(low)
            prob_list.append(foreclosure_probability)
            low=low+20


    print(value_array)
    print(prob_list)
    return value_array, prob_list





def get_default_selections():
    return {
        'first_time_homebuyer': 'Y',
        'property_type': 'SF',
        'unit_count': 1,
        'occupancy_status': 'P',
        'loan_purpose': 'P'
    }

def compute_dti(annual_income, loan_amount, annual_interest, loan_term):
    monthly_interest = annual_interest / 1200.0
    monthly_payment = 1.0 * loan_amount * (monthly_interest * (1.0 + monthly_interest) ** loan_term) / ((1.0 + monthly_interest) ** loan_term - 1.0)
    return int(100.0 * monthly_payment / (annual_income / 12.0))

def find_optimum_credit_score(foreclosure_model, foreclosure_scaler,
        borrower_credit_score, debt_to_income_ratio, lender, interest_rate, loan_amount,
        state, zip_code, loan_term, loan_to_value, combined_loan_to_value, borrower_count,
        first_time_homebuyer, loan_purpose, property_type, unit_count, occupancy_status,
        product_type, co_borrower_credit_score, income, low, high):

        #print("current low credit= "+ str(low)+", current high credit= "+str(high))

        if(low>high):
            #print('checkpoint 1')
            #print('-1, -1')
            return -1, -1
        elif(high-low<=20):

            #print('checkpoint 2')
            
            foreclosure_probability = predict_single_data(foreclosure_model, foreclosure_scaler,
            low, debt_to_income_ratio, lender, interest_rate, loan_amount,
            state, zip_code, loan_term, loan_to_value, combined_loan_to_value, borrower_count,
            first_time_homebuyer, loan_purpose, property_type, unit_count, occupancy_status,
            product_type, co_borrower_credit_score)
            #print('foreclosure probability for credit score '+str(low)+' is '+str(foreclosure_probability))

            if(get_pred_Status(foreclosure_probability)==1):
                #print('-1, -1')
                return -1, -1
            else:
                #print("low credit = "+ str(low)+", high credit = "+str(high))
                return  low, high

        #print('checkpoint 3')
        mid = low+ (high-low)/2

        
        foreclosure_probability = predict_single_data(foreclosure_model, foreclosure_scaler,
            mid, debt_to_income_ratio, lender, interest_rate, loan_amount,
            state, zip_code, loan_term, loan_to_value, combined_loan_to_value, borrower_count,
            first_time_homebuyer, loan_purpose, property_type, unit_count, occupancy_status,
            product_type, co_borrower_credit_score
        )
        #print('foreclosure probability for credit '+str(mid)+' is '+str(foreclosure_probability))

        if(get_pred_Status(foreclosure_probability)==1):
            return find_optimum_credit_score(foreclosure_model, foreclosure_scaler,
            borrower_credit_score, debt_to_income_ratio, lender, interest_rate, loan_amount,
            state, zip_code, loan_term, loan_to_value, combined_loan_to_value, borrower_count,
            first_time_homebuyer, loan_purpose, property_type, unit_count, occupancy_status,
            product_type, co_borrower_credit_score, income, low, mid)
        else:
            return find_optimum_credit_score(foreclosure_model, foreclosure_scaler, 
            borrower_credit_score, debt_to_income_ratio, lender, interest_rate, new_loan_amount,
            state, zip_code, loan_term, loan_to_value, combined_loan_to_value, borrower_count,
            first_time_homebuyer, loan_purpose, property_type, unit_count, occupancy_status,
            product_type, co_borrower_credit_score, income, mid, high)

def find_optimum_price(foreclosure_model, foreclosure_scaler,
        borrower_credit_score, debt_to_income_ratio, lender, interest_rate, loan_amount,
        state, zip_code, loan_term, loan_to_value, combined_loan_to_value, borrower_count,
        first_time_homebuyer, loan_purpose, property_type, unit_count, occupancy_status,
        product_type, co_borrower_credit_score, income, low, high):

        #print("current low price= "+ str(low)+", current high price= "+str(high))

        if(low>high):
            #print('checkpoint 1')
            #print('-1, -1')
            return -1, -1
        elif(high-low<=10000):

            #print('checkpoint 2')
            down_payment=100.0-loan_to_value
            new_loan_amount = (low * (100.0-down_payment))/100.0
            new_debt_to_income_ratio = compute_dti(income, new_loan_amount, interest_rate, loan_term)


            foreclosure_probability = predict_single_data(foreclosure_model, foreclosure_scaler,
            borrower_credit_score, new_debt_to_income_ratio, lender, interest_rate, new_loan_amount,
            state, zip_code, loan_term, loan_to_value, combined_loan_to_value, borrower_count,
            first_time_homebuyer, loan_purpose, property_type, unit_count, occupancy_status,
            product_type, co_borrower_credit_score)
            #print('foreclosure probability for price '+str(low)+' is '+str(foreclosure_probability))

            if(get_pred_Status(foreclosure_probability)==1):
                #print('-1, -1')
                return -1, -1
            else:
                #print("low price = "+ str(low)+", high price = "+str(high))
                return  low, high

        #print('checkpoint 3')
        mid = low+ (high-low)/2

        down_payment=100.0-loan_to_value
        new_loan_amount = (mid * (100.0-down_payment))/100.0
        new_debt_to_income_ratio = compute_dti(income, new_loan_amount, interest_rate, loan_term)

        foreclosure_probability = predict_single_data(foreclosure_model, foreclosure_scaler,
            borrower_credit_score, new_debt_to_income_ratio, lender, interest_rate, new_loan_amount,
            state, zip_code, loan_term, loan_to_value, combined_loan_to_value, borrower_count,
            first_time_homebuyer, loan_purpose, property_type, unit_count, occupancy_status,
            product_type, co_borrower_credit_score
        )
        #print('foreclosure probability for price '+str(mid)+' is '+str(foreclosure_probability))

        if(get_pred_Status(foreclosure_probability)==1):
            return find_optimum_price(foreclosure_model, foreclosure_scaler,
            borrower_credit_score, new_debt_to_income_ratio, lender, interest_rate, new_loan_amount,
            state, zip_code, loan_term, loan_to_value, combined_loan_to_value, borrower_count,
            first_time_homebuyer, loan_purpose, property_type, unit_count, occupancy_status,
            product_type, co_borrower_credit_score, income, low, mid)
        else:
            return find_optimum_price(foreclosure_model, foreclosure_scaler, borrower_credit_score, new_debt_to_income_ratio, lender, interest_rate, new_loan_amount,
            state, zip_code, loan_term, loan_to_value, combined_loan_to_value, borrower_count,
            first_time_homebuyer, loan_purpose, property_type, unit_count, occupancy_status,
            product_type, co_borrower_credit_score, income, mid, high)

def find_optimum_interest_rate(foreclosure_model, foreclosure_scaler,
        borrower_credit_score, debt_to_income_ratio, lender, interest_rate, loan_amount,
        state, zip_code, loan_term, loan_to_value, combined_loan_to_value, borrower_count,
        first_time_homebuyer, loan_purpose, property_type, unit_count, occupancy_status,
        product_type, co_borrower_credit_score, income, low, high):

        #print("current low interest_rate= "+ str(low)+", current high interest_rate= "+str(high))

        if(low>high):
            #print('-1, -1')
            return -1, -1
        elif(high-low<=0.1):

            #print('checkpoint 2')
            new_debt_to_income_ratio = compute_dti(income, loan_amount, low, loan_term)

            foreclosure_probability = predict_single_data(foreclosure_model, foreclosure_scaler,
            borrower_credit_score, new_debt_to_income_ratio, lender,  low, loan_amount,
            state, zip_code, loan_term, loan_to_value, combined_loan_to_value, borrower_count,
            first_time_homebuyer, loan_purpose, property_type, unit_count, occupancy_status,
            product_type, co_borrower_credit_score)
            #print('foreclosure probability for interest rate '+str(low)+' is '+str(foreclosure_probability))

            if(get_pred_Status(foreclosure_probability)==1):
                #print('-1, -1')
                return -1, -1
            else:
                #print("low interest= "+ str(low)+", high interest rate= "+str(high))
                return  low, high
        #print('checkpoint 3')
        mid = low+ (high-low)/2

        
        new_debt_to_income_ratio = compute_dti(income, loan_amount, mid, loan_term)

        foreclosure_probability = predict_single_data(foreclosure_model, foreclosure_scaler,
            borrower_credit_score, new_debt_to_income_ratio, lender, mid, loan_amount,
            state, zip_code, loan_term, loan_to_value, combined_loan_to_value, borrower_count,
            first_time_homebuyer, loan_purpose, property_type, unit_count, occupancy_status,
            product_type, co_borrower_credit_score
        )
        #print('foreclosure probability for interest rate '+str(mid)+' is '+str(foreclosure_probability))
        if(get_pred_Status(foreclosure_probability)==1):
            return find_optimum_interest_rate(foreclosure_model, foreclosure_scaler,
            borrower_credit_score, new_debt_to_income_ratio, lender, mid, loan_amount,
            state, zip_code, loan_term, loan_to_value, combined_loan_to_value, borrower_count,
            first_time_homebuyer, loan_purpose, property_type, unit_count, occupancy_status,
            product_type, co_borrower_credit_score, income, low, mid)
        else:
            return find_optimum_interest_rate(foreclosure_model, foreclosure_scaler,
            borrower_credit_score, new_debt_to_income_ratio, lender, mid, loan_amount,
            state, zip_code, loan_term, loan_to_value, combined_loan_to_value, borrower_count,
            first_time_homebuyer, loan_purpose, property_type, unit_count, occupancy_status,
            product_type, co_borrower_credit_score, income, mid, high)


def find_optimum_bank(foreclosure_model, foreclosure_scaler,
        borrower_credit_score, debt_to_income_ratio, lender, interest_rate, loan_amount,
        state, zip_code, loan_term, loan_to_value, combined_loan_to_value, borrower_count,
        first_time_homebuyer, loan_purpose, property_type, unit_count, occupancy_status,
        product_type, co_borrower_credit_score):

        temp = list(ALL_SELECTION_OTIONS["lender"].items())

        num_banks = len(temp)

        for i in range(num_banks):
            foreclosure_probability = predict_single_data(foreclosure_model, foreclosure_scaler,
            borrower_credit_score, debt_to_income_ratio, i,  interest_rate, loan_amount,
            state, zip_code, loan_term, loan_to_value, combined_loan_to_value, borrower_count,
            first_time_homebuyer, loan_purpose, property_type, unit_count, occupancy_status,
            product_type, co_borrower_credit_score)
            #print('foreclosure probability for bank '+str(temp[i][0])+' is '+str(foreclosure_probability))



def get_pred_Status(foreclosure_probability):
    foreclosure_probability_percentage = int(100*foreclosure_probability)
    #print("foreclosure_probability_percentage="+str(foreclosure_probability_percentage))

    if foreclosure_probability_percentage > 20:
        return 1
    else:
        return 0

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
        flag_fc=1
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

@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    return render_template('reco.html', recommendations=request.form['recommendations'])

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





