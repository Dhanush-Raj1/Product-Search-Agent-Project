import os
import sys

class CustomException(Exception):
    def __init__(self, error_message):
        self.error_message = self._prepare_error_message(error_message)
        super().__init__(self.error_message)

    def _prepare_error_message(self, error_message):
        """
        Prepare a detailed error message with traceback information
        """
        _, _, exc_tb = sys.exc_info()
        
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        
        error_message = f"Error occurred in script: [{file_name}] at line number: [{line_number}] error message: [{error_message}]"
        
        return error_message

    def __str__(self):
        return self.error_message


# try:
#     print(hello)
# except Exception as e:
#     raise CustomException(e)