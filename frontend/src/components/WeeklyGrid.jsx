const WeeklyGrid = ({ inputdf, coursedf, sectiondf, timeblockdf, onBlockClick }) => {
  const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];

  return (
    <div className="days-wrapper">
      {days.map((dayName, dayIndex) => (
        <div key={dayName} className="day-column">
          <div className="day-header">{dayName}</div>
          <div className="column-content">
            
            {/* 1. Start with the user's input selections */}
            {inputdf.map(input => {
              // 2. Find the section details for this input (Connects CRN)
              const section = sectiondf.find(s => s.crn === input.crn);
              if (!section) return null;

              // 3. Find the master course info (Connects Dept/Code)
              const course = coursedf.find(c => c.course_code === input.code);
              
              // 4. Find all timeblocks for this section that match the current day
              const blocksForDay = timeblockdf.filter(t => 
                section.timeblock_id.includes(t.timeblock_id) && t.day === dayIndex
              );

              return blocksForDay.map(block => (
                <div 
                  key={`${input.crn}-${block.id}`}
                  className="course-rect"
                  style={getPositionStyles(block.start, block.end)}
                  /* When clicked, you pass the raw "row" objects from your DataFrames */
                  onClick={() => onBlockClick({ input, section, course, block })}
                >
                  <div className="course-text">
                    <strong>{course?.department}{course?.course_code}</strong>
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