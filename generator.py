from models import Course, Section
from scheduler import is_valid, section_conflicts_with_schedule
from optimizer import calculate_total_score

def find_all_schedules(courses: list[Course]) -> list[list[Section]]:
    all_valid_schedules = []
    
    def backtrack(course_index: int, current_schedule: list[Section]):
        if course_index == len(courses):
            all_valid_schedules.append(list(current_schedule))
            return
        
        target_course = courses[course_index]
        for section in target_course.sections:
            if is_valid(section) and not section_conflicts_with_schedule(section, current_schedule):
                current_schedule.append(section)
                backtrack(course_index+1, current_schedule)
                current_schedule.pop()
    backtrack(0, [])
    return all_valid_schedules