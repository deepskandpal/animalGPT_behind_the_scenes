import json
from google.oauth2 import service_account
from google.cloud import bigquery
import random

from  animal_gpt.utils.config import (
    default_bq_cliente_mail,
    default_bq_private_key,
    default_bq_token_uri,
    default_project_id,
    default_dialect,
    default_private_key,
    format_bqprivatekey,
)


class BQ:
    def __init__(self, bq_cliente_mail=default_bq_cliente_mail, bq_private_key=default_bq_private_key,
        bq_token_uri=default_bq_token_uri, project_id=default_project_id, private_key=default_private_key,
        dialect=default_dialect, timeout=60*60):
        if isinstance(bq_cliente_mail, type(None)):
            raise ValueError("Fail to initiate BQ bq_cliente_mail is None")
        if isinstance(bq_token_uri, type(None)):
            raise ValueError("Fail to initiate BQ bq_token_uri is None")
        if isinstance(bq_private_key, type(None)):
            raise ValueError("Fail to initiate BQ bq_private_key is None")

        self.bq_cliente_mail = bq_cliente_mail
        self.bq_private_key = bq_private_key
        self.bq_token_uri = bq_token_uri
        self.project_id = project_id
        self.private_key = private_key
        self.dialect = dialect
        self.timeout = timeout

        self.bqlogin = (
                "{"
                + '"project_id": "'
                + self.project_id
                + '", '
                + '"private_key": "-----BEGIN PRIVATE KEY-----\\n'
                + format_bqprivatekey(self.bq_private_key)
                + '\\n-----END PRIVATE KEY-----\\n", '
                + '"client_email": "'
                + self.bq_cliente_mail
                + '", '
                + '"token_uri": "'
                + self.bq_token_uri
                + '"'
                + "}"
        )       
        try:
            _ = json.loads(self.bqlogin)
        except Exception as e:
            raise e("BQLOGIN must be a valid json string")

        with open(private_key, "wt") as f:
            f.write(self.bqlogin)

        self.credentials = service_account.Credentials.from_service_account_file(self.private_key, )
        self.client = bigquery.Client.from_service_account_json(private_key)

    def read_bq(self, query, col_rename=None, timeout=None):
        timeout = timeout if timeout is not None else self.timeout
        job = self.client.query(query, project=self.project_id)
        df = job.result(timeout=timeout)
        df = df.to_dataframe(create_bqstorage_client=True)
        df.bq_job_id = job._properties['jobReference']['jobId']

        if col_rename is not None:
            if len(col_rename) > 0:
                df.rename(columns=col_rename, inplace=True)
        return df
    
    def to_bq(self, df, table, if_exists="append", retries=0):
        while retries >= 0:
            try:
                return self._to_bq(df, table, if_exists)
            except Exception as e:
                if retries > 0:
                    pass
                else:
                    raise e

            retries -= 1

    def _to_bq(self, df, table, if_exists):
        table_split = table.split(".", 1)
        simple_table = table_split[-1]
        project_id = table_split[0]
        df.to_gbq(
            simple_table,
            project_id=project_id,
            chunksize=None,
            if_exists=if_exists,
            credentials=self.credentials,
            progress_bar=False,
        )
        return True