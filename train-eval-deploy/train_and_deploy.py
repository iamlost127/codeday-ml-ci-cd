import logging
import os
import sys

from azure.storage.blob import BlobServiceClient
from training import ModelTraining


AZURE_CONTAINER_NAME = 'codeday-ml-ci-cd'
LOGGER = logging.getLogger(__name__)


def _upload_file_to_azure(azure_blob_key, file_path):
    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=AZURE_CONTAINER_NAME, blob=azure_blob_key)

    with open(file_path, 'rb') as f:
        blob_client.upload_blob(f)

    LOGGER.info('Model successfully uploaded')


def main():
    model_training = ModelTraining()
    model, val_score = model_training.train()

    if model_training.evaluate_model(val_score):
        model_file_path = model_training.save_model(model)
        model_name = model_file_path.split('/')[-1]

        LOGGER.info('Model evaluation passed, uploading new model version: {}'.format(model_name))
        _upload_file_to_azure('models/' + model_name, model_file_path)
        os.remove(model_file_path)
    else:
        LOGGER.info('Model evaluation failed, skip model upload, val score: {}'.format(val_score))


if __name__ == '__main__':
    main()
    sys.exit()
