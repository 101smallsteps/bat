import React, { useState, useEffect } from "react";
import axios from "axios";
import "./SuperUserApproval.scss";
const SuperUserApproval: React.FC = () => {
  const [applications, setApplications] = useState<any[]>([]);
  const [symbols, setSymbols] = useState<any[]>([]);

  useEffect(() => {
    // Fetch all staff applications that are not yet approved
    const fetchApplications = async () => {
      try {
        const response = await axios.get("/api/staff-applications/");
        const pendingApplications = response.data.filter(
          (app: any) => !app.approved
        );
        setApplications(pendingApplications);
      } catch (error) {
        console.error("Error fetching applications", error);
      }
    };

    // Fetch available symbols
    const fetchSymbols = async () => {
      try {
        const response = await axios.get("/api/symbols/"); // Adjust URL as per your API
        setSymbols(response.data);
      } catch (error) {
        console.error("Error fetching symbols", error);
      }
    };

    fetchApplications();
    fetchSymbols();
  }, []);

  const handleApprove = async (applicationId: number, selectedSymbol: string) => {
    try {
      await axios.post(`/api/staff-applications/${applicationId}/approve/`, {
        symbol: selectedSymbol,
      });
      setApplications(applications.filter((app) => app.id !== applicationId));
      alert("Application approved and symbol assigned!");
    } catch (error) {
      console.error("Error approving application", error);
    }
  };

  const handleDisapprove = async (applicationId: number) => {
    try {
      await axios.post(`/api/staff-applications/${applicationId}/disapprove/`);
      setApplications(applications.filter((app) => app.id !== applicationId));
      alert("Application disapproved.");
    } catch (error) {
      console.error("Error disapproving application", error);
    }
  };

  return (
    <div className="superuser-approval">
      <h2>Approve Staff Applications</h2>
      {applications.length === 0 ? (
        <p>No pending applications.</p>
      ) : (
        applications.map((app) => (
          <div key={app.id} className="application-card">
            <h3>{app.user.username}</h3>
            <p>Institution: {app.institution_name}</p>
            <p>Email: {app.email}</p>
            <p>Phone: {app.phone}</p>
            <label htmlFor="symbol">Assign Symbol</label>
            <select
              id="symbol"
              onChange={(e) => handleApprove(app.id, e.target.value)}
            >
              <option value="">Select Symbol</option>
              {symbols.map((symbol) => (
                <option key={symbol.id} value={symbol.id}>
                  {symbol.name}
                </option>
              ))}
            </select>
            <button onClick={() => handleApprove(app.id, "")}>
              Approve
            </button>
            <button onClick={() => handleDisapprove(app.id)}>Disapprove</button>
          </div>
        ))
      )}
    </div>
  );
};

export default SuperUserApproval;
