from common.database import DatabaseConnector

class SubmissionService():
    def __init__(self):
        self.conn = DatabaseConnector().conn

    def updateSubmission(self, submission_id, result):
        print("updating submissions")
        try:
            with self.conn.cursor() as cur:
                status_to_update = "2b1a2f79-830a-44a3-822f-3d6f75a1afb7"
                match result:
                    case "success":
                        result_to_update = "ab7ee9bd-fc7a-4aab-8adf-afefddc7c561"
                    case "fail":
                        result_to_update = "5e158300-5594-4171-ae4d-a2d603306266"
                    case "error":
                        result_to_update = "a2d50ed8-d404-4ad4-94f0-9bde4f16aecd"
                    case "default":
                        status_to_update = "002aa7db-a589-409a-836e-f351b14a2442"
                        result_to_update = "a2d50ed8-d404-4ad4-94f0-9bde4f16aecd"
                cur.execute("""
                update "frontendLeetcode_submission" set status=(%s), result=(%s)
                where id=(%s)
                """, (status_to_update, result_to_update, submission_id))
                self.conn.commit()
            print("updated submissions")
            return
        except Exception as e:
            print("Error in updating submissions: ", e)
            return