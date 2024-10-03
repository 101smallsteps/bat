import { Link } from "react-router-dom";
import "./Courses.scss";
import { data_courses } from "../../data_courses";
import CourseCard from '../../components/courseCard/CourseCard'; // Import your CourseCard component

interface Courses {
  id: number;
  title: string;
  description: string;
  youtubeLinks: string[];
}

const Courses = (props) => {

  return (
    <div className="courses">
      <h1>Courses</h1>
      <div className="courses-container"> {/* Added container for styling */}
        {data_courses.map((course) => (
          <CourseCard key={course.id} {...course} />
        ))}
      </div>
    </div>
  );
};


export default Courses;
