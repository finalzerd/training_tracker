

from dataclasses import dataclass, field
from datetime import date
from types import coroutine
from typing import List



@dataclass
class CourseTaker:
    name: str
    email:str
    
    def first_name(self) -> str:
        try:
            return self.name.split(" ")[0].capitalize()
        except:
            return self.name


@dataclass
class Course:
    name: str
    links: List[str]
    login: str
    password: str
    start_date: date
    end_date: date
    taker: CourseTaker
    box_completion: float
    feedback_provided: bool
    is_reschedule: bool
    was_rescheduled: bool
    incomplete_modules: List[str]
    needs_reschedule: bool
    currently_tracking:bool

    def is_complete(self, min_completion:float=0.9) -> bool:
        return self.box_completion > min_completion
             

    def forms_link(self) -> str:
        taker_name: str = self.taker.name.replace("+", "%2B").replace(" ", "+")
        course_name: str = self.name.replace("+", "%2B").replace(" ", "+")
        return f"https://docs.google.com/forms/d/e/1FAIpQLSdwquJZFdCx1c3cPz4OUExO1w8RJL2MbBK56tUildM47zSwBw/viewform?usp=pp_url&entry.1961833826={self.taker.email}&entry.263768831={taker_name}&entry.1892952282={course_name}"
    
    

    
