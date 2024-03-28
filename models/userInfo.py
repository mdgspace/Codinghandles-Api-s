from dataclasses import dataclass

@dataclass
class CodeforceUserInfo:
    handle: str 
    rating: int
    maxRating: int 
    status: str


@dataclass
class CodeshefUserInfo:
    handle: str 
    rating: int 
    maxRating: int 
    stars: int 
    status: str