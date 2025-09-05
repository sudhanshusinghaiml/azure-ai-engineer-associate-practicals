from azure.ai.anomalydetector import AnomalyDetectorClient
from azure.ai.anomalydetector.models import *
from azure.core.credentials import AzureKeyCredential
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

API_KEY = os.environ['ANOMALY_DETECTOR_API_KEY']
ENDPOINT = os.environ['ANOMALY_DETECTOR_ENDPOINT']
DATA_PATH = "REPLACE_WITH_YOUR_LOCAL_SAMPLE_REQUEST_DATA_PATH" #example: c:\\test\\request-data.csv

client = AnomalyDetectorClient(ENDPOINT, AzureKeyCredential(API_KEY))

series = []
data_file = pd.read_csv(DATA_PATH, header=None, encoding='utf-8', date_parser=[0])
for index, row in data_file.iterrows():
    series.append(TimeSeriesPoint(timestamp=row[0], value=row[1]))

request = UnivariateDetectionOptions(series=series, granularity=TimeGranularity.DAILY)

change_point_response = client.detect_univariate_change_point(request)
anomaly_response = client.detect_univariate_entire_series(request)

for i in range(len(data_file.values)):
    temp_date_to_num = mdates.date2num(data_file.values[i])
    date= temp_date_to_num[0]
    if (change_point_response.is_change_point[i]):
        plt.plot(date,data_file.values[i][1], 's', color ='blue')
        print("Change point detected at index: "+ str(i))
    elif (anomaly_response.is_anomaly[i]):
        plt.plot(date,data_file.values[i][1], '^', color="red")
        print("Anomaly detected at index:      "+ str(i))
    else:
        plt.plot(date,data_file.values[i][1], 'o', color ='green')
plt.show()