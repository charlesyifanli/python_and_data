## Introduction

1. The entire project consists of five files, each containing a class.
2. The `Robot` class is responsible for integrating and invoking other classes.
3. The `Clean` class handles missing value processing and data type conversion.
4. The `Inspection` class is responsible for data classification and then visualizing the results through charts.
5. The `Analysis` class is in charge of data analysis and relationship prediction.
6. The `Sentiment` class performs sentiment analysis on text data.

## Clean

1. The `Clean` class is used for data cleaning, handling missing values and data type conversions.
2. The `process` method iterates over each column and calls `handle_missing_values` to either fill or drop missing
   values. If more than 50% of a column's data is missing, the column is dropped; otherwise, it's filled with the median
   or mode depending on the data type.
3. The `check_data_types` method attempts to convert the column to a numeric type.

## Inspection

1. The `Inspection` class is used for classifying data, performing statistical calculations, and visualizing it. It
   first identifies column types through the `list_column_types` method, categorizing them as nominal, numeric ordinal,
   non-numeric ordinal, or interval data.
2. Then, it uses `calculate_and_show` to display statistical information such as mean, mode, and standard deviation.
3. Finally, the `plot_data` method offers various visualization options, including bar charts, box plots, histograms,
   and scatter plots.

## Analysis

1. The `Analysis` class performs hypothesis testing and regression analysis on both numeric and categorical data.
2. It provides three main types of analysis: numeric vs. categorical, categorical only, and numeric only (regression).
3. For numeric data, it checks normality and uses appropriate statistical tests (e.g., t-test, ANOVA, Mann-Whitney U,
   Kruskal-Wallis).
4. For categorical data, it uses chi-square testing. For numeric-only analysis, it performs linear regression and
   displays a regression line, providing key insights such as correlation and R-squared values.

## Sentiment

1. This `Sentiment` class performs sentiment analysis using three methods: Vader, TextBlob, and DistilBERT (if
   available). It processes text columns from a DataFrame, allowing the user to select a column for analysis.
2. Depending on the chosen method, the class outputs sentiment scores and classifications (positive, neutral, or
   negative).
3. Vader uses rule-based analysis, TextBlob calculates polarity and subjectivity, while DistilBERT leverages a
   pre-trained transformer model for a more nuanced sentiment analysis.

## Robot

1. This script defines a `Robot` class to load a CSV dataset, then cleans, inspects, analyzes, and performs sentiment
   analysis on the data.
2. The main function integrates the `Clean`, `Inspection`, `Analysis`, and `Sentiment` classes, allowing the user to
   clean data, conduct hypothesis testing, and analyze sentiments interactively.
3. It presents options for visualizing data, testing hypotheses, and performing sentiment analysis, all driven by user
   input in a loop until the user chooses to quit.
