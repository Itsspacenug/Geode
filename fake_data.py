import random
import json
from models import Course, Section, TimeBlock

MWF_SLOTS = [(480, 530), (540, 590), (600, 650), (660, 710), (720, 770), (780, 830)]
TR_SLOTS = [(480, 555), (570, 645), (660, 735), (750, 825), (840, 915)]

def make_fake_sections(course_code, department, n=None):
    n = n or random.randint(2,4)
    section_ids = ['A', 'B', 'C', 'D']
    
    mwf_options = [(slot, [0,2,4]) for slot in MWF_SLOTS]
    tr_options = [(slot, [1,3]) for slot in TR_SLOTS]
    all_options = mwf_options+tr_options
    
    chosen_configs = random.sample(all_options, min(n, len(all_options)))
    
    sections = []
    for i, ((start, end), days) in enumerate(chosen_configs): 
        sections.append(Section(
            course_reg_num=f"{course_code}-{section_ids[i]}",
            section_id=section_ids[i],
            course_code=course_code,
            department=department,
            time_blocks=[TimeBlock(day=d, start=start, end=end) for d in days]
        ))
        
    return sections

def parse_code(raw_code):
    letters = ''.join(c for c in raw_code if c.isalpha())
    numbers = ''.join(c for c in raw_code if c.isdigit())
    return letters, numbers

def load_courses():
    with open('mines_catalog.json') as f:
        catalog = json.load(f)
        
    print(f"Loading {len(catalog)} courses...")
    print(catalog[0])
        
    courses = []
    for i, entry in enumerate(catalog):
        department, _ = parse_code(entry['code'])
        courses.append(Course(
            name=entry['name'],
            course_code=entry['code'],
            department=department,
            sections=make_fake_sections(entry['code'], department)
        ))
        if i % 5 == 0:
            print(f" {i}/{len(catalog)} loaded")
    print(f"Done. {len(courses)} courses ready.")
    return courses
