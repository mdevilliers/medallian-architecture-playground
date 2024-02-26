from dagster import asset
from dagster import (
    HourlyPartitionsDefinition
)

import urllib.request
from datetime import datetime


"""
Download the RSS feed at https://bills.parliament.uk/rss/allbills.rss
Runs every hour and will download RSS files with duplicated data.
Stored
    Locally 
        data/parliament/bills/rss_feed/2024-01-25-15:00
    S3
        Path : dagster/parliament/bills/rss_feed/2024-01-25-14:00
    URI s3://ingestion-data/dagster/parliament/bills/rss_feed
"""

hourly_partitions = HourlyPartitionsDefinition(start_date=datetime(2024, 1, 25))

@asset(
  partitions_def=hourly_partitions,
  key_prefix=["parliament", "bills"],
  )
def rss_feed():
  url = 'https://bills.parliament.uk/rss/allbills.rss'
  response = urllib.request.urlopen(url)
  data = response.read()
  return data
