import config from '../config';
import axios from "axios";

const getToken = ()=> {
   var auth_token =window.localStorage.getItem("bat.auth");
    var n_tok=auth_token.replace(/"/g, "");
   return n_tok;
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


// API call to fetch volunteer jobs
export const postStaffApplications = async (applicationData: any) => {
  try {
    var tok="Token "+getToken();
    //let tok_str='Token a8a31d16b64a1fa1e02de3401d2a78a1738977cd';
    console.log("token->"+tok);
    console.log("postStaffApplications"+applicationData);
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



