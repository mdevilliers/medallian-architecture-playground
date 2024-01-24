from dagster import op, graph, repository, sensor
from dagster import daily_partitioned_config
from dagster import RunRequest, SkipReason
from datetime import datetime
from dagster_aws.s3 import s3_pickle_io_manager, s3_resource
from dagster_aws.s3.sensor import get_s3_keys
from dagster_k8s import k8s_job_executor


@op(config_schema={"date": str, "file_path": str})
def process_data(context):
    date = context.op_config["date"]
    filez = context.op_config["file_path"]
    context.log.info(f"processing data for {date} or file path {filez}")


@daily_partitioned_config(start_date=datetime(2021, 6, 1))
def my_partitioned_config(start: datetime, _end: datetime):
    return {
        "ops": {
            "process_data": {
                "config": {
                    "date": start.strftime("%Y-%m-%d")},
                    "file": "unknown",
                },
            },
        "resources": {
            "io_manager": {
                "config": {
                    "s3_bucket": "dagster-data"
                },
            },
            "s3": {
                "config": {
                    "endpoint_url": "http://minio.minio.svc.cluster.local:9000",
                    "region_name": "us-east-1"
                },
            },
        },
    }


@graph
def example_graph():
    process_data()


step_isolated_job = example_graph.to_job(
    name="step_isolated_job",
    resource_defs={"s3": s3_resource, "io_manager": s3_pickle_io_manager},
    executor_def=k8s_job_executor,
    config=my_partitioned_config,
)


@sensor(job=step_isolated_job)
def s3_upload_sensor(context):
    bucket = "project-example-data"

    new_s3_keys = get_s3_keys(bucket, since_key=context.last_run_key)
    if not new_s3_keys:
        yield SkipReason(f"No s3 updates found for bucket {bucket}.")
        return

    for s3_key in new_s3_keys:
        yield RunRequest(
            run_key=s3_key,
            run_config={
                "ops": {
                    "process_data": {
                        "config": {
                            "date": "unknown",
                            "file": s3_key,
                        },
                    },
                "resources": {
                    "io_manager": {
                        "config": {
                            "s3_bucket": "dagster-data"
                        },
                    },
                    "s3": {
                        "config": {
                            "endpoint_url": "http://minio.minio.svc.cluster.local:9000",
                            "region_name": "us-east-1"
                        },
                    },
                },
              },
            }
        )


@repository
def example_repo():
    return [step_isolated_job, s3_upload_sensor]
