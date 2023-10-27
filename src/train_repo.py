from train_source import training_model
from dotenv import dotenv_values
config = dotenv_values("..\\.env")
training_model(starting_repo=config["DEST_REPO"], dest_repo=config["DEST_REPO"], source_repo=config["SOURCE_REPO"])