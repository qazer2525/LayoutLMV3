import uuid
from train_source import training_model
from dotenv import dotenv_values
config = dotenv_values("..\\.env")
dest_repo = f"model-{uuid.uuid1()}"
training_model(starting_repo=config["STARTING_REPO"], dest_repo=dest_repo, source_repo=config["SOURCE_REPO"])