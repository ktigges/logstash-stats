# logstash-stats.py

Simple script to show how you might poll the logstash API to monitor or obtain statistics from the logstash node

Python is required

The modules required at this time are:

===== Requirements.txt =====
certifi==2024.12.14
charset-normalizer==3.4.1
idna==3.10
prettytable==3.12.0
requests==2.32.3
urllib3==2.3.0
wcwidth==0.2.13


To install the requirements, pip install -r requirements.txt 

Takes 3 parameters

IP/Hostname of the Logstash Node
Logstash API Port 
time increment for refreshing statistics

ex:

python logstash-stats.py 10.1.1.1 9600 5

Sample Output:


Logstash Host: logstash
Logstash Version: 8.17.0
Status: green
Pipeline: main
Events:
  Duration (ms): 6628365
  Queue Push Duration (ms): 1329
  In: 114671
  Filtered: 114671
  Out: 114671

--- Flow Stats ---
+----------+----------------+---------------+------------------+-------------------+--------------+-------------+
| Pipeline | Event Duration | Push Duration | Input Throughput | Output Throughput | Backpressure | Utilization |
+----------+----------------+---------------+------------------+-------------------+--------------+-------------+
| main     | 6628365        | 1329          | 0.1678           | 0.1678            | 0.0          | 1.59        |
+----------+----------------+---------------+------------------+-------------------+--------------+-------------+

