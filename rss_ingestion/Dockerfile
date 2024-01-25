ARG BASE_IMAGE
FROM "${BASE_IMAGE}"

ARG DAGSTER_VERSION
ARG DAGSTER_LIBS_VERSION

RUN \
       apt-get update -yqq \
    && apt-get install -yqq cron \
    && pip install \
        dagster==${DAGSTER_VERSION} \
        dagster-deltalake==${DAGSTER_LIBS_VERSION} \
        dagster-deltalake-pandas==${DAGSTER_LIBS_VERSION} \
        dagster-aws==${DAGSTER_LIBS_VERSION} \
        dagster-k8s==${DAGSTER_LIBS_VERSION} \
        dagster-postgres==${DAGSTER_LIBS_VERSION} 

COPY . /rss_ingestion
