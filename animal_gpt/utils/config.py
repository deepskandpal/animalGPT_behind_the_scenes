import os


def format_bqprivatekey(key):
    chunks, chunk_size = len(key), 64
    return "\\n".join([key[i: i + chunk_size] for i in range(0, chunks, chunk_size)])


default_bq_cliente_mail = os.getenv("client_email")
default_bq_token_uri    = os.getenv("token_uri")
default_bq_private_key  = os.getenv("private_key")
default_prompt_db = os.getenv("prompt_read_table")
default_logs_db = os.getenv("default_logs_db")
default_project_id = os.getenv("project_id")
default_private_key = "bq_private_key.json"
default_dialect  = "standard"

#######Queries#########
read_prompts = f'''SELECT * FROM `{default_prompt_db}`'''



