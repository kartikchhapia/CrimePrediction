# Minority Report: Predicting Crime Rates for Neighborhoods Using Local Infrastructure and Socio-economic Indicators

## Installation

The project uses Python 2.7 as the programming language of choice. We recommend using conda environments to run our project. You can either install [Anaconda](https://www.continuum.io/downloads) or [Miniconda](https://conda.io/miniconda.html) to run our project. You can then run the command 

`conda env create -f environment.yml`

to build the environment from the `environment.yml` file. Activate the environment by running the command:

`source activate peppermint`.

NOTE: If you wish, you can manually read the `environment.yml` file and add dependencies by scratch.

Further instructions can be found here: https://conda.io/docs/using/envs.html

## Running the code

The following files/directories  contain code that was used to collect and extract the data from APIs:

- code/createCrimeDataset.py (Extracts the historical crime data)
- code/locationsinNYC.py (Collects the landmark data)
- code/CensusDataExtract (Collects census data)

These files were used in the preliminary step and most of the work in data extraction and collection involved commenting out parts of code. We had to do this because the data collection took several hours and the code would often stop running because of disconnections and API limits. Furthermore, we collected three different kinds of data: crime, landmarks and demographic data. All data was collected in several chunks because of these limitations and were later merged.

The main Machine Learning code exists in `code/Models/`. The file `prepare_data.py` contains methods that return subsets of data. It also contains methods that perfrom some data cleaning and adds new composite features. It also contains a method that perfroms Lasso for feature selection. Furthermore, it also uses the stored feature importances and saves it in csv files.

All model evaluation, hyperparam optimization happens in `code/Models/modelTesting.py`. We have created separate methods for each regressor and each method contains flags and config variables that control the execution of the methods. For e.g there is a flag named `fs` that determines whether to perform feature selection. Similarly, there is a config variable named  `data_config` that determines which data subset to use for training. Individual methods can be called from `if __name__ == '__main__'` to train the appropriate regressor and the flags and config variables can be adjusted to achieve the desired behavior. 