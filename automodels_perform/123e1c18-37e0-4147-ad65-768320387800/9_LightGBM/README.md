# Summary of 9_LightGBM

[<< Go back](../README.md)


## LightGBM
- **objective**: regression
- **metric**: rmse
- **num_leaves**: 15
- **learning_rate**: 0.05
- **feature_fraction**: 0.8
- **bagging_fraction**: 0.5
- **min_data_in_leaf**: 50
- **explain_level**: 1

## Validation
 - **validation_type**: kfold
 - **k_folds**: 5
 - **shuffle**: True

## Optimized metric
rmse

## Training time

33.9 seconds

### Metric details:
| Metric   |       Score |
|:---------|------------:|
| MAE      |   20.8032   |
| MSE      | 1740.29     |
| RMSE     |   41.7168   |
| R2       |    0.556188 |



## Learning curves
![Learning curves](learning_curves.png)

## Permutation-based Importance
![Permutation-based Importance](permutation_importance.png)

[<< Go back](../README.md)
