import os

from dagster_aws.s3 import S3PickleIOManager, S3Resource
from dagster import (
    FilesystemIOManager,
    define_asset_job,
    ScheduleDefinition,
    Definitions,
    AssetSelection
)
from rss_ingestion.assets import rss_feed

resource_defs = {
    "local": {
        "io_manager": FilesystemIOManager(
            base_dir="data",
        ),
    },
    "production": {
        "io_manager": S3PickleIOManager(s3_resource=S3Resource(), s3_bucket="ingestion-data"),
    },
}
deployment_name = os.getenv("DAGSTER_DEPLOYMENT", "local")

rss_ingestion_job = define_asset_job("rss_ingestion_job", selection=AssetSelection.all())

rss_schedule = ScheduleDefinition(
    job=rss_ingestion_job,
    cron_schedule="0 * * * *",  # every hour
)

defs = Definitions(
    assets=[rss_feed],
    schedules=[rss_schedule],
    resources=resource_defs[deployment_name],
)
