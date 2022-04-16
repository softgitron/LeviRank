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
        if constants.DEBUG:
            stderr = None
        else:
            stderr = subprocess.DEVNULL
        child = subprocess.Popen([pipenv_location, "run", "python", self.special_environment_binary],
                                 stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr,
                                 env=custom_environment_variables, cwd=special_working_directory)

        # Pack everything to be send to special environment
        pickle.dump((queries, hit_list), child.stdin)
        child.stdin.close()

        # Convert output to normal list again
        output = pickle.load(child.stdout)
        child.stdout.close()

        return output
