#Requirements pip3 install -U pandas matplotlib scikit-learn
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Load the data into a pandas DataFrame
df = pd.read_csv("https://raw.githubusercontent.com/datasets/bitcoin/master/data/bitcoin.csv")

# Convert the date column to a datetime type
df['Date'] = pd.to_datetime(df['Date'])

# Set the date column as the index
df = df.set_index('Date')

# Create a training set consisting of the first 80% of the data
training_set = df[:int(len(df)*0.8)]

# Create a test set consisting of the remaining 20% of the data
test_set = df[int(len(df)*0.8):]

# Fit a linear regression model to the training set
regressor = LinearRegression()
regressor.fit(training_set.index.to_julian_date().values.reshape(-1, 1), training_set['Price'].values.reshape(-1, 1))

# Use the trained model to make predictions on the test set
predictions = regressor.predict(test_set.index.to_julian_date().values.reshape(-1, 1))

# Plot the actual and predicted prices
plt.plot(test_set.index, test_set['Price'], color='red', label='Actual Price')
plt.plot(test_set.index, predictions, color='blue', label='Predicted Price')
plt.title('Bitcoin Price Prediction')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.show()
