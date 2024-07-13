import time
import subprocess
from multiprocessing import Process
from common.repositories.SubmissionService import SubmissionService
import socket
import traceback
from models.models import ValidationResultModel
import sys
import http.server
import socketserver
import logging

logging.basicConfig(
    level=logging.INFO,
    format="SERVICE %(levelname)s: %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class CodeValidatorService:

    def __init__(self) -> None:
        self.supportedLanguages = ["html"]

    def handle_validation(self, submission_type, question_id, submission_id, raw_string):
        try:
            # handler = getattr(self, f"handle_{submission_type}")(raw_string, question_id)
            if submission_type.lower() not in self.supportedLanguages:
                return

            if submission_type == "html":
                validationOutcome = self.handle_html(raw_string, question_id)
                
            return validationOutcome
        
        except Exception as e:
            # self.handle_unsupported
            logger.error("Unexpected Exception at CodeValidatorService.handle_validation: ", exc_info=True)
            raise
        

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
                [sys.executable, f"src/validation_scripts/{question_id}.py", str(port)], 
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            logger.info("serving at port %d", port)
            logger.info("DEBUG: Return code: %d", result.returncode)
            logger.info("DEBUG: Standard Output: %s", result.stdout)
            logger.info("DEBUG: Standard Error: %s", result.stderr)

            if result.returncode == 0:
                isCorrectAnswer = True
            else:
                errorStackTrace = result.stderr
                
            stdOut = result.stdout
            logs = str(stdOut).split("--")

            return ValidationResultModel(
                status="processed",
                isCorrectAnswer=isCorrectAnswer,
                errorStackTrace=errorStackTrace,
                logs=logs
            )
        except Exception as e:
            logger.error(f"Exception during validation", exc_info=True)
            traceback.print_exc()
        finally:
            logger.info("Stopping the HTTP server")
            p.terminate()
            # p.join()
            logger.info("HTTP server stopped")
            

    def handle_unsupported(self):
        logger.info("Unsupported submission type.")


    def start_server(self, port):
        logger.info("starting http server at port: %d", port)
        # subprocess.run(["python3", "-m", "http.server", str(port)])
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", port), handler) as httpd:
            logger.info("serving at port %d", port)
            httpd.serve_forever()

    # def stop_server(self):
    #     if hasattr(self, 'httpd'):
    #         logger.info("stopping http server")
    #         self.httpd.shutdown()
    #         self.httpd.server_close()

    def get_available_port(self):
        """returns an open port so that we do not try to run 2 http servers on the same port"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', 0))
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                return s.getsockname()[1]
        except Exception as e:
            logger.error("Error: unable to get open socket", exc_info=True)
            raise

