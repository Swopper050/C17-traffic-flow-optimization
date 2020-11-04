"""
This file contains the code for performing polynomial and multiple linear regression
on the density versus timesteps data collected from simulation. The coefficients of
the final model are extracted and the equation is used to predict time delays. 
"""
import pdb

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures


def perform_poly_regression(config):
    """
    Performs polynomial regression on Density versus timesteps on road data collect through simulations.
    :param config: namespace with the configuration for the run
    """
    dataset = pd.read_csv(f"{config.dir}/reg_data.csv")
    dataset = dataset[dataset.columns[-2:]]
    X = dataset.iloc[:, -2].values
    y = dataset.iloc[:, -1].values
    X = X.reshape(-1, 1)

    #Initialise a Polynomial Regressor of Degree 4
    #Fit the entire dataset to polynomial features
    #Use a linear egressor on this to estimate result
    
    poly_reg = PolynomialFeatures(degree=4)
    X_poly = poly_reg.fit_transform(X)
    lin_reg = LinearRegression()
    lin_reg.fit(X_poly, y)

    #R Squared score gives the accuracy of the predictor on the dataset
    print("R Squared Score of Polynomial regressor:" + str(lin_reg.score(X_poly, y)))

    # Visualising the Polynomial Regression results (for higher resolution and smoother curve)
    X_grid = np.arange(min(X), max(X), 0.01)
    X_grid = X_grid.reshape((len(X_grid), 1))
    plt.scatter(X, y, color="red")
    plt.plot(X_grid, lin_reg.predict(poly_reg.fit_transform(X_grid)), color="blue")
    plt.title("Polynomial Regression of Density vs TIme")
    plt.xlabel("Density")
    plt.ylabel("Timesteps on Road")
    plt.savefig("Poly2.png")
    plt.show()

def perform_multiple_lin_regression(config):
    """
    Performs multiple regression on Speed, Road Length, Density versus timesteps on road data collect through simulations.
    :param config: namespace with the configuration for the run
    """
    dataset = pd.read_csv(f"{config.dir}/reg_data.csv")
    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, -1].values

    # Splitting the dataset into the Training set and Test set
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0
    )

    # Training the Multiple Linear Regression model on the Training set

    regressor = LinearRegression()
    regressor.fit(X_train, y_train)

    # Predicting the Test set results
    y_pred = regressor.predict(X_test)
    np.set_printoptions(precision=2)
    print(
        np.concatenate(
            (y_pred.reshape(len(y_pred), 1), y_test.reshape(len(y_test), 1)), 1
        )
    )
    print("Score of Mulitple Linear regressor:" + str(regressor.score(X_test, y_test)))
