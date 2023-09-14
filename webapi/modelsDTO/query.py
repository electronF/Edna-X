from typing import Dict, List, Union
from dataclasses import dataclass

@dataclass
class QueryDTO:
    username: str
    query:str
    user_id:str
    email:str = None
    sended_at:str = None