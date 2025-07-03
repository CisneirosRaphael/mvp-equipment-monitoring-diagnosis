from pydantic import BaseModel

class ErrorSchema(BaseModel):
    """ Defines how the error message is shown
    """
    message: str
