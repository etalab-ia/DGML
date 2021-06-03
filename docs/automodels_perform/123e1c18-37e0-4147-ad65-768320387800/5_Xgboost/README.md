# Summary of 5_Xgboost

[<< Go back](../README.md)


## Extreme Gradient Boosting (Xgboost)
- **objective**: reg:squarederror
- **eval_metric**: rmse
- **eta**: 0.05
- **max_depth**: 8
- **min_child_weight**: 5
- **subsample**: 1.0
- **colsample_bytree**: 1.0
- **explain_level**: 1

## Validation
 - **validation_type**: kfold
 - **k_folds**: 5
 - **shuffle**: True

## Optimized metric
rmse

## Training time

36.1 seconds

### Metric details:
| Metric   |       Score |
|:---------|------------:|
| MAE      |   21.2899   |
| MSE      | 1785.57     |
| RMSE     |   42.256    |
| R2       |    0.544639 |



## Learning curves
![Learning curves](learning_curves.png)

## Permutation-based Importance
![Permutation-based Importance](permutation_importance.png)

[<< Go back](../README.md)
