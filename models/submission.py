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


@dataclass
class CodeshefSubmission:
    problemCode: str 
    time: int 
    status: str
    language: str


@dataclass
class LeetcodeACSubmission:
    problemName: str 
    problemSlug: str 
    time: int


@dataclass 
class InterviewbitSubmission:
    count: int
    time: int