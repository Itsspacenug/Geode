

const DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];


const GRID_START = 7 * 60;
const PIXELS_PER_MINUTE = 1.2;


const getPositionStyles = (start, end) => ({
  position: 'absolute',
  top: `${(start - GRID_START) * PIXELS_PER_MINUTE}px`,
  height: `${(end - start) * PIXELS_PER_MINUTE}px`,
});

// Props are built by the parent from the raw API response — WeeklyGrid just renders
const WeeklyGrid = ({ inputdf, coursedf, sectiondf, timeblockdf, onBlockClick }) => {

  // REMOVED: duplicate const declarations for inputdf, sectiondf, timeblockdf
  // Those were redefining the props and referencing `schedule` which isn't in scope here
  // The parent is responsible for building these arrays and passing them in

  return (
    <div className="days-wrapper">
      {DAYS.map((dayName, dayIndex) => (
        <div key={dayName} className="day-column">
          <div className="day-header">{dayName}</div>
          <div className="column-content">

            {/* 1. Start with the user's input selections */}
            {inputdf.map(input => {
              // 2. Find the section for this input by CRN
              const section = sectiondf.find(s => s.crn === input.crn);
              if (!section) return null;

              // 3. Find the master course info by course code
              // coursedf may not always have an entry — course is allowed to be undefined
              const course = coursedf.find(c => c.course_code === input.code);

              // 4. Find all timeblocks for this section that fall on the current day
              const blocksForDay = timeblockdf.filter(t =>
                section.timeblock_id.includes(t.timeblock_id) && t.day === dayIndex
              );
              if (blocksForDay.length === 0) return null;

              return blocksForDay.map(block => (
                <div
                  key={`${input.crn}-${block.timeblock_id}`}
                  className="course-rect"
                  style={getPositionStyles(block.start, block.end)}
                  onClick={() => onBlockClick({ input, section, course, block })}
                >
                  <div className="course-text">
                    {/* Added space between department and code — otherwise renders as e.g. "CSCI128" */}
                    <strong>{course ? `${course.department} ${course.course_code}` : input.code}</strong>
                    <span>{section.section_id}</span>
                  </div>
                </div>
              ));
            })}

          </div>
        </div>
      ))}
    </div>
  );
};

export default WeeklyGrid;