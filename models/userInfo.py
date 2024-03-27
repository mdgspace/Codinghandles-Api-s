from dataclasses import dataclass

@dataclass
class CodeforceUserInfo:
    handle: str 
    rating: int
    maxRating: int 
    status: str