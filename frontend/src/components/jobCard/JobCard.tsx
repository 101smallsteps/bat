import React from "react";
import { JobType } from "../types";
import "./JobCard.scss";

interface JobCardProps {
  job: JobType;
  userCertificates?: { id: number }[];
  hasApplied: boolean;
  onApply: (jobId: number) => void;
}

const JobCard: React.FC<JobCardProps> = ({ job, userCertificates = [], hasApplied, onApply }) => {
  // Extract certificate IDs for easier comparison
  const userCertificateIds = userCertificates.map(cert => cert.id);

  // Check if user has all prerequisite certificates
  const hasAllPrerequisites = job.prerequisites.every(prerequisite => userCertificateIds.includes(prerequisite.id));

  // Determine button label and disable status
  let buttonText = "Submit Application";
  let buttonDisabled = false;

  if (!hasAllPrerequisites) {
    buttonText = "Pre-req Certification required to apply";
    buttonDisabled = true;
  } else if (hasApplied) {
    buttonText = "Already Applied";
    buttonDisabled = true;
  }

  return (
    <div className="job-card">
      <h3>{job.title}</h3>
      <p><strong>Description:</strong> {job.description}</p>
      <p><strong>Responsibilities:</strong> {job.responsibilities}</p>
      <p><strong>Designation:</strong> {job.designation}</p>
      <p><strong>Designation Level:</strong> {job.designation_level}</p>
      <button
        className={`submit-btn ${buttonDisabled ? "not-eligible" : "eligible"}`}
        disabled={buttonDisabled}
        onClick={() => !buttonDisabled && onApply(job.id)}
      >
        {buttonText}
      </button>
    </div>
  );
};

export default JobCard;
