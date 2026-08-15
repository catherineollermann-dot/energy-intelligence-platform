# ⚡ Energy Intelligence Platform

An interactive energy analytics platform built with Python and Streamlit to explore historical U.S. energy data, compare state-level trends, visualize geographic patterns, and experiment with predictive modeling.

This project was developed as part of my professional data and technology portfolio while pursuing an M.S. in Science & Technology Management with a Computer Science focus.

## 📊 Project Overview

The Energy Intelligence Platform transforms a large U.S. energy dataset into an interactive analytical dashboard.

Users can upload the dataset and dynamically explore energy indicators across U.S. states and historical periods.

The platform combines data processing, interactive visualization, statistical analysis, and experimental machine learning in a single application.

## 🚀 Features

- CSV dataset upload and processing
- Interactive state selection
- Energy indicator filtering
- Historical year-range filtering
- U.S. state-level energy consumption map
- Dynamic map-year selection
- Comparison of energy trends between two states
- Minimum, average, and maximum consumption metrics
- Automated analytical insights
- Historical dataset preview
- Experimental 5-year trend projection using Linear Regression

## 🛠️ Technologies

- Python
- Pandas
- Streamlit
- Plotly
- Scikit-learn
- Git / GitHub

## 🤖 Machine Learning

The project includes an experimental 5-year trend projection using Linear Regression.

During development, multiple modeling approaches were evaluated. Random Forest initially produced strong results with a random train/test split, but performance deteriorated substantially when temporal validation was applied.

This highlighted an important time-series modeling consideration: strong performance on randomly divided historical observations does not necessarily translate into reliable future predictions.

For this reason, the application presents the Linear Regression output as an **experimental trend projection rather than a validated forecast**.

## 📈 Analytical Capabilities

The dashboard allows users to:

- Compare historical energy patterns between U.S. states
- Identify historical peaks and minimum values
- Analyze average energy consumption
- Explore geographic differences through an interactive map
- Adjust analysis periods dynamically
- Examine experimental future trend projections

## 📂 Dataset

The application is designed to work with U.S. state-level historical energy data containing fields such as:

- `StateCode`
- `Year`
- `MSN`
- `Data`
- `Data_Status`

The dataset used during development contains more than 2.5 million observations.

## ⚠️ Model Limitation

The predictive component is intended for educational and exploratory analysis.

Historical energy behavior may be nonlinear and influenced by economic, technological, policy, environmental, and market factors that are not included as model features.

The projected values should therefore not be interpreted as production-grade energy forecasts.

## 👩‍💻 Author

**Catherine Ollermann**

M.S. Science & Technology Management — Computer Science Focus  
B.S. Petroleum Engineering