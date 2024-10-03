import React from 'react';
import { Link } from 'react-router-dom';
import './courseCard.scss';
interface CourseCardProps {
  id: number;
  title: string;
  description: string;
  image: string; // URL of the course image
}

const CourseCard: React.FC<CourseCardProps> = ({ id, title, description, image }) => {
  return (
    <div className="course-card">
      <img src={image} alt={title} className="course-card-image" />
      <div className="course-card-content">
        <h3 className="course-card-title">
          <Link to={`/courses/${id}`}>{title}</Link>
        </h3>
        <p className="course-card-description">{description}</p>
      </div>
    </div>
  );
};

export default CourseCard;
