import time
import subprocess
from multiprocessing import Process
from common.repositories.submission import SubmissionRepository

class CodeValidator:
    def validate_HTML_CSS_JS_Code(self, srcDoc, question_id, submission_id):
        """checks if code has invalid syntax"""
        with open("index.html", "w") as infile:
            infile.write(srcDoc)

        p = Process(target=self.start_server)
        p.start()
        time.sleep(3)
        result = subprocess.run(
            ["env/bin/python", f"src/validation_scripts/{question_id}.py"], 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(result)
        p.terminate()
        print("hello world")
        submission_repository = SubmissionRepository()
        if result.returncode == 1:
            submission_repository.updateSubmission(submission_id, "fail")
            return {
                "isCorrectSolution" : False,
                "error_message" : result.stderr
            }
        submission_repository.updateSubmission(submission_id, "success")
        return { "isCorrectSolution": True } 

    def start_server(self):
        print("starting server")
        subprocess.run(["python3", "-m", "http.server"])
