// TeamAdminDashboard.tsx
import React from 'react';
import TeamAdminProjectsTab from '../teamAdminProjectsTab/TeamAdminProjectsTab';
import './TeamAdminDashboard.scss';

const TeamAdminDashboard: React.FC = () => {
  return (
    <div className="dashboard-container">
      <div className="tab-header">
        <h1>Team Admin Dashboard</h1>
        <div className="tabs">
          <button className="active-tab">Projects</button>
          {/* Additional tabs can be added here */}
        </div>
      </div>
      <TeamAdminProjectsTab />
    </div>
  );
};

export default TeamAdminDashboard;
