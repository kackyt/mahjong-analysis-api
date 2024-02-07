from typing import Iterator
from google.cloud import bigquery
from google.cloud.bigquery.dataset import DatasetListItem

import api.schemas.dataset as dataset_schema


async def get_datasets() -> list[dataset_schema.Dataset]:
    client = bigquery.Client()
    datasets: Iterator[DatasetListItem] = client.list_datasets()
    return [dataset_schema.Dataset(id=dataset.dataset_id, friendly_name=dataset.friendly_name) for dataset in datasets]
