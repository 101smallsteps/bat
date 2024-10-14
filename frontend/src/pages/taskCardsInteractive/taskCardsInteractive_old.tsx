import React, { useState } from 'react';
import { Button, Dialog, DialogTitle, DialogContent, DialogActions, TextField } from '@mui/material';
import { updateTaskStatus, addTaskComment } from '../../api/api';
import InteractiveDetailTaskCard from '../interactiveDetailTaskCard/InteractiveDetailTaskCard';

const TaskCardsInteractive = ({ tasks, userData }) => {
  const [selectedTask, setSelectedTask] = useState(null);

  const handleOpenDetails = (task) => {
    setSelectedTask(task);
  };

  return (
    <div className="task-cards-interactive">
      {tasks.length === 0 ? (
        <div className="empty-message">No tasks available</div>
      ) : (
        tasks.map((task) => (
          <div key={task.id} className="task-card">
            <h3>{task.title}</h3>
            <p>{task.description}</p>
            <p>Status: {task.task_status}</p>
            <Button variant="contained" onClick={() => handleOpenDetails(task)}>
              Detail
            </Button>
          </div>
        ))
      )}

      {selectedTask && (
        <InteractiveDetailTaskCard
          task={selectedTask}
          onClose={() => setSelectedTask(null)}
          userData={userData}
        />
      )}
    </div>
  );
};

export default TaskCardsInteractive;
