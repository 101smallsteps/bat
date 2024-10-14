import React from 'react';
import './readOnlyDetailTaskCard.scss';
import { Button, Dialog, DialogTitle, DialogContent, DialogActions, TextField } from '@mui/material';

const ReadOnlyDetailTaskCard = ({ task, onClose }) => {
  return (
    <Dialog open={Boolean(task)} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>{task.title} Details</DialogTitle>
      <DialogContent className="dialog-content-scrollable">
        <p><strong>Description:</strong> {task.description}</p>
        <p><strong>Current Status:</strong> {task.task_status}</p>

        {/* Comments Section */}
        <div className="comments">
          <h4>Comments</h4>
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

export default ReadOnlyDetailTaskCard;
