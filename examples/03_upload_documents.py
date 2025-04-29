# examples/03_upload_documents.py

import os
import sys
import json
import logging # Import logging module
from moorcheh_sdk import (
    MoorchehClient,
    MoorchehError,
    AuthenticationError,
    InvalidInputError,
    NamespaceNotFound,
    APIError,
)

# --- Configure Logging ---
# Set up basic configuration for logging
logging.basicConfig(
    level=logging.INFO, # Set the minimum level to capture (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
# Get a logger for this specific script
logger = logging.getLogger(__name__)
# -------------------------

def main():
    """
    Example script to upload documents to a text namespace using the SDK, with logging.
    """
    logger.info("--- Moorcheh SDK: Upload Documents Example ---")

    # 1. Initialize the Client
    try:
        # Client initialization will log its base URL (at INFO level)
        client = MoorchehClient()
        logger.info("Client initialized successfully.")
    except AuthenticationError as e:
        logger.error(f"Authentication Error: {e}")
        logger.error("Please ensure the MOORCHEH_API_KEY environment variable is set correctly.")
        sys.exit(1)
    except MoorchehError as e:
        logger.error(f"Error initializing client: {e}", exc_info=True) # Log full traceback
        sys.exit(1)

    # 2. Define Target Namespace and Documents to Upload
    target_namespace = "sdk-test-text-ns-01" # Use the text namespace created earlier

    documents_to_upload = [
        {
            "id": "sdk-doc-001", # Unique ID for this chunk
            "text": "The Moorcheh Python SDK simplifies API interactions.",
            "source": "sdk_example_03",
            "version": 1.0
        },
        {
            "id": "sdk-doc-002",
            "text": "Uploading documents involves sending a list of dictionaries.",
            "source": "sdk_example_03",
            "topic": "ingestion"
        },
        {
            "id": "sdk-doc-003",
            "text": "Each document needs a unique ID and text content. Metadata is optional but useful.",
            "source": "sdk_example_03",
            "topic": "data_format"
        }
    ]

    logger.info(f"Attempting to upload {len(documents_to_upload)} documents to namespace: '{target_namespace}'")

    # 3. Call the upload_documents method
    try:
        # Use the client's context manager
        with client:
            # SDK method call will produce its own logs
            response = client.upload_documents(
                namespace_name=target_namespace,
                documents=documents_to_upload
            )
            logger.info("--- API Response (Should be 202 Accepted) ---")
            # Use json.dumps for pretty printing the response dict in the log
            logger.info(json.dumps(response, indent=2))
            logger.info("--------------------------------------------")
            if response.get('status') == 'queued':
                submitted_count = len(response.get('submitted_ids', []))
                logger.info(f"Successfully queued {submitted_count} documents for processing! ✅")
            else:
                logger.warning(f"Upload request sent, but status was not 'queued'. Status: {response.get('status')}. Check response details.")


    # 4. Handle Specific Errors using logger.error or logger.exception
    except NamespaceNotFound as e:
         logger.error(f"Namespace '{target_namespace}' not found.")
         logger.error(f"API Message: {e}")
    except InvalidInputError as e:
        logger.error("Invalid input provided for document upload.")
        logger.error(f"API Message: {e}")
    except AuthenticationError as e:
        logger.error("Authentication failed during document upload.")
        logger.error(f"API Message: {e}")
    except APIError as e:
        # Log the full traceback for unexpected API errors
        logger.exception("An API error occurred during document upload.")
    except MoorchehError as e: # Catch base SDK or network errors
        # Log the full traceback for SDK/network errors
        logger.exception("An SDK or network error occurred.")
    except Exception as e: # Catch any other unexpected errors
        # Log the full traceback for any other errors
        logger.exception("An unexpected error occurred.")

if __name__ == "__main__":
    main()
