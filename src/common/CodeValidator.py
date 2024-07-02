import time
import subprocess
from multiprocessing import Process
from common.repositories.submission import SubmissionRepository

class CodeValidator:

    def handle_submission(self, submission_type, question_id, submission_id, raw_string):
        try:
            handler = getattr(self, f"handle_{submission_type}")(raw_string, question_id)
        except AttributeError:
            handler = self.handle_unsupported
        
        print(handler)

    def handle_html(self, raw_string, question_id):
        with open("index.html", "w") as infile:
            infile.write(raw_string)

        p = Process(target=self.start_server)
        p.start()
        time.sleep(5)

        result = subprocess.run(
            ["env/bin/python", f"src/validation_scripts/{question_id}.py"], 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        p.terminate()
        return result.returncode
    
    def handle_unsupported(self):
        pass


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
