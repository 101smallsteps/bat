import React from 'react';
import { useParams } from 'react-router-dom';
import { useState,useEffect  } from 'react';

import { data_courses } from "../../data_courses";
import './CourseDetail.scss';

const CourseDetail = () => {
  const { courseId } = useParams();
  const [course, setCourse] = useState(null);
  const [thumbnails, setThumbnails] = useState([]);

  useEffect(() => {
    const fetchCourseData = async () => {
      const fetchedCourse = data_courses.find((course) => course.id === parseInt(courseId));

      if (fetchedCourse) {
        setCourse(fetchedCourse);

        // Fetch thumbnails using a service like YouTube Data API
        const thumbnailUrls = await fetchThumbnails(fetchedCourse.youtubeLinks);
        setThumbnails(thumbnailUrls);
      }
    };

    fetchCourseData();
  }, [courseId]);

  const fetchThumbnails = async (youtubeLinks) => {
    // Implement your logic to fetch thumbnails using YouTube Data API or a third-party service
    // Return an array of thumbnail URLs
    return youtubeLinks.map((link) => {
      // Example: Construct thumbnail URL based on video ID
      const videoId = extractVideoId(link);
      return `https://img.youtube.com/vi/${videoId}/hqdefault.jpg`;
    });
  };

const extractVideoId = (url) => {
  const regex = /v=([^&?]+)/;
  const match = url.match(regex);

  if (match && match.length > 1) {
    return match[1];
  }

  return null; // Return null if no video ID is found
};

  if (!course) {
    return <div>Course not found</div>;
  }

return (
    <div className="course-detail">
      <h2>{course.title}</h2>
      <p>{course.description}</p>
      <div className="youtube-links-container">
        {course.youtubeLinks.map((link, index) => (
          <div className="youtube-link-card" key={index}>
            <a
              href={link.url}
              target="_blank"
              rel="noopener noreferrer"
            >
              <img src={thumbnails[index]} alt="Thumbnail" />
              <p>{link.description}</p>
            </a>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CourseDetail;