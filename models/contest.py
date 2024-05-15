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


@dataclass
class LeetcodeContestInfo:
    name: str 
    time: int

@dataclass
class InterviewbitContestInfo:
    name: str 
    time: int 
    length: int