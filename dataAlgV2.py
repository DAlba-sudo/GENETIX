# This will observe the data found in a population
# 
# Functions include:
# - Create Linear Regression algorithms to control bias of each type of gene
#    * Steps needed to achieve this:
#         - Before creating a linear regression algorithm we first need data
#                  - When creating an individual we need to "rebuild" the LR model 
from linearRegressionAlg import LinearRegression

XVAL = [4512, 3738, 4261, 3777, 4177]
YVAL = [1530, 1297, 1335, 1282, 1590]

LR = LinearRegression(x_values=XVAL, y_values=YVAL)
print(LR.predict(4512))

