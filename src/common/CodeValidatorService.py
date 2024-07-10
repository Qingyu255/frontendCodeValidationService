import time
import subprocess
from multiprocessing import Process
from common.repositories.SubmissionService import SubmissionService
import socket
import traceback
from models.models import ValidationResultModel

class CodeValidatorService:

    def __init__(self) -> None:
        self.supportedLanguages = ["html"]

    def handle_submission(self, submission_type, question_id, submission_id, raw_string):
        try:
            # handler = getattr(self, f"handle_{submission_type}")(raw_string, question_id)
            if submission_type.lower() not in self.supportedLanguages:
                return

            if submission_type == "html":
                validationOutcome = self.handle_html(raw_string, question_id)
                
            return validationOutcome
        
        except AttributeError:
            self.handle_unsupported
        
        return 1 # fail

    def handle_html(self, raw_string, question_id):
        with open("index.html", "w") as infile:
            infile.write(raw_string)

        port = self.get_available_port()
        p = Process(target=self.start_server, args=((port, )))
        p.start()
        time.sleep(5)

        isCorrectAnswer = False
        stdOut = "stdOut"
        errorStackTrace = ""
        try:
            result = subprocess.run(
                ["env/bin/python", f"src/validation_scripts/{question_id}.py", str(port)], 
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print("DEBUG: Return code:", result.returncode) # returncode == 0 means no exceptions raised(pass), returncode == 1 means exception raised(fail)
            print("DEBUG: Standard Output:", result.stdout)
            print("DEBUG: Standard Error:", result.stderr)

            if result.returncode == 0:
                isCorrectAnswer = True
            else:
                errorStackTrace = result.stderr
                
            stdOut = result.stdout
            logs = str(stdOut).split("--")

            return ValidationResultModel(
                isCorrectAnswer=isCorrectAnswer,
                errorStackTrace=errorStackTrace,
                logs=logs
            )
        except Exception as e:
            traceback.print_exc()
        finally:
            p.terminate()
            p.join()
            
    
    def handle_unsupported(self):
        print("Unsupported submission type.")


    def start_server(self, port):
        print("starting http server at port: " + str(port))
        subprocess.run(["python3", "-m", "http.server", str(port)])

    def get_available_port(self):
        """returns an open port so that we do not try to run 2 http servers on the same port"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]
