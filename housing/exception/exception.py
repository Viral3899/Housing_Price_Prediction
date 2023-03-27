import sys

def error_message_detail(error,error_detail:sys):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    try_block_line_no = exc_tb.tb_lineno
    Exception_block_line_no = exc_tb.tb_frame.f_lineno
    error_message = f"""Python Script :
    [{file_name}] 
    at try block line number : [{try_block_line_no}] and exception block line no : [{Exception_block_line_no}] 
    error message : 
    [{str(error)}]
    """
    return error_message


class HousingException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail=error_detail)

    def __str__(self):
        return self.error_message

    def __str__(self):
        return self.error_message

    def __repr__(self) -> str:
        return HousingException.__name__.str()
