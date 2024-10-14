import React, { useEffect, useState } from 'react';
import { Button, List, ListItem, ListItemText, Dialog, DialogTitle, DialogActions, DialogContent, TextField, Grid, Select, MenuItem, FormControl, InputLabel, Autocomplete } from '@mui/material';
import { fetchProjects, createProject, updateProject, deleteProject, fetchCertifiedUsersByEmail } from '../../api/api';

const TeamAdminProjectsTab: React.FC = () => {
  const [projects, setProjects] = useState([]);
  const [filteredProjects, setFilteredProjects] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedProject, setSelectedProject] = useState(null);
  const [isCreating, setIsCreating] = useState(false);
  const [emailSearch, setEmailSearch] = useState('');
  const [certifiedUsers, setCertifiedUsers] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;

  const [newProject, setNewProject] = useState({
    title: '',
    description: '',
    start_date: '',
    end_date: '',
    project_type: 'shortTerm',
    members: []
  });

  useEffect(() => {
    fetchProjects().then((fetchedProjects) => {
      setProjects(fetchedProjects);
      setFilteredProjects(fetchedProjects);
    });
  }, []);

  useEffect(() => {
    setFilteredProjects(
      projects.filter((project) =>
        project.title.toLowerCase().includes(searchTerm.toLowerCase())
      )
    );
  }, [searchTerm, projects]);

  useEffect(() => {
    if (emailSearch) {
      fetchCertifiedUsersByEmail(emailSearch).then(setCertifiedUsers);
    } else {
      setCertifiedUsers([]);
    }
  }, [emailSearch]);

  // Update newProject state when selectedProject is set
  useEffect(() => {
    if (selectedProject) {
      setNewProject({
        title: selectedProject.title || '',
        description: selectedProject.description || '',
        start_date: selectedProject.start_date || '',
        end_date: selectedProject.end_date || '',
        project_type: selectedProject.project_type || 'shortTerm',
        members: selectedProject.members || []
      });
    }
  }, [selectedProject]);

  const handleSaveProject = async () => {
    const projectData = {
      ...newProject,
      end_date: newProject.end_date || null,
      members: newProject.members.length > 0 ? newProject.members : null,
    };

    if (selectedProject) {
      await updateProject(selectedProject.id, projectData);
    } else {
      await createProject(projectData);
    }

    fetchProjects().then((updatedProjects) => {
      setProjects(updatedProjects);
      setFilteredProjects(updatedProjects);
    });
    setSelectedProject(null);
    setIsCreating(false);
    setNewProject({ title: '', description: '', start_date: '', end_date: '', project_type: 'shortTerm', members: [] });
  };

  const handleDelete = async (id: string) => {
    await deleteProject(id);
    fetchProjects().then((updatedProjects) => {
      setProjects(updatedProjects);
      setFilteredProjects(updatedProjects);
    });
  };

  const startIdx = (currentPage - 1) * itemsPerPage;
  const paginatedProjects = filteredProjects.slice(startIdx, startIdx + itemsPerPage);

  return (
    <div className="projects-tab">
      <div className="projects-header">
        <TextField
          label="Search Projects"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          variant="outlined"
        />
        <Button variant="contained" color="primary" onClick={() => setIsCreating(true)}>
          Create Project
        </Button>
      </div>

      {filteredProjects.length > 0 ? (
        <List className="project-list">
          {paginatedProjects.map((project) => (
            <ListItem key={project.id} button onClick={() => setSelectedProject(project)}>
              <ListItemText primary={project.title} />
              {project.description && (
                <Button variant="outlined" color="primary" onClick={() => setSelectedProject(project)}>
                  Details
                </Button>
              )}
            </ListItem>
          ))}
        </List>
      ) : (
        <p>No projects available</p>
      )}

      <div className="pagination">
        <Button disabled={currentPage === 1} onClick={() => setCurrentPage(currentPage - 1)}>
          Previous
        </Button>
        <span>{`Page ${currentPage} of ${Math.ceil(filteredProjects.length / itemsPerPage)}`}</span>
        <Button
          disabled={currentPage === Math.ceil(filteredProjects.length / itemsPerPage)}
          onClick={() => setCurrentPage(currentPage + 1)}
        >
          Next
        </Button>
      </div>

      {/* Project Details / Edit Dialog */}
      <Dialog open={!!selectedProject || isCreating} onClose={() => setSelectedProject(null)}>
        <DialogTitle>{selectedProject ? 'Edit Project' : 'Create Project'}</DialogTitle>
        <DialogContent>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                label="Title"
                fullWidth
                value={newProject.title}
                onChange={(e) => setNewProject({ ...newProject, title: e.target.value })}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                label="Description"
                fullWidth
                multiline
                rows={4}
                value={newProject.description}
                onChange={(e) => setNewProject({ ...newProject, description: e.target.value })}
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                label="Start Date"
                type="date"
                fullWidth
                InputLabelProps={{ shrink: true }}
                value={newProject.start_date}
                onChange={(e) => setNewProject({ ...newProject, start_date: e.target.value })}
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                label="End Date"
                type="date"
                fullWidth
                InputLabelProps={{ shrink: true }}
                value={newProject.end_date}
                onChange={(e) => setNewProject({ ...newProject, end_date: e.target.value })}
              />
            </Grid>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Project Type</InputLabel>
                <Select
                  value={newProject.project_type}
                  onChange={(e) => setNewProject({ ...newProject, project_type: e.target.value })}
                >
                  <MenuItem value="shortTerm">Short Term</MenuItem>
                  <MenuItem value="longTerm">Long Term</MenuItem>
                  <MenuItem value="continuous">Continuous</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <TextField
                label="Search by Email to Add Members"
                fullWidth
                value={emailSearch}
                onChange={(e) => setEmailSearch(e.target.value)}
              />
              <Autocomplete
                multiple
                options={certifiedUsers}
                getOptionLabel={(option) => option.email}
                onChange={(event, value) => setNewProject({ ...newProject, members: value })}
                renderInput={(params) => <TextField {...params} placeholder="Select members by email" />}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button
            onClick={() => {
              setIsCreating(false);
              setSelectedProject(null);
              setNewProject({ title: '', description: '', start_date: '', end_date: '', project_type: 'shortTerm', members: [] });
            }}
            color="secondary"
          >
            Cancel
          </Button>
          <Button onClick={handleSaveProject} color="primary">Save</Button>
          {selectedProject && (
            <Button onClick={() => handleDelete(selectedProject.id)} color="error">
              Delete
            </Button>
          )}
        </DialogActions>
      </Dialog>
    </div>
  );
};

export default TeamAdminProjectsTab;
