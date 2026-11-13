import logging
import os
from typing import Optional

from azure.cosmos import CosmosClient
from openai import AzureOpenAI

# --- Azure OpenAI Client ---
# Uses API key auth when AOAI_KEY is set (local dev).
# Falls back to AAD token provider if AOAI_KEY is absent (managed identity in production).
AOAI_ENDPOINT = os.getenv("AOAI_ENDPOINT")
AOAI_KEY = os.getenv("AOAI_KEY")
AOAI_API_VERSION = os.getenv("AOAI_API_VERSION", "2025-01-01-preview")

aoai_client: Optional[AzureOpenAI] = None

if AOAI_ENDPOINT and AOAI_KEY:
    # API key authentication (local development + key-based deployments)
    aoai_client = AzureOpenAI(
        api_version=AOAI_API_VERSION,
        azure_endpoint=AOAI_ENDPOINT,
        api_key=AOAI_KEY,
    )
    logging.info("Azure OpenAI client initialized with API key auth.")
elif AOAI_ENDPOINT:
    # AAD / DefaultAzureCredential fallback (production managed identity)
    try:
        from azure.identity import DefaultAzureCredential, get_bearer_token_provider

        credential = DefaultAzureCredential()
        token_provider = get_bearer_token_provider(
            credential, "https://cognitiveservices.azure.com/.default"
        )
        aoai_client = AzureOpenAI(
            api_version=AOAI_API_VERSION,
            azure_endpoint=AOAI_ENDPOINT,
            azure_ad_token_provider=token_provider,
        )
        logging.info("Azure OpenAI client initialized with AAD auth.")
    except Exception as e:
        logging.warning(f"AAD auth failed: {e}. Client unavailable.")
else:
    logging.warning("AOAI_ENDPOINT not set — Azure OpenAI client unavailable.")

# --- Azure Cosmos DB Client ---
cosmos_endpoint = os.getenv("COSMOS_ENDPOINT")
cosmos_key = os.getenv("COSMOS_KEY")

cosmos_client: Optional[CosmosClient] = None
container_client = None

if cosmos_endpoint:
    if "localhost" in cosmos_endpoint:
        cosmos_client = CosmosClient(url=cosmos_endpoint, credential=cosmos_key)
    elif cosmos_key:
        cosmos_client = CosmosClient(url=cosmos_endpoint, credential=cosmos_key)
    else:
        try:
            from azure.identity import DefaultAzureCredential

            cosmos_client = CosmosClient(
                url=cosmos_endpoint, credential=DefaultAzureCredential()
            )
        except Exception as e:
            logging.warning(f"Cosmos AAD auth failed: {e}")

    if cosmos_client:
        db_name = os.getenv("COSMOS_DATABASE_NAME")
        container_name = os.getenv("COSMOS_CONTAINER_NAME")
        if db_name and container_name:
            try:
                database_client = cosmos_client.get_database_client(db_name)
                container_client = database_client.get_container_client(container_name)
            except Exception as e:
                logging.warning(f"Cosmos container init failed: {e}")
        else:
            logging.warning("COSMOS_DATABASE_NAME or COSMOS_CONTAINER_NAME not set.")
else:
    logging.warning("COSMOS_ENDPOINT not set — Cosmos client unavailable.")
