from pydantic import BaseModel


class Data(BaseModel):
    name: str
    description: str
