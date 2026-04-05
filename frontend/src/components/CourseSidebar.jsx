import React from 'react';
import './CourseSidebar.css';

const CourseSidebar = ({ data, onClose }) => {
  if (!data) return null;

  // Destructure the "joined" data we passed from WeeklyGrid
  const { course, section, block } = data;

  return (
    <aside className="course-sidebar">
      <div className="sidebar-header">
        <button className="close-btn" onClick={onClose}>&times;</button>
        <h2>{course?.department} {course?.course_code}</h2>
        <p className="course-title">{course?.name || "Abstract Algebra"}</p>
      </div>

      <div className="sidebar-body">
        <section className="info-group">
          <h3>Section Details</h3>
          <div className="info-row">
            <span>CRN:</span> <strong>{section.crn}</strong>
          </div>
          <div className="info-row">
            <span>Section ID:</span> <strong>{section.section_id}</strong>
          </div>
        </section>

        <section className="info-group">
          <h3>Current Block</h3>
          <p>
            This block runs from <strong>{Math.floor(block.start / 60)}:{(block.start % 60).toString().padStart(2, '0')}</strong> to 
            <strong> {Math.floor(block.end / 60)}:{(block.end % 60).toString().padStart(2, '0')}</strong>.
          </p>
        </section>

        {/* Since you have the course object, you can display catalog info here */}
        <section className="info-group">
          <h3>Description</h3>
          <p className="description-text">
            {course?.description || "No description available in coursedf."}
          </p>
        </section>
      </div>

      <div className="sidebar-footer">
        <button className="action-btn secondary">Lock Section</button>
        <button className="action-btn primary">Remove Course</button>
      </div>
    </aside>
  );
};

export default CourseSidebar;