from reranking.reranker import Reranker
from indexing.hit import Hit
from indexing.queries import Queries
import constants
import subprocess
import shutil
import pickle
import os

class SpecialEnvironmentHelper:
    special_environment_path: str
    special_environment_binary: str

    def __init__(self, special_environment_path, special_environment_binary):
        self.special_environment_path = special_environment_path
        self.special_environment_binary = special_environment_binary

    def rerank(self, queries: Queries, hit_list: list[Hit]) -> list[Hit]:
        # Open new special python process and pass the dump
        pipenv_location = shutil.which('pipenv')
        special_working_directory = os.path.abspath(self.special_environment_path)
        custom_environment_variables = os.environ.copy()
        custom_environment_variables["PIPENV_IGNORE_VIRTUALENVS"] = "1"
        custom_environment_variables["PYTHONPATH"] = os.path.abspath("./src")
        custom_environment_variables["HF_DATASETS_OFFLINE"] = "1"
        custom_environment_variables["TRANSFORMERS_OFFLINE"] = "1"
        if constants.DEBUG:
            stderr = subprocess.STD_ERROR_HANDLE
        else:
            stderr = subprocess.DEVNULL
        child = subprocess.Popen([pipenv_location, "run", "python", self.special_environment_binary],
                                 stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr,
                                 env=custom_environment_variables, cwd=special_working_directory)

        # Pack everything to be send to special environment
        pickle.dump((queries, hit_list), child.stdin)
        child.stdin.close()

        # Very hacky! Initialization may cause some trash to stdout
        # Flush stdout and try again.
        for attempt in range(1000):
            try:
                # Convert output to normal list again
                output = pickle.load(child.stdout)
                child.stdout.close()
                break
            except:
                child.stdout.readline()

        return output
