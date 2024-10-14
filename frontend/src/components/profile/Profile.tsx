import React from "react";
import { Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import "./profile.scss";
import StarIcon from '@mui/icons-material/Star';

type Props = {
  id: number;
  username: string;
  email: string;
  profData: { [key: string]: any } | null; // Allow profData to be nullable
  stars: number;
  taskOwnershipHistory: { task: string; assignedAt: string; assignedBy: string }[];
};

const Profile: React.FC<Props> = (props) => {
 console.log("stars",props.stars);
  return (
    <div className="single">
      {/* Upper Section */}
      <div className="view">
        {/* Left: User Details */}
        <div className="info">
          <div className="topInfo">
            <h1>{props.username}</h1>
            <button>Update</button>
          </div>
          <div className="details">
            {props.profData ? (
              Object.entries(props.profData).map(([key, value]) => (
                <div className="item" key={key}>
                  <span className="itemTitle">{key}</span>
                  <span className="itemValue">{value}</span>
                </div>
              ))
            ) : (
              <p>No profile data available</p>
            )}
          </div>
        </div>

        {/* Right: Star Rating */}
        <div className="star-rating">
          <h2>Star Rating</h2>
          {Array.from({ length: props.stars }, (_, i) => (
            <StarIcon key={i} style={{ color: 'gold' }} />
          ))}
        </div>
      </div>

      <hr />

      {/* Bottom Section: Task Ownership History */}
      <div className="activities">
        <h2>Task Ownership History</h2>
        <ul>
          {props.taskOwnershipHistory.map((entry, index) => (
            <li key={index}>
              <p>{entry.task} - Assigned by {entry.assignedBy}</p>
              <time>{new Date(entry.assignedAt).toLocaleString()}</time>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Profile;
