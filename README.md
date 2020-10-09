Loan Prediction
-----------------------

If a potential home buyer gets a loan from the bank, predict if it's too risky for them. The app will tell the buyer their chance of foreclosure and delinquency. 
The app will also visualize relevant data on maps and cartograms.

Installation
----------------------

### Download the data

* Clone this repo to your computer.
* Get into the folder using `cd loan-prediction-vis`.
* Run `mkdir data`.
* Switch into the `data` directory using `cd data`.
* Download the data files from Fannie Mae into the `data` directory.  
    * You can find the data [here](http://www.fanniemae.com/portal/funding-the-market/data/loan-performance-data.html).
    * You'll need to register with Fannie Mae to download the data.
    * It's recommended to download all the data from 2015 Q1 to present.
* Extract all of the `.zip` files you downloaded.
    * On OSX, you can run `find ./ -name \*.zip -exec unzip {} \;`.
    * At the end, you should have a bunch of text files called `Acquisition_YQX.txt`, and `Performance_YQX.txt`, where `Y` is a year, and `X` is a number from `1` to `4`.
* Remove all the zip files by running `rm *.zip`.
* Switch back into the `loan-prediction-vis` directory using `cd ..`.

### Install the requirements
 
* Install the requirements using `pip install -r requirements.txt`.
    * Make sure you use Python 3.
    

Usage
-----------------------

* Run `mkdir processed` to create a directory for our processed datasets.
* Run `python assemble.py` to combine the `Acquisition` and `Performance` datasets.
    * This will create `Acquisition.txt` and `Performance.txt` in the `processed` folder.
* Run `python annotate.py`.
    * This will create training data from `Acquisition.txt` and `Performance.txt`.
    * It will add a file called `train.csv` to the `processed` folder.
* Run `python prediction_model.py`.
    * This will print the accuracy scores.  
* Run `python loan_predict.py`.
    * This will run run the app.
