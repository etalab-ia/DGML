# AutoML Leaderboard

| Best model   | name                                                         | model_type   | metric_type   |   metric_value |   train_time |
|:-------------|:-------------------------------------------------------------|:-------------|:--------------|---------------:|-------------:|
|              | [1_Linear](1_Linear/README.md)                               | Linear       | rmse          |        40.3491 |        17.02 |
|              | [2_Default_LightGBM](2_Default_LightGBM/README.md)           | LightGBM     | rmse          |        41.8809 |        35.51 |
|              | [3_Default_Xgboost](3_Default_Xgboost/README.md)             | Xgboost      | rmse          |        42.2151 |        27.57 |
|              | [4_Default_CatBoost](4_Default_CatBoost/README.md)           | CatBoost     | rmse          |        41.6113 |        56.08 |
|              | [9_LightGBM](9_LightGBM/README.md)                           | LightGBM     | rmse          |        41.7168 |        34.62 |
|              | [5_Xgboost](5_Xgboost/README.md)                             | Xgboost      | rmse          |        42.256  |        36.88 |
|              | [1_Linear_GoldenFeatures](1_Linear_GoldenFeatures/README.md) | Linear       | rmse          |        40.7032 |         7.44 |
| **the best** | [Ensemble](Ensemble/README.md)                               | Ensemble     | rmse          |        39.3104 |         0.15 |

### AutoML Performance
![AutoML Performance](ldb_performance.png)

### AutoML Performance Boxplot
![AutoML Performance Boxplot](ldb_performance_boxplot.png)