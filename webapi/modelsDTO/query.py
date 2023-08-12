from typing import Dict, List, Union
from dataclasses import dataclass

@dataclass
class QueryDTO:
    username: str
    email:str = None
    query:str
    user_id:str
    sended_at:str = None