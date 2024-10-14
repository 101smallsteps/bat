// TaskTabs.tsx
import React, { useState, useEffect } from 'react';
import { Tabs, Tab } from '@mui/material';
import TaskCardsInteractive from '../taskCardsInteractive/TaskCardsInteractive';
import TaskCardsReadOnly from '../taskCardsReadOnly/TaskCardsReadOnly';
import { fetchTasks, fetchTasksForUser,fetchClosedTasksForUser,fetchUserCompletedOrAcceptedTasks,updateTaskStatus } from '../../api/api';
import './taskTabs.scss';
const TaskTabs: React.FC = ({userData}) => {
  const [tabIndex, setTabIndex] = useState(0);
  const [tasks, setTasks] = useState([]);
  const [closedTasks, setclosedTasks] = useState([]);
  const [pendingTasks, setpendingTasks] = useState([]);

  useEffect(() => {
    fetchTasksForUser(userData.id).then(setTasks);
    console.log(tasks);
  }, []);

  useEffect(() => {
    fetchClosedTasksForUser().then(setclosedTasks);
    console.log(closedTasks);
  }, []);

  useEffect(() => {
    fetchUserCompletedOrAcceptedTasks().then(setpendingTasks);
    console.log("pendingTasks",pendingTasks);
  }, []);

  // Calculate task counts for each tab
  const todoCount = tasks.filter(
    (task) =>
      task.task_type === 'sequential' &&
      task.task_status !== 'created' &&
      task.task_status !== 'accepted' &&
      task.task_status !== 'closed'
  ).length;

  const pendingCount = pendingTasks.filter(
    (task) => task.task_status === 'completed' || task.task_status === 'accepted'
  ).length;

  const closedCount = closedTasks.filter((task) => task.task_status === 'closed').length;

  return (
  <div className="task-tabs-container">
  <div className="tabs">
    <Tab
       label={`TODO (${todoCount})`}
      onClick={() => setTabIndex(0)}
      className={tabIndex === 0 ? "tab active" : "tab"}
    />
    <Tab
      label={`Pending Approval (${pendingCount})`}
      onClick={() => setTabIndex(1)}
      className={tabIndex === 1 ? "tab active" : "tab"}
    />
    <Tab
      label={`History (${closedCount})`}
      onClick={() => setTabIndex(2)}
      className={tabIndex === 2 ? "tab active" : "tab"}
    />
  </div>

  <div className="task-tabs-content">
    {tabIndex === 0 && (
      <TaskCardsInteractive
        tasks={tasks.filter(
          (task) =>
            task.task_type === "sequential" &&
            task.task_status !== "created" &&
            task.task_status !== "accepted" &&
            task.task_status !== "closed"
        )}
        userData={userData}
      />
    )}
    {tabIndex === 1 && (
      <TaskCardsReadOnly
        tasks={pendingTasks.filter(
          (task) =>
            task.task_status === "completed" ||
            task.task_status === "accepted"
        )}
        userData={userData}
      />
    )}
    {tabIndex === 2 && (
      <TaskCardsReadOnly
        tasks={closedTasks.filter((task) => task.task_status === "closed")}
        userData={userData}
      />
    )}
  </div>
</div>

  );
};

export default TaskTabs;
