import React, { useState, useEffect } from "react";
import JobCard from "../../components/jobcard/JobCard";
import ApplicationForm from "../../pages/applicationform/ApplicationForm"; // Adjust path as necessary
import { getVolunteerJobs, getUserCertificates } from "../../api/api";
import { JobType } from "../../types"; // Define JobType properly in your types file
import "./VolunteerJobs.scss";

const VolunteerJobs: React.FC = () => {
  const [volunteerJobs, setVolunteerJobs] = useState<JobType[]>([]);
  const [userCertificates, setUserCertificates] = useState<string[]>([]);
  const [applyingJobId, setApplyingJobId] = useState<number | null>(null);
  const [applyingJobName, setApplyingJobName] = useState<string>("");

  const handleApply = (jobId: number, jobName: string) => {
    console.log("Applying for job with ID:", jobId, "Job Name:", jobName);
    setApplyingJobId(jobId);
    setApplyingJobName(jobName); // Set the job name as well
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getVolunteerJobs();
        const userCerts = await getUserCertificates();
        setVolunteerJobs(data.results || data || []);
        setUserCertificates(userCerts.results || userCerts || []);
      } catch (error) {
        console.error("Failed to fetch volunteer jobs:", error);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="volunteer-jobs-page">
      <h1>Volunteer Jobs</h1>
      <div className="job-list">
        {applyingJobId === null ? (
          volunteerJobs.length > 0 ? (
            volunteerJobs.map((job) => (
              <JobCard
                key={job.id}
                job={job}
                userCertificates={userCertificates}
                onApply={() => handleApply(job.id, job.title)} // Pass job title to handleApply
              />
            ))
          ) : (
            <p>No volunteer jobs available at the moment.</p>
          )
        ) : (
          <ApplicationForm userId={1} jobId={applyingJobId} jobName={applyingJobName} /> // Pass job name here
        )}
      </div>
    </div>
  );
};

export default VolunteerJobs;
