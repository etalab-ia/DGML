# Summary of 5_Default_RandomForest

[<< Go back](../README.md)


## Random Forest
- **criterion**: gini
- **max_features**: 0.9
- **min_samples_split**: 30
- **max_depth**: 4
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

15.6 seconds

### Metric details
|           |            1 |    2 |           3 |            4 |   accuracy |    macro avg |   weighted avg |   logloss |
|:----------|-------------:|-----:|------------:|-------------:|-----------:|-------------:|---------------:|----------:|
| precision |     0.607326 |    0 |    0.511325 |     0.597158 |    0.60077 |     0.428952 |       0.577426 |  0.888669 |
| recall    |     0.828565 |    0 |    0.117582 |     0.537089 |    0.60077 |     0.370809 |       0.60077  |  0.888669 |
| f1-score  |     0.700902 |    0 |    0.191197 |     0.565533 |    0.60077 |     0.364408 |       0.564368 |  0.888669 |
| support   | 21390        | 1024 | 6336        | 18779        |    0.60077 | 47529        |   47529        |  0.888669 |


## Confusion matrix
|              |   Predicted as 1 |   Predicted as 2 |   Predicted as 3 |   Predicted as 4 |
|:-------------|-----------------:|-----------------:|-----------------:|-----------------:|
| Labeled as 1 |            17723 |                0 |              138 |             3529 |
| Labeled as 2 |              523 |                0 |              134 |              367 |
| Labeled as 3 |             2683 |                0 |              745 |             2908 |
| Labeled as 4 |             8253 |                0 |              440 |            10086 |

## Learning curves
![Learning curves](learning_curves.png)

[<< Go back](../README.md)
