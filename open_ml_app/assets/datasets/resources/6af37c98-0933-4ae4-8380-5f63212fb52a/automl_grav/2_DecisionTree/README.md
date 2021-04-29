# Summary of 2_DecisionTree

[<< Go back](../README.md)


## Decision Tree
- **n_jobs**: -1
- **criterion**: entropy
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

1.3 seconds

### Metric details
|           |            1 |   2 |           3 |           4 |   accuracy |    macro avg |   weighted avg |   logloss |
|:----------|-------------:|----:|------------:|------------:|-----------:|-------------:|---------------:|----------:|
| precision |     0.663255 |   0 |    0.41997  |    0.590541 |   0.607067 |     0.418441 |       0.578562 |  0.909709 |
| recall    |     0.754595 |   0 |    0.281625 |    0.620914 |   0.607067 |     0.414284 |       0.607067 |  0.909709 |
| f1-score  |     0.705983 |   0 |    0.337158 |    0.605347 |   0.607067 |     0.412122 |       0.589295 |  0.909709 |
| support   | 10391        | 655 | 3913        | 9974        |   0.607067 | 24933        |   24933        |  0.909709 |


## Confusion matrix
|              |   Predicted as 1 |   Predicted as 2 |   Predicted as 3 |   Predicted as 4 |
|:-------------|-----------------:|-----------------:|-----------------:|-----------------:|
| Labeled as 1 |             7841 |                0 |              485 |             2065 |
| Labeled as 2 |              158 |                0 |              243 |              254 |
| Labeled as 3 |              836 |                0 |             1102 |             1975 |
| Labeled as 4 |             2987 |                0 |              794 |             6193 |

## Learning curves
![Learning curves](learning_curves.png)

[<< Go back](../README.md)
