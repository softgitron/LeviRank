from reranking.reranker import Reranker
from indexing.hit import Hit
import subprocess
import shutil
import pickle
import os


class MonoT5Reranker(Reranker):
    def rerank(self, query: str, hit_list: list[Hit]) -> list[Hit]:
        # Open new special python process and pass the dump
        pipenv_location = shutil.which('pipenv')
        special_working_directory = os.path.abspath(
            "./src/special_environments/t5_reranker")
        custom_environment_variables = os.environ.copy()
        custom_environment_variables["PIPENV_IGNORE_VIRTUALENVS"] = "1"
        custom_environment_variables["PYTHONPATH"] = os.path.abspath("./src")
        child = subprocess.Popen([pipenv_location, "run", "python", "./mono_t5_reranker.py"],
                                 stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 env=custom_environment_variables, cwd=special_working_directory)

        # Pack everything to be send to special environment
        pickle.dump((query, hit_list), child.stdin)
        child.stdin.close()

        # Convert output to normal list again
        output = pickle.load(child.stdout)

        return output
