import sys





class HousingException(Exception):
    
    def __init__(self, error_message:Exception,error_detail:sys):
        super().__init__(error_message)
        self.error_message=HousingException.get_detailed_error_message(error=error_message,error_detail=error_detail)


    @staticmethod
    def get_detailed_error_message(error,error_detail:sys) ->str:
        _,_,exc_tb=error_detail.exc_info()
        file_name=exc_tb.tb_frame.f_code.co_filename
        try_block_line_no=exc_tb.tb_lineno
        EXception_block_line_no=exc_tb.tb_frame.f_lineno
        error_message=f"""
        Error Occured in Python Script : [{file_name}] 
        at try block line number : [{try_block_line_no}]
        and exception block line no : [{EXception_block_line_no}]
        error message : [{str(error)}]
        """

        return error_message
    
    def __str__(self):
        return self.error_message
        
    def __repr__(self) -> str:
        return HousingException.__name__.str()
