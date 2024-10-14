import React, { useState } from 'react';
import { Button, Dialog, DialogTitle, DialogContent, DialogActions, TextField } from '@mui/material';
import { updateTaskStatus, addTaskComment, uploadCompletionEvidence } from '../../api/api';
import './InteractiveDetailTaskCard.scss';
const InteractiveDetailTaskCard = ({ task, onClose, userData }) => {
  const [currentStatus, setCurrentStatus] = useState(task.task_status);
  const [completionSummary, setCompletionSummary] = useState('');
  const [comment, setComment] = useState('');
  const [evidence, setEvidence] = useState(null);
  const [isCompleteDialogOpen, setIsCompleteDialogOpen] = useState(false);
  const isSuperUser = userData.isSuperUser || false; // Ensure isSuperUser has a fallback
  console.log(userData);
  const handleStatusChange = async (newStatus) => {
    await updateTaskStatus(task.id, { task_status: newStatus });
    setCurrentStatus(newStatus);

    if (newStatus === 'completed') {
      setIsCompleteDialogOpen(true);
    }
  };

  const handleSaveCompletion = async () => {
    await updateTaskStatus(task.id, {
      task_status: 'completed',
      completion_summary: completionSummary,
    });
    if (evidence) {
      await uploadCompletionEvidence(task.id, evidence);
    }
    setIsCompleteDialogOpen(false);
    onClose();
  };

  const handleFileChange = (e) => {
    setEvidence(e.target.files[0]);
  };

  const handleAddComment = async () => {
    await addTaskComment(task.id, comment);
    setComment('');
  };

  return (
    <Dialog open={Boolean(task)} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>{task.title} Details</DialogTitle>
      <DialogContent className="dialog-content-scrollable">
        <p>Description: {task.description}</p>
        <p>Current Status: {currentStatus}</p>

        {currentStatus === 'assigned' && (
          <Button variant="contained" color="primary" onClick={() => handleStatusChange('started')}>
            Start Task
          </Button>
        )}

        {currentStatus === 'started' && (
          <Button variant="contained" color="secondary" onClick={() => setIsCompleteDialogOpen(true)}>
            Complete Task
          </Button>
        )}
        {/* Superuser-specific transitions */}
        {isSuperUser && (
          <>
            {currentStatus === 'completed' && (
              <>
                <Button
                  variant="contained"
                  color="success"
                  onClick={() => handleStatusChange('accepted')}
                >
                  Accept Task
                </Button>
                <Button
                  variant="contained"
                  color="warning"
                  onClick={() => handleStatusChange('assigned')}
                >
                  Reassign Task
                </Button>
              </>
            )}

            {currentStatus === 'accepted' && (
              <Button
                variant="contained"
                color="info"
                onClick={() => handleStatusChange('closed')}
              >
                Close Task
              </Button>
            )}
          </>
        )}


        {/* Complete Task Dialog */}
        <Dialog open={isCompleteDialogOpen} onClose={() => setIsCompleteDialogOpen(false)}>
          <DialogTitle>Complete Task</DialogTitle>
          <DialogContent>
            <TextField
              label="Completion Summary"
              multiline
              rows={3}
              value={completionSummary}
              onChange={(e) => setCompletionSummary(e.target.value)}
              fullWidth
            />
            <input type="file" onChange={handleFileChange} />
          </DialogContent>
          <DialogActions>
            <Button
                onClick={handleSaveCompletion}
                color="primary"
                disabled={!completionSummary.trim()} // Disable if completionSummary is empty
             >Save Completion</Button>
            <Button onClick={() => setIsCompleteDialogOpen(false)}>Cancel</Button>
          </DialogActions>
        </Dialog>

        {/* Comment Section */}
        <div className="comments">
          <h4>Comments</h4>
          <TextField
            label="Add Comment"
            multiline
            rows={2}
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            fullWidth
          />
          <Button variant="outlined" onClick={handleAddComment}>Add Comment</Button>

          {/* Display comments in reverse chronological order */}
          {task.comments?.slice().reverse().map((c) => (
            <div key={c.id} className="comment-card">
              <p className="comment-author">{c.user}</p>
              <p className="comment-timestamp">{new Date(c.created_at).toLocaleString()}</p>
              <p className="comment-text">{c.comment}</p>
            </div>
          ))}
        </div>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Close</Button>
      </DialogActions>
    </Dialog>
  );
};

export default InteractiveDetailTaskCard;
