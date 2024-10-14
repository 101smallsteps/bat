import config from '../config';
import axios from "axios";

const getToken = ()=> {
   var auth_token =window.localStorage.getItem("bat.auth");
    var n_tok=auth_token.replace(/"/g, "");
   return n_tok;
};


export const fetchUserDetails = async (userId: number) => {
  try {
    const response = await axios.get(`${config.backend_server}/api/team/user-details/by-user/${userId}/`, {
      headers: {
        "Authorization": `Token ${getToken()}`,
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching fetchUserDetails", error);
    throw error;
  }
};

export const fetchTaskOwnershipHistory = async (userId: number) => {
  try {
    const response = await axios.get(`${config.backend_server}/api/team/task-ownership-history/by-user/${userId}/`, {
      headers: {
        "Authorization": `Token ${getToken()}`,
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetchTaskOwnershipHistory", error);
    throw error;
  }

};

export const getCurrentUser = async () => {
  try {
    const response = await axios.get(`${config.backend_server}/api/auth/user/`, {
      headers: {
        "Authorization": `Token ${getToken()}`,
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching current user", error);
    throw error;
  }
};

// API call to fetch volunteer jobs
export const getVolunteerJobs = async () => {
  try {
    var tok="Token "+getToken();
    //let tok_str='Token a8a31d16b64a1fa1e02de3401d2a78a1738977cd';
    console.log("token->"+tok);
    const backend_server = config.backend_server;

    const response = await axios.get(
            `${backend_server}/api/team/jobs/`,
            {
                'headers':{
                    "Content-Type": "application/json",
                    "Authorization": `${tok}`
                }
            }
    );
    return response.data;  // This should return the list of volunteer jobs
  } catch (error) {
    console.error("Error fetching volunteer jobs", error);
    throw error;
  }
};


// API call to fetch volunteer jobs
export const getUserCertificates = async () => {
  try {
    var tok="Token "+getToken();
    //let tok_str='Token a8a31d16b64a1fa1e02de3401d2a78a1738977cd';
    console.log("token->"+tok);
    const backend_server = config.backend_server;

    const response = await axios.get(
            `${backend_server}/api/cert/certificates/`,
            {
                'headers':{
                    "Content-Type": "application/json",
                    "Authorization": `${tok}`
                }
            }
    );
    return response.data;  // This should return the list of volunteer jobs
  } catch (error) {
    console.error("Error fetching UserCertificates", error);
    throw error;
  }
};

// API call to fetch volunteer jobs
export const getStaffApplications = async () => {
  try {
    var tok="Token "+getToken();
    //let tok_str='Token a8a31d16b64a1fa1e02de3401d2a78a1738977cd';
    console.log("token->"+tok);
    const backend_server = config.backend_server;

    const response = await axios.get(
            `${backend_server}/api/team/staff-applications/`,
            {
                'headers':{
                    "Content-Type": "application/json",
                    "Authorization": `${tok}`
                }
            }
    );
    return response.data.results;  // This should return the list of volunteer jobs
  } catch (error) {
    if (error.response) {
      console.error("Detailed backend error response:", error.response.data);  // Log exact error details
    }

    console.error("Error fetching staff-applications", error);
    throw error;
  }
};

// API call to fetch UnassignedSymbol
export const getUnassignedSymbols = async () => {
  try {
    var tok="Token "+getToken();
    //let tok_str='Token a8a31d16b64a1fa1e02de3401d2a78a1738977cd';
    console.log("token->"+tok);
    const backend_server = config.backend_server;

    const response = await axios.get(
            `${backend_server}/api/team/unassigned-symbols/`,
            {
                'headers':{
                    "Content-Type": "application/json",
                    "Authorization": `${tok}`
                }
            }
    );
    return response.data.results;  // This should return the list of volunteer jobs
  } catch (error) {
    if (error.response) {
      console.error("Detailed backend error response:", error.response.data);  // Log exact error details
    }

    console.error("Error fetching staff-applications", error);
    throw error;
  }
};


// API call to fetch volunteer jobs
export const postStaffApplications = async (applicationData: any) => {
  try {
    var tok="Token "+getToken();
    //let tok_str='Token a8a31d16b64a1fa1e02de3401d2a78a1738977cd';
    console.log("token->"+tok);
    console.log("postStaffApplications "+applicationData);
    const backend_server = config.backend_server;

    const response = await axios.post(
            `${backend_server}/api/team/staff-applications/`,
            applicationData,
            {
                'headers':{
                    "Content-Type": "application/json",
                    "Authorization": `${tok}`
                }
            }
    );
    return response;  // This should return the list of volunteer jobs
  } catch (error) {
    if (error.response) {
      console.error("Detailed backend error response:", error.response.data);  // Log exact error details
    }

    console.error("Error fetching staff-applications", error);
    throw error;
  }
};


// API call to fetch volunteer jobs
export const postApproveStaffApplications = async (applicationData: any) => {
  try {
    var tok="Token "+getToken();
    //let tok_str='Token a8a31d16b64a1fa1e02de3401d2a78a1738977cd';
    console.log("token->"+tok);
    console.log("postApproveStaffApplications "+applicationData);
    const backend_server = config.backend_server;
    const { applId, symbol_id } = applicationData;
    const response = await axios.post(
            `${backend_server}/api/team/staff-applications/${applId}/approve/`,
            {symbol_id},
            {
                'headers':{
                    "Content-Type": "application/json",
                    "Authorization": `${tok}`
                }
            }
    );
    return response;  // This should return the list of volunteer jobs
  } catch (error) {
    if (error.response) {
      console.error("Detailed backend error response:", error.response);  // Log exact error details
    }

    console.error("Error fetching staff-applications", error);
    throw error;
  }
};


// API call to fetch volunteer jobs
export const postDisApproveStaffApplications = async (applicationId: number) => {
  try {
    var tok="Token "+getToken();
    //let tok_str='Token a8a31d16b64a1fa1e02de3401d2a78a1738977cd';
    console.log("token->"+tok);
    console.log("postDisApproveStaffApplications "+applicationId);
    const backend_server = config.backend_server;
    const response = await axios.post(
            `${backend_server}/api/team/staff-applications/${applicationId}/disapprove/`,
            null,
            {
                'headers':{
                    "Content-Type": "application/json",
                    "Authorization": `${tok}`
                }
            }
    );
    return response;  // This should return the list of volunteer jobs
  } catch (error) {
    if (error.response) {
      console.error("Detailed backend error response:", error.response);  // Log exact error details
    }

    console.error("Error fetching staff-applications", error);
    throw error;
  }
};


// API call to fetch UnassignedSymbol
export const fetchProjects = async () => {
  try {
    var tok="Token "+getToken();
    //let tok_str='Token a8a31d16b64a1fa1e02de3401d2a78a1738977cd';
    console.log("token->"+tok);
    const backend_server = config.backend_server;

    const response = await axios.get(
            `${backend_server}/api/team/projects/`,
            {
                'headers':{
                    "Content-Type": "application/json",
                    "Authorization": `${tok}`
                }
            }
    );
    return response.data.results;  // This should return the list of volunteer jobs
  } catch (error) {
    if (error.response) {
      console.error("Detailed backend error response:", error.response.data);  // Log exact error details
    }

    console.error("Error fetching projects", error);
    throw error;
  }
};

export const deleteProject = async (id: string) => {
  await fetch(`/api/projects/${id}/`, { method: 'DELETE' });
};


export const createProject = async (projectData: { title: string; description: string; start_date: string; end_date: string; project_type: string; }) => {
  try {
    var tok="Token "+getToken();
    const backend_server = config.backend_server;
    const response = await axios.post(
            `${backend_server}/api/team/projects/`,
            projectData,
            {
                'headers':{
                    "Content-Type": "application/json",
                    "Authorization": `${tok}`
                }
            }
    );
    return response;  // This should return the list of volunteer jobs
  } catch (error) {
    if (error.response) {
      console.error("Detailed backend error response:", error.response);  // Log exact error details
    }

    console.error("Error createProject", error);
    throw error;
  }
};


// Update an existing project
export const updateProject = async (id: string, updatedData: { title?: string; description?: string; start_date?: string; end_date?: string; project_type?: string; }) => {
  const response = await fetch(`/api/projects/${id}/`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(updatedData),
  });
  return response.json();
};

export const fetchCertifiedUsersByEmail = async (email) => {
  const response = await fetch(`/api/certified-users/?email=${email}`);
  return response.json();
};

export const fetchTasksForUser = async (userId) => {
  try {
    const tok = "Token " + getToken();
    const backend_server = config.backend_server;

    const response = await axios.get(
      `${backend_server}/api/team/tasks/?user_id=${userId}`, // Include user filter in query
      {
        headers: {
          "Content-Type": "application/json",
          "Authorization": tok,
        },
      }
    );
    console.log(response);
    return response.data; // Return the list of tasks for the specific user
  } catch (error) {
    if (error.response) {
      console.error("Detailed backend error response:", error.response.data);
    }
    console.error("Error fetching tasks", error);
    throw error;
  }
};


export const fetchTasks = async () => {
  try {
    var tok="Token "+getToken();
    //let tok_str='Token a8a31d16b64a1fa1e02de3401d2a78a1738977cd';
    console.log("token->"+tok);
    const backend_server = config.backend_server;

    const response = await axios.get(
            `${backend_server}/api/team/tasks/`,
            {
                'headers':{
                    "Content-Type": "application/json",
                    "Authorization": `${tok}`
                }
            }
    );
    console.log(response);
    return response.data;  // This should return the list of volunteer jobs
  } catch (error) {
    if (error.response) {
      console.error("Detailed backend error response:", error.response.data);  // Log exact error details
    }

    console.error("Error fetching tasks", error);
    throw error;
  }
};

export const fetchUserCompletedOrAcceptedTasks = async () => {
  try {
    const token = `Token ${getToken()}`; // Ensure `getToken` retrieves the current user token
    const backendServer = config.backend_server;

    const response = await axios.get(
      `${backendServer}/api/team/tasks/user-history-completed-accepted/`,
      {
        headers: {
          "Content-Type": "application/json",
          "Authorization": token,
        },
      }
    );

    return response.data; // Returns list of tasks in completed or accepted state for the user
  } catch (error) {
    console.error("Error fetching user completed or accepted tasks", error);
    throw error;
  }
};

export const fetchClosedTasksForUser = async () => {
  try {
    var tok="Token "+getToken();
    //let tok_str='Token a8a31d16b64a1fa1e02de3401d2a78a1738977cd';
    console.log("token->"+tok);
    const backend_server = config.backend_server;

    const response = await axios.get(
            `${backend_server}/api/team/tasks/user-closed-tasks/`,
            {
                'headers':{
                    "Content-Type": "application/json",
                    "Authorization": `${tok}`
                }
            }
    );
    console.log("fetchClosedTasksForUser",response.data);
    return response.data;  // This should return the list of volunteer jobs
  } catch (error) {
    if (error.response) {
      console.error("Detailed backend error response:", error.response.data);  // Log exact error details
    }

    console.error("Error fetching tasks", error);
    throw error;
  }
};

export const updateTaskStatus = async (taskId, data) => {
//  const response = await axios.patch(`/api/tasks/${taskId}/status/`, data);
//  return response.data;
  try {
    var tok="Token "+getToken();
    //let tok_str='Token a8a31d16b64a1fa1e02de3401d2a78a1738977cd';
    console.log("token->"+tok);
    const backend_server = config.backend_server;

    const response = await axios.patch(
            `${backend_server}/api/team/tasks/${taskId}/status/`,
            data,
            {
                'headers':{
                    "Content-Type": "application/json",
                    "Authorization": `${tok}`
                }
            }
    );
    console.log(response);
    return response.data;  // This should return the list of volunteer jobs
  } catch (error) {
    if (error.response) {
      console.error("Detailed backend error response:", error.response.data);  // Log exact error details
    }

    console.error("Error fetching tasks", error);
    throw error;
  }


};

export const addTaskComment_old = async (taskId, comment) => {
  await axios.post(`/api/tasks/${taskId}/comments/`, { comment });
};

// API call to fetch volunteer jobs
export const addTaskComment = async (taskId, comment) => {
  try {
    var tok="Token "+getToken();
    //let tok_str='Token a8a31d16b64a1fa1e02de3401d2a78a1738977cd';
    console.log("token->"+tok);
    console.log("addTaskComment "+taskId);
    console.log("addTaskComment "+comment);

    const backend_server = config.backend_server;
    const response = await axios.post(
            `${backend_server}/api/team/task-comments/`,
            {
                task: taskId,
                comment: comment,
             },
            {
                'headers':{
                    "Content-Type": "application/json",
                    "Authorization": `${tok}`
                }
            }
    );
    return response;  // This should return the list of volunteer jobs
  } catch (error) {
    if (error.response) {
      console.error("Detailed backend error response:", error.response);  // Log exact error details
    }

    console.error("Error fetching staff-applications", error);
    throw error;
  }
};

export const uploadCompletionEvidence = async (taskId, file) => {
  const formData = new FormData();
  formData.append('completion_evidence', file);
  await axios.post(`/api/tasks/${taskId}/upload/`, formData, { headers: { 'Content-Type': 'multipart/form-data' } });
};
