# Summary of 3_Default_Xgboost

[<< Go back](../README.md)


## Extreme Gradient Boosting (Xgboost)
- **n_jobs**: -1
- **objective**: multi:softprob
- **eval_metric**: mlogloss
- **eta**: 0.075
- **max_depth**: 6
- **min_child_weight**: 1
- **subsample**: 1.0
- **colsample_bytree**: 1.0
- **num_class**: 4
- **explain_level**: 0

## Validation
 - **validation_type**: split
 - **train_ratio**: 0.75
 - **shuffle**: True
 - **stratify**: True

## Optimized metric
logloss

## Training time

17.3 seconds

### Metric details
|           |            1 |           2 |           3 |           4 |   accuracy |    macro avg |   weighted avg |   logloss |
|:----------|-------------:|------------:|------------:|------------:|-----------:|-------------:|---------------:|----------:|
| precision |     0.738655 |   0.393701  |    0.517142 |    0.664934 |   0.677055 |     0.578608 |       0.665338 |  0.736726 |
| recall    |     0.819267 |   0.0763359 |    0.458727 |    0.654    |   0.677055 |     0.502083 |       0.677055 |  0.736726 |
| f1-score  |     0.776875 |   0.127877  |    0.486186 |    0.659422 |   0.677055 |     0.51259  |       0.66722  |  0.736726 |
| support   | 10391        | 655         | 3913        | 9974        |   0.677055 | 24933        |   24933        |  0.736726 |


## Confusion matrix
|              |   Predicted as 1 |   Predicted as 2 |   Predicted as 3 |   Predicted as 4 |
|:-------------|-----------------:|-----------------:|-----------------:|-----------------:|
| Labeled as 1 |             8513 |                4 |              313 |             1561 |
| Labeled as 2 |               86 |               50 |              382 |              137 |
| Labeled as 3 |              473 |               56 |             1795 |             1589 |
| Labeled as 4 |             2453 |               17 |              981 |             6523 |

## Learning curves
![Learning curves](learning_curves.png)

[<< Go back](../README.md)
