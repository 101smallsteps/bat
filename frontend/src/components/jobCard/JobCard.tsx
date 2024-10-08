import React from "react";
import { JobType } from "../types";
import "./JobCard.scss";

interface JobCardProps {
  job: JobType;
  userCertificates?: { id: number }[];
  hasApplied: boolean; // Add this prop
  onApply: (jobId: number) => void;
}

const JobCard: React.FC<JobCardProps> = ({ job, userCertificates = [], hasApplied, onApply }) => {
  const userCertificateIds = userCertificates.map(cert => cert.id);
  const isEligible = job.prerequisites.every(prerequisite => userCertificateIds.includes(prerequisite.id));

  return (
    <div className="job-card">
      <h3>{job.title}</h3>
      <p><strong>Description:</strong> {job.description}</p>
      <p><strong>Responsibilities:</strong> {job.responsibilities}</p>

      <button
        className={`submit-btn ${isEligible ? "eligible" : "not-eligible"}`}
        disabled={!isEligible || hasApplied}
        onClick={() => isEligible && !hasApplied && onApply(job.id)}
      >
        {hasApplied ? "Already Applied" : isEligible ? "Submit Application" : "Not Eligible"}
      </button>
    </div>
  );
};

export default JobCard;
