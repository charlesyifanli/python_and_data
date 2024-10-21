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

