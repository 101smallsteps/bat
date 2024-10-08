import React, { useState, useEffect } from "react";
import JobCard from "./JobCard";
import ApplicationForm from "./ApplicationForm";
import { getVolunteerJobs, getUserCertificates } from "../api/api"; // Replace with actual API calls
import "./JobList.scss";

const JobList: React.FC = () => {
  const [jobs, setJobs] = useState<JobType[]>([]);
  const [userCertificates, setUserCertificates] = useState<string[]>([]);
  const [applyingJobId, setApplyingJobId] = useState<number | null>(null);  // Track which job the user is applying for

  const handleApply = (jobId: number) => {
    console.log("Applying for job with ID:", jobId);
    setApplyingJobId(jobId);  // Set the job for which the user is applying
  };

  // Fetch jobs and user certificates
  useEffect(() => {
    const fetchData = async () => {
      const jobsData = await getVolunteerJobs();
      const userCerts = await getUserCertificates(); // Should return certificate IDs
      setJobs(jobsData);
      console.log("userCerts in joblist",userCerts);
      setUserCertificates(userCerts);
    };

    fetchData();
  }, []);


console.log("handleApply function in JobList:", handleApply);

  return (
    <div className="job-list">
      {!applyingJobId ? (
        jobs.map((job) => (
          <JobCard
            key={job.id}
            job={job}
            userCertificates={userCertificates}
            onApply={handleApply}  // Pass the apply handler
          />
        ))
      ) : (
        <ApplicationForm userId={1} jobId={applyingJobId} />  {/* Render form for selected job */}
      )}
    </div>
  );
};

export default JobList;
