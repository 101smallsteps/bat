import React, { useState, useEffect } from "react";
import JobCard from "../../components/jobcard/JobCard";
import ApplicationForm from "../../pages/applicationform/ApplicationForm";
import { getVolunteerJobs, getUserCertificates, getStaffApplications, getCurrentUser } from "../../api/api"; // Add `getCurrentUser` function
import { JobType } from "../../types";
import "./VolunteerJobs.scss";

const VolunteerJobs: React.FC = () => {
  const [volunteerJobs, setVolunteerJobs] = useState<JobType[]>([]);
  const [userCertificates, setUserCertificates] = useState<{ id: number }[]>([]);
  const [applyingJobId, setApplyingJobId] = useState<number | null>(null);
  const [applyingJobName, setApplyingJobName] = useState<string>("");
  const [userApplications, setUserApplications] = useState<{ job: number; approved: boolean | null }[]>([]);
  const [currentUser, setCurrentUser] = useState<{ id: number; username: string } | null>(null);

  const handleApply = (jobId: number, jobName: string) => {
    setApplyingJobId(jobId);
    setApplyingJobName(jobName);
  };

  const hasUserApplied = (jobId: number) => {
    return userApplications.some((app) => app.job === jobId);
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [jobsData, userCerts, applications, user] = await Promise.all([
          getVolunteerJobs(),
          getUserCertificates(),
          getStaffApplications(),
          getCurrentUser(),
        ]);

        setVolunteerJobs(jobsData.results || jobsData || []);
        setUserCertificates(userCerts.results || userCerts || []);
        setUserApplications(Array.isArray(applications) ? applications : []);
        setCurrentUser(user);
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
                hasApplied={hasUserApplied(job.id)}
                onApply={() => handleApply(job.id, job.title)}
              />
            ))
          ) : (
            <p>No volunteer jobs available at the moment.</p>
          )
        ) : (
          currentUser && (
            <ApplicationForm userId={currentUser.id} jobId={applyingJobId} jobName={applyingJobName} />
          )
        )}
      </div>
    </div>
  );
};

export default VolunteerJobs;
