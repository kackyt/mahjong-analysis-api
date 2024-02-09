import asyncio
from google.cloud import bigquery
from datetime import date
from functools import partial

import api.schemas.game as game_schema


async def get_games_count(dataset_id: str, start_date: date, end_date: date) -> int:
    loop = asyncio.get_running_loop()
    client = bigquery.Client()
    dataset = client.get_dataset(client.project + "." + dataset_id)
    table = f"{client.project}.{dataset.dataset_id}.games"
    query = f"""
        SELECT
            COUNT(id)
        FROM
            {table}
        WHERE
            dt BETWEEN @start_date AND @end_date
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
            bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
        ]
    )
    func = partial(client.query_and_wait, query, job_config=job_config)
    rows = await loop.run_in_executor(None, func)

    return 0 if rows is None else next(rows)[0]


async def get_games(dataset_id: str, start_date: date, end_date: date, limit: int, offset: int) -> list[game_schema.Game]:
    loop = asyncio.get_running_loop()
    client = bigquery.Client()
    dataset = client.get_dataset(client.project + "." + dataset_id)
    table = f"{client.project}.{dataset.dataset_id}.games"
    query = f"""
        SELECT
            id,
            tonpu,
            ariari,
            has_aka,
            demo,
            soku,
            level,
            started_at
        FROM
            {table}
        WHERE
            dt BETWEEN @start_date AND @end_date
        LIMIT @limit
        OFFSET @offset
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
            bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
            bigquery.ScalarQueryParameter("limit", "INT64", limit),
            bigquery.ScalarQueryParameter("offset", "INT64", offset),
        ]
    )
    func = partial(client.query_and_wait, query, job_config=job_config)
    rows = await loop.run_in_executor(None, func)
    games = []
    for row in rows:
        games.append(game_schema.Game(**row))
    return games
