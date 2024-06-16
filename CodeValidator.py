import time
import subprocess
from multiprocessing import Process

class CodeValidator:
    def validate_HTML_CSS_JS_Code(self, srcDoc):
        """checks if code has invalid syntax"""
        with open("index.html", "w") as infile:
            infile.write(srcDoc)

        p = Process(target=self.start_server)
        p.start()
        time.sleep(3)

        result = subprocess.run(
            ["env/bin/python", "test_script.py"], 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(result)

        p.terminate()
        p.join()

        if result.returncode == 1:
            return {
                "isCorrectSolution" : False,
                "error_message" : result.stderr
            }
        return { "isCorrectSolution": True } 

    def start_server(self):
        print("starting server")
        subprocess.run(["python3", "-m", "http.server"])
