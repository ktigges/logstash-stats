

# Author.....: Kevin Tigges
# Script Name: logstash-stats.py
# Desc.......: Script to query logstash api and print statistics about each pipeline
#              Feel free to modify as needed .              
#
# Modules required:
#     certifi==2024.12.14
#     charset-normalizer==3.4.1
#     idna==3.10
#     prettytable==3.12.0
#     requests==2.32.3
#     urllib3==2.3.0
#     wcwidth==0.2.13
#
# Last Updates: 12/31/2024
# v001
#
# Note: This uses unsecure and unauthenticated API calls, and is only shown as an example of how you might do this in production.
#       It is highly recommended that you enable authentcation and TLS for production environments.

import requests
import json
import time
from os import system, name
import argparse
# enable pdb for debugging if needed
# import pdb
import urllib3
from prettytable import PrettyTable


urllib3.disable_warnings()


def main(stash_host, stash_port, interval):
  
   #build URL - This is unsecure as mentioned above
   apiurl = f'http://{stash_host}:{stash_port}/_node/stats/pipelines'
   while True:
      response = requests.get(apiurl, verify=False)
      if response.status_code != 200 :
         print(f"Error running API Call - {response.status_code}")
         exit()
      print_stats(response)
      time.sleep(interval)

def clear():
    # Clears the screen
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def print_stats(response):
   clear()
   jsondata = json.loads(response.content)
   # Get and print some basic info
   status = jsondata["status"]
   host = jsondata["host"]
   version = jsondata["version"]
   print(f'Logstash Host: {host}')
   print(f'Logstash Version: {version}')
   print(f'Status: {status}')
   # create the output table and headers
   out_table = PrettyTable()
   out_table.field_names = ["Pipeline", "Event Duration", "Push Duration", "Input Throughput", "Output Throughput", "Backpressure", "Utilization"]
   out_table.max_width = 10
   out_table.align = "l"
   # load in the pipelines section of the json blob
   pipelines = jsondata['pipelines']
   for pipeline_name, pipeline_data in pipelines.items():
      # For each pipeline, gather the statistics
      events = pipeline_data.get('events', {})
      print(f"Pipeline: {pipeline_name}")
      print("Events:")
      print(f"  Duration (ms): {events.get('duration_in_millis', 'N/A')}")
      print(f"  Queue Push Duration (ms): {events.get('queue_push_duration_in_millis', 'N/A')}")
      print(f"  In: {events.get('in', 'N/A')}")
      print(f"  Filtered: {events.get('filtered', 'N/A')}")
      print(f"  Out: {events.get('out', 'N/A')}")
      print("\n--- Flow Stats ---")
      # for each flow, capture the stats
      flow = pipeline_data.get('flow', {})
      # Extract the relevant data for the current pipeline
      event_duration = events.get("duration_in_millis", "N/A")
      queue_push_duration = events.get("queue_push_duration_in_millis", "N/A")
      input_throughput = flow.get("input_throughput", {}).get("current", "N/A")
      output_throughput = flow.get("output_throughput", {}).get("current", "N/A")
      queue_backpressure = flow.get("queue_backpressure", {}).get("current", "N/A")
      worker_utilization = flow.get("worker_utilization", {}).get("current", "N/A")

    # Add the row to the table
      out_table.add_row([pipeline_name, event_duration, queue_push_duration, input_throughput, output_throughput, queue_backpressure, worker_utilization])

   # Print the table
   print(out_table)
   
if __name__ == "__main__":
   # Create the Parser for the command line arguments
   p = argparse.ArgumentParser(description = 'Script to query logstash server and print stats')
   p.add_argument('stash_host', type=str, default="", help="Enter the logstash host IP or DNS name")
   p.add_argument('stash_port', type=str, default="9600", help="Enter the logstash api port (9600 default)")
   p.add_argument('interval', type=int, default=5, help="Enter the interval between polls (5 sec default)")
   args = p.parse_args()
   main(args.stash_host, args.stash_port, args.interval)   
   