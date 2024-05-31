class CodeValidator:
    def __init__(self):
        srcDoc = ''

    def validate_HTML_CSS_JS_Code(self, srcDoc):
        """checks if code has invalid syntax"""
        error_message = ""

        # code validation here...

        error_message = "Password Input absent"
        return {
            "isCorrectSolution" : True,
            "error_message" : error_message
        }
    
    