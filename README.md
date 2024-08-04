# F1 Lap Time Forecasting

## Introduction

This repository contains a machine learning project that aims to predict lap times in Formula 1 using historical data and advanced data science techniques. The project leverages the power of XGBoost to build a robust and accurate model that can forecast lap times based on a variety of factors, including track conditions, weather, and driver performance. The goal of this project is to provide a data-driven approach to understanding F1 performance and to explore the potential of machine learning in motorsport.

## Data Source

The [FastF1](https://github.com/theOehrly/Fast-F1) package is a wrapper for an API giving access to the data needed to train the model: 
* historical laps data from previous races
* track-specific data
* weather information
* car telemetry

## Feature Engineering

### Track and driver

Each circuit, car and driver have specific characteristics influencing lap times that are beyond the scope of this project. Therefore this XGBoost model is track- and team-specific, and the dataset is taken from Max Verstappen's laps at the Spanish Grand Prix from seasons 2019 and 2020.

### Feature selection

Features are selected based on their correlation with lap times in training data while minimizing correlation between themselves. Telemetry data is processed to get average values for each lap, such as throttle position and braking time.

### Imputation and outliers

The dataset is preprocessed to handle missing values and outliers. Missing values are imputed with the mean. Laps considered as outliers are laps with an incident (safety car, yellow/red flag), pit stops and the first lap of the race. All these laps are removed from the dataset.

## Training

### Hyperparameter tuning 

A grid search is used with a series of XGBoost parameters, including tree depth, number of estimators and learning rate.

### Cross-validation

Different subsets of the most recent laps in training data are taken to create validation sets. The grid search optimization finds the set of parameters that minimize the loss function over all validation sets.

## Contributing

We welcome contributions! Please see our `CONTRIBUTING.md` file for guidelines on how to submit pull requests, report issues, or suggest improvements.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

Special thanks to [theOehrly](https://github.com/theOehrly) for providing access to historical race data and telemetry information with their FastF1 API.
