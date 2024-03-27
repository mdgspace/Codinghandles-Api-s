from dataclasses import dataclass


@dataclass
class CodeforcesSubmission:
    problemCode: str 
    problemName: str 
    time: int 
    language: str 
    status: str 
    timeConsumed: str 
    spaceConsumed: str 
