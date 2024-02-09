import asyncio
from google.cloud import bigquery
from datetime import date
from functools import partial

import api.schemas.kyoku as kyoku_schema


async def get_kyokus_count(dataset_id: str, start_date: date, end_date: date, game_id: str | None) -> int:
    loop = asyncio.get_running_loop()
    client = bigquery.Client()
    dataset = client.get_dataset(client.project + "." + dataset_id)
    table = f"{client.project}.{dataset.dataset_id}.kyokus"
    query = f"""
        SELECT
            COUNT(id)
        FROM
            {table}
        WHERE
            dt BETWEEN @start_date AND @end_date
    """

    params = [
        bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
        bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
    ]

    if game_id is not None:
        query += " AND game_id = @game_id"
        params.append(bigquery.ScalarQueryParameter("game_id", "STRING", game_id))

    job_config = bigquery.QueryJobConfig(query_parameters=params)
    func = partial(client.query_and_wait, query, job_config=job_config)
    rows = await loop.run_in_executor(None, func)

    return 0 if rows is None else next(rows)[0]


async def get_kyokus(
    dataset_id: str,
    start_date: date,
    end_date: date,
    limit: int,
    offset: int,
    game_id: str | None,
) -> list[kyoku_schema.Kyoku]:
    loop = asyncio.get_running_loop()
    client = bigquery.Client()
    dataset = client.get_dataset(client.project + "." + dataset_id)
    table = f"{client.project}.{dataset.dataset_id}.kyokus"

    params = [
        bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
        bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
        bigquery.ScalarQueryParameter("limit", "INT64", limit),
        bigquery.ScalarQueryParameter("offset", "INT64", offset),
    ]

    if game_id is not None:
        cond_game_id = " AND game_id = @game_id"
        params.append(bigquery.ScalarQueryParameter("game_id", "STRING", game_id))
    else:
        cond_game_id = ""

    query = f"""
        SELECT
            id,
            game_id,
            kyoku_num,
            honba,
            reachbou,
            scores,
            kazes
        FROM
            {table}
        WHERE
            dt BETWEEN @start_date AND @end_date
            {cond_game_id}
        LIMIT @limit
        OFFSET @offset
    """

    job_config = bigquery.QueryJobConfig(query_parameters=params)
    func = partial(client.query_and_wait, query, job_config=job_config)
    rows = await loop.run_in_executor(None, func)
    kyokus = []
    for row in rows:
        kyokus.append(kyoku_schema.Kyoku(**row))

    return kyokus
