from dataclasses import dataclass

@dataclass
class CodeforcesContestInfo:
    name: str
    length: str
    time: int 


@dataclass
class CodeshefContestInfo:
    name: str
    code: str
    length: int 
    time: int