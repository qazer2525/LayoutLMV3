from huggingface_hub import login
from dotenv import dotenv_values
config = dotenv_values(".env")
login(token = config["HUGGINGFACE_TOKEN"], add_to_git_credential=True, write_permission=True)