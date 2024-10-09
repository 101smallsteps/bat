import React, { useState, useEffect } from "react";
import axios from "axios";
import { getStaffApplications,getUnassignedSymbols,postApproveStaffApplications,postDisApproveStaffApplications } from "../../api/api"; // Add `getCurrentUser` function

import "./SuperUserApproval.scss";
const SuperUserApproval: React.FC = () => {
  const [applications, setApplications] = useState<any[]>([]);
  const [symbols, setSymbols] = useState<any[]>([]);
  const [selectedSymbols, setSelectedSymbols] = useState<{ [key: number]: string }>({});

  useEffect(() => {
    // Fetch all staff applications that are not yet approved
    const fetchApplications = async () => {
      try {
        const response = await getStaffApplications();
        console.log("fetchApplications",response);
        const pendingApplications = response.filter(
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
        const response = await getUnassignedSymbols(); // Adjust URL as per your API
        console.log("fetchSymbols",response);
        setSymbols(response);
      } catch (error) {
        console.error("Error fetching symbols", error);
      }
    };

    fetchApplications();
    fetchSymbols();
  }, []);

  const handleSymbolChange = (appId: number, symbolId: string) => {
    setSelectedSymbols((prev) => ({ ...prev, [appId]: symbolId }));
  };

  const handleApprove = async (applicationId: number) => {
    try {
      const selectedSymbol = selectedSymbols[applicationId]; // Retrieve the selected symbol for this application
      if (!selectedSymbol) {
        alert("Please select a symbol before approving.");
        return;
      }
      const applicationData = {symbol_id: selectedSymbol,applId:applicationId };
      await postApproveStaffApplications(applicationData);
      setApplications(applications.filter((app) => app.id !== applicationId));
      alert("Application approved and symbol assigned!");
    } catch (error) {
      console.error("Error approving application", error);
    }
  };

  const handleDisapprove = async (applicationId: number) => {
    try {
      await postDisApproveStaffApplications(applicationId);
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
            <label htmlFor={`symbol-${app.id}`}>Assign Symbol</label>
            <select
              id={`symbol-${app.id}`}
              value={selectedSymbols[app.id] || ""}
              onChange={(e) => handleSymbolChange(app.id, e.target.value)}
            >
              <option value="">Select Symbol</option>
              {symbols.map((symbol) => (
                <option key={symbol.id} value={symbol.id}>
                  {symbol.symbolName}
                </option>
              ))}
            </select>
            <div className="button-group">
              <button onClick={() => handleApprove(app.id)}
              disabled={app.approved}>
               {app.approved ? "Already Approved" : "Approve"}
              </button>
              <button onClick={() => handleDisapprove(app.id)}>Disapprove</button>
            </div>
          </div>
        ))
      )}
    </div>
  );
};

export default SuperUserApproval;
