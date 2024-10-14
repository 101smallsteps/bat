import React, { useState } from 'react';
import { Dialog, DialogTitle, DialogContent } from '@mui/material';
import { updateTaskStatus, addTaskComment } from '../../api/api';
import ReadOnlyDetailTaskCard from '../readOnlyDetailTaskCard/ReadOnlyDetailTaskCard';

const TaskCardsReadOnly = ({ tasks, userData }) => {
  const [selectedTask, setSelectedTask] = useState(null);

  return (
    <div className="task-cards-readonly">
      {tasks.length === 0 ? (
      <div className="empty-message">No tasks available</div>
      ) : (
        tasks.map((task) => (
          <div key={task.id} className="task-cards">
            <h3>{task.title}</h3>
            <p>{task.description}</p>
            <button onClick={() => setSelectedTask(task)}>View</button>

            <Dialog open={Boolean(selectedTask)} onClose={() => setSelectedTask(null)}>
              <DialogTitle>{selectedTask?.title}</DialogTitle>
              <DialogContent>
                <p>{selectedTask?.description}</p>
                {/* Display comments here */}
              </DialogContent>
            </Dialog>
          </div>
        ))
      )}
      {selectedTask && (
        <ReadOnlyDetailTaskCard
          task={selectedTask}
          onClose={() => setSelectedTask(null)}
          userData={userData}
        />
      )}
    </div>
  );
};

export default TaskCardsReadOnly;
