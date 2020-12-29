## MVP versions
The comparison across different MVP versions in terms of data and features used is listed in the table below.

| Version | Data | Feature |
| ---- | ---- | ---- | 
| 1.1 | Daily Mail articles which have more than 10% of economic themes | Average `tone` column from GDELT database |
| 1.2 | Daily Mail articles (money/markets section) | Average `tone` column from GDELT database  |
| 2.1 | Daily Mail articles (money/markets section) | Term frequency of n-grams |
| 2.2 | Daily Mail articles (money/markets section) | Pre-defined vocabulary |
| 3.1 | Bloomberg TV News | Pre-defined vocabulary |

The `compare_performance` notebook shows the improvement of MVP v3.1 model (relative to baseline AR(1) model)
for 3 different target variables across different forecast horizons.

There is a significant improvement in forecasting 3M-on-3M GDP change for 1, 2 and 3 months horizon.