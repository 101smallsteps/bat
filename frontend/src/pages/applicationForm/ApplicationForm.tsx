import React, { useState, useEffect } from "react";
import axios from "axios";
import "./ApplicationForm.scss";
import { getStaffApplications,postStaffApplications } from "../../api/api";

interface ApplicationFormProps {
  userId: number;
  jobId: number;
  jobName: string;  // Receive jobName as a prop
}

const ApplicationForm: React.FC<ApplicationFormProps> = ({ userId, jobId, jobName }) => {
  const [formData, setFormData] = useState({
    institution_name: "",
    home_address: "",
    home_state: "",
    home_county: "",
    home_country: "",
    home_zipcode: "",
    institution_address: "",
    institution_state: "",
    institution_county: "",
    institution_country: "",
    institution_zipcode: "",
    email: "",
    phone: "",
  });

  const [hasApplied, setHasApplied] = useState(false);
  const [isApproved, setIsApproved] = useState<boolean | null>(null);

  // Fetch the application status
  useEffect(() => {
    const fetchApplicationStatus = async () => {
      try {
        const response = await getStaffApplications;
        const applications = Array.isArray(response.data) ? response.data : [];
        const application = applications.find(
          (app: any) => app.user === userId && app.job === jobId
        );
        if (application) {
          setHasApplied(true);
          setIsApproved(application.approved);
        }
      } catch (error) {
        console.error("Error fetching application status", error);
      }
    };
    fetchApplicationStatus();
  }, [userId, jobId]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const applicationData = { ...formData, job: jobId, user: userId };
      await postStaffApplications(applicationData);
      setHasApplied(true);
      alert("Application submitted successfully!");
    } catch (error) {
      console.error("Error submitting application", error);
    }
  };

    return (
    <div className="application-form">
      <h2>Staff User Application for {jobName}</h2>
      {hasApplied && isApproved !== null ? (
        <p>Your application for this job has been {isApproved ? "approved" : "disapproved"}.</p>
      ) : (
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            name="institution_name"
            placeholder="Institution Name"
            value={formData.institution_name}
            onChange={handleInputChange}
            required
          />
          <input
            type="text"
            name="institution_address"
            placeholder="Institution Address"
            value={formData.institution_address}
            onChange={handleInputChange}
            required
          />
          <input
            type="text"
            name="institution_state"
            placeholder="Institution State"
            value={formData.institution_state}
            onChange={handleInputChange}
            required
          />
          <input
            type="text"
            name="institution_county"
            placeholder="Institution County"
            value={formData.institution_county}
            onChange={handleInputChange}
            required
          />
          <input
            type="text"
            name="institution_country"
            placeholder="Institution Country"
            value={formData.institution_country}
            onChange={handleInputChange}
            required
          />
          <input
            type="text"
            name="institution_zipcode"
            placeholder="Institution Zipcode"
            value={formData.institution_zipcode}
            onChange={handleInputChange}
            required
          />

          <input
            type="text"
            name="home_address"
            placeholder="Home Address"
            value={formData.home_address}
            onChange={handleInputChange}
            required
          />
          <input
            type="text"
            name="home_state"
            placeholder="Home State"
            value={formData.home_state}
            onChange={handleInputChange}
            required
          />
          <input
            type="text"
            name="home_county"
            placeholder="Home County"
            value={formData.home_county}
            onChange={handleInputChange}
            required
          />
          <input
            type="text"
            name="home_country"
            placeholder="Home Country"
            value={formData.home_country}
            onChange={handleInputChange}
            required
          />
          <input
            type="text"
            name="home_zipcode"
            placeholder="Home Zipcode"
            value={formData.home_zipcode}
            onChange={handleInputChange}
            required
          />
          <input
            type="text"
            name="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleInputChange}
            required
          />
          <input
            type="text"
            name="phone"
            placeholder="Phone"
            value={formData.phone}
            onChange={handleInputChange}
            required
          />
          <button type="submit" disabled={hasApplied}>
            Submit Application
          </button>
        </form>
      )}
    </div>
  );
};

export default ApplicationForm;
