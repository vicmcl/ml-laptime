# F1 Lap Time Forecasting

## Introduction

This repository contains a machine learning project that aims to predict lap times in Formula 1 using historical data and advanced data science techniques. The project leverages the power of XGBoost to build a robust and accurate model that can forecast lap times based on a variety of factors, including track conditions, weather, and driver performance. The goal of this project is to provide a data-driven approach to understanding F1 performance and to explore the potential of machine learning in motorsport.

## Data Sources

The [FastF1](https://github.com/theOehrly/Fast-F1) package is a wrapper for an API giving access to the data needed to train the model: 
* historical laps data from previous races
* track-specific data
* weather information
* car telemetry

## Training

Each circuit, car and driver have specific characteristics influencing lap times that are beyond the scope of this project. Therefore this XGBoost model is track- and team-specific, and is trained on data from Max Verstappen's laps at the Spanish Grand Prix from seasons 2019 and 2020.

The dataset is preprocessed to handle missing values and outliers. Missing values are imputed with the mean. Laps considered as outliers are laps with an incident (safety car, yellow/red flag), pit stops and the first lap of the race. All these laps are removed from the dataset.

The model was then trained using a combination of hyperparameter tuning and cross-validation to optimize its performance. The training process involved splitting the dataset into training and validation sets, and using the training set to train the model while evaluating its performance on the validation set. The model was trained using a variety of hyperparameters, including learning rate, max depth, and number of estimators, to achieve the best possible performance.The XGBoost model was trained on a dataset of historical F1 lap times, which was collected from various sources, including the official F1 website and other online databases. The dataset was preprocessed to handle missing values, outliers, and feature scaling. The model was then trained using a combination of hyperparameter tuning and cross-validation to optimize its performance. The training process involved splitting the dataset into training and validation sets, and using the training set to train the model while evaluating its performance on the validation set. The model was trained using a variety of hyperparameters, including learning rate, max depth, and number of estimators, to achieve the best possible performance.

## Contributing

We welcome contributions! Please see our `CONTRIBUTING.md` file for guidelines on how to submit pull requests, report issues, or suggest improvements.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

Special thanks to [theOehrly](https://github.com/theOehrly) for providing access to historical race data and telemetry information with their FastF1 API.
