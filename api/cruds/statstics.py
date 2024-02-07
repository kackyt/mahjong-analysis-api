from google.cloud import bigquery
from datetime import date

import api.schemas.statistics as statistics_schema


async def get_average_score_by_player(dataset_id: str, start_date: date, end_date: date) -> list[statistics_schema.AverageScore]:
    client = bigquery.Client()
    dataset = client.get_dataset(client.project + "." + dataset_id)
    table_prefix = f"{client.project}.{dataset.dataset_id}"
    query = f"""
        SELECT
            game_players.player_name AS player_name,
            AVG(game_scores.score) AS score,
            AVG(game_scores.point) AS point,
            COUNT(game_scores.game_id) AS game_count
        FROM
            {table_prefix}.game_scores as game_scores
            JOIN {table_prefix}.game_players as game_players ON game_scores.game_id = game_players.game_id
            AND game_scores.player_index = game_players.player_index
        WHERE
            game_scores.dt BETWEEN @start_date AND @end_date
        GROUP BY
            game_players.player_name
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
            bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
        ]
    )
    query_job = client.query(query, job_config=job_config)
    rows = query_job.result()

    return [statistics_schema.AverageScore(**row) for row in rows]


async def get_yaku_count(dataset_id: str, start_date: date, end_date: date) -> list[statistics_schema.YakuCount]:
    client = bigquery.Client()
    dataset = client.get_dataset(client.project + "." + dataset_id)
    table_prefix = f"{client.project}.{dataset.dataset_id}"
    query = f"""
        SELECT
            name,
            SUM(han) AS han_count,
            COUNT(name) AS count
        FROM (
            SELECT
                yakus.element.name AS name,
                yakus.element.han AS han
            FROM
                {table_prefix}.agaris
                CROSS JOIN UNNEST(yaku.list) AS yakus
            WHERE
                dt BETWEEN @start_date AND @end_date
        ) sub
        GROUP BY
            name
        ORDER BY
            count DESC
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
            bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
        ]
    )
    query_job = client.query(query, job_config=job_config)
    rows = query_job.result()

    return [statistics_schema.YakuCount(**row) for row in rows]


async def get_nagare_count(dataset_id: str, start_date: date, end_date: date) -> list[statistics_schema.NagareCount]:
    client = bigquery.Client()
    dataset = client.get_dataset(client.project + "." + dataset_id)
    table_prefix = f"{client.project}.{dataset.dataset_id}"
    query = f"""
        SELECT
            name,
            COUNT(name) AS count
        FROM 
            {table_prefix}.nagares
        WHERE
            dt BETWEEN @start_date AND @end_date
        GROUP BY
            name
        ORDER BY
            count DESC
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
            bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
        ]
    )
    query_job = client.query(query, job_config=job_config)
    rows = query_job.result()

    return [statistics_schema.NagareCount(**row) for row in rows]
