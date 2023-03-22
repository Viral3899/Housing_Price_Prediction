import sys

def error_message_details(error,error_detail:sys):
    _,_,exc_tb=error_detail.exc_info()
    file_name=exc_tb.tb_frame.f_code.co_filename
    line_no=exc_tb.tb_lineno
    error_message=f"Error Occured in Python Script [{file_name}] line number [{line_no}] error message [{str(error)}]"

    return error_message



class CustomeException(Exception):
    def __init__(self, error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_details(error_message,error_detail=error_message_details)
    
    def __str__(self):
        return self.error_message
