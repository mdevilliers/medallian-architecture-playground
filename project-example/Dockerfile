ARG BASE_IMAGE
FROM "${BASE_IMAGE}"

ARG DAGSTER_VERSION
ARG DAGSTER_LIBS_VERSION

# ==> Add Dagster layer
RUN \
# Cron
       apt-get update -yqq \
    && apt-get install -yqq cron \
# Dagster
    && pip install \
        dagster==${DAGSTER_VERSION} \
        dagster-aws==${DAGSTER_LIBS_VERSION} \
        dagster-k8s==${DAGSTER_LIBS_VERSION} \
        dagster-postgres==${DAGSTER_LIBS_VERSION} 

# ==> Add user code layer
# Example pipelines
COPY ./ /project-example
