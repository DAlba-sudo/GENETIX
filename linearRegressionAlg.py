import numpy as np

class LinearRegression:
    def __init__(self, complete_dataset=None, x_values=None, y_values=None):
        # x_values => (Integer/Float Array) holds the x values
        # y_values => ((Integer/Float Array) holds the y values)
        # complete_dataset => ([[]]) 2D array holding coordinate values for the items
        self.XDS = []
        self.YDS = []
        self.CDS = []

        self.b0 = 0
        self.b1 = 0


        if(complete_dataset is not None):
            self.CDS = complete_dataset
        elif ((x_values is not None) and (y_values is not None)):
            self.CDS = self.compose_dataset(x_values, y_values)
            self.XDS = x_values
            self.YDS = y_values
        else:
            raise Exception("Unplanned Scenario: no dataset or dataset subset provided.")

        if((x_values is None) and (y_values is None)):
            self.XDS = self.extractValues(DS=self.CDS, index=0)
            self.YDS = self.extractValues(DS=self.CDS, index=1)


        self.x_mean = np.mean(self.XDS)
        self.y_mean = np.mean(self.YDS)

        self.build_model()
    
    
    # creates a two dimensional array containing the dataset's values
    def compose_dataset(self, x_values, y_values):
        if(len(x_values) != len(y_values)):
            raise Exception("The x and y datasets do not have the same amount of data! Please fix.")
        
        tempDS = []
        for DSObj in range(len(x_values)):
            current_x = x_values[DSObj]
            current_y = y_values[DSObj]

            tempDS.append([current_x, current_y])
        
        return tempDS

    # from a complete dataset extracts x and y DS
    def extractValues(self, DS, index):
        tempXY = []
        for itms in range(len(DS)):
            currentObj = DS[itms]
            tempXY.append(currentObj[index])
        
        return tempXY


    def build_model(self):
        # using the formula to calculate the b1 and b0
        numerator = 0
        denominator = 0
        for i in range(len(self.XDS)):
            numerator += (self.XDS[i] - self.x_mean) * (self.YDS[i] - self.y_mean)
            denominator += (self.XDS[i] - self.x_mean) ** 2
            
        self.b1 = numerator / denominator
        self.b0 = self.y_mean - (self.b1 * self.x_mean)

    def predict(self, x):
        return (self.b0 + (self.b1 * x))
        


