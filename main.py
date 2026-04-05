from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sample_data import COURSES
from generator import find_all_schedules
from optimizer import calculate_total_score


# Create the FastAPI app instance
app = FastAPI()

#Allows the frontend on port 5173 to talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Defines the format of the data that we expect to in the POST request body
# Pydantic validates it automatically and if frontend sends wrong data, Pydantic errors cleanly
class OptimizeRequests(BaseModel):
    course_codes: list[str]
    preferences: dict[str, float]

@app.get("/courses")
def get_courses():
    return[
        {
            "course_code": classes.course_code,
            "name": classes.name,
            "sections": [
                {
                "section_id": section.section_id,
                "time_blocks": [
                    {
                        "day": tb.day,
                        "start": tb.start,
                        "end": tb.end
                    }
                    for tb in section.time_blocks
                ]
            }
            for section in classes.sections
            ],
            "departments": classes.department,


        }
        for classes in COURSES
    ]

@app.post("/optimize")
def run_optimize(request: OptimizeRequests):
    filtered_courses = [c for c in COURSES if c.course_code in request.course_codes] #Filter all coursese that the user has chosen from requests
    all_possible_schedules = find_all_schedules(filtered_courses) # finds all permiatations from the filtered courses
    #calculates the score of each possible schedule based on the users request of preferences and ranks it from highest to lowest score
    sorted_schedules_score = sorted(
        all_possible_schedules,
        key=lambda schedule: calculate_total_score(schedule, request.preferences),
        reverse=True
    )

    return {"results" : sorted_schedules_score[0:5]}







# from generator import find_all_schedules
# from optimizer import calculate_total_score
# import models

# courses = [models.Course("Calculus III", "213", "MATH", [
#                 models.Section("81004","A","213","MATH", [models.TimeBlock(0, 780, 840)])
#                 ]),
#            models.Course("Computer Science for STEM", "128", "CSCI", [models.Section("81005","A","128","CSCI", [models.TimeBlock(0, 825, 900)]), models.Section("81009","D","128","CSCI", [models.TimeBlock(2, 825, 900)])]),
#            models.Course("Physics I - Mechanics", "100", "PHGN", [models.Section("81005","B","100","PHGN", [models.TimeBlock(0,910,970)])]),
#            models.Course("Nature and Human Values", "100", "HASS", [models.Section("81006","C","100","HASS", [models.TimeBlock(0, 1000, 1060)])])]
# # make course list

# raw_schedules = find_all_schedules(courses)

# user_weights = {
#     "compactness": 1.0,
#     "early_morning": 2.5
# }


# def minutes_to_time(minutes: int) -> str:
#     hours = minutes // 60
#     mins = minutes % 60
#     period = "AM" if hours < 12 else "PM"
    
#     if hours == 0:
#         hours = 12
#     elif hours > 12:
#         hours -= 12
        
#     return f"{hours}:{mins:02d} {period}"

# def print_schedule(schedule: list[models.Section]):
#     DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
#     print("\n"+"="*30)
#     print("Your GEODE Schedule:")
#     print("="*30)
    
#     for section in schedule:
#         print(f"\n{section.department} {section.course_code} (Section {section.section_id})")
#         print(f"CRN: {section.course_reg_num}")
        
#         for tb in section.time_blocks:
#             day_name = DAYS[tb.day]
#             start_str = minutes_to_time(tb.start)
#             end_str = minutes_to_time(tb.end)
#             print(f" {day_name}: {start_str} - {end_str}")
            
#     print("\n" + "="*30 + "\n")

# if not raw_schedules:
#     print("No valid schedules found.")
# else:
#     ranked_schedules = sorted(
#         raw_schedules,
#         key=lambda schedule: calculate_total_score(schedule, user_weights) or 0,
#         reverse=True
#     )
    
#     top_choice = ranked_schedules[0]
#     print(f"Found {len(ranked_schedules)} valid schedule(s)!")
#     print(f"Top Score: {calculate_total_score(top_choice, user_weights)}")
    
#     # Print the beautiful output!
#     print_schedule(top_choice)
