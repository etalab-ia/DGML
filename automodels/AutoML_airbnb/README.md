# AutoML Leaderboard

| Best model   | name                                                                             | model_type     | metric_type   |   metric_value |   train_time |
|:-------------|:---------------------------------------------------------------------------------|:---------------|:--------------|---------------:|-------------:|
|              | [1_Baseline](1_Baseline/README.md)                                               | Baseline       | rmse          |        65.581  |         0.28 |
|              | [2_DecisionTree](2_DecisionTree/README.md)                                       | Decision Tree  | rmse          |        52.8481 |        11.49 |
|              | [3_Linear](3_Linear/README.md)                                                   | Linear         | rmse          |        40.2766 |        10.6  |
|              | [4_Default_Xgboost](4_Default_Xgboost/README.md)                                 | Xgboost        | rmse          |        43.2487 |        18.14 |
|              | [5_Default_NeuralNetwork](5_Default_NeuralNetwork/README.md)                     | Neural Network | rmse          |        51.7376 |         2.64 |
|              | [6_Default_RandomForest](6_Default_RandomForest/README.md)                       | Random Forest  | rmse          |        46.464  |        14.69 |
|              | [4_Default_Xgboost_categorical_mix](4_Default_Xgboost_categorical_mix/README.md) | Xgboost        | rmse          |        43.0563 |        17.62 |
| **the best** | [Ensemble](Ensemble/README.md)                                                   | Ensemble       | rmse          |        38.3926 |         0.14 |

### AutoML Performance
![AutoML Performance](ldb_performance.png)

### AutoML Performance Boxplot
![AutoML Performance Boxplot](ldb_performance_boxplot.png)