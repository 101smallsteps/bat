import Single from "../../components/single/Single"
import Profile from "../../components/profile/Profile"
import { fetchUserDetails, fetchTaskOwnershipHistory } from '../../api/api'; // Adjust based on actual API functions
import { singleUser } from "../../data"
import "./user.scss"
import { useState, useEffect } from "react";


const User = (userData:Prop) => {
  const [userProfileData, setUserProfileData] = useState(null);
  const [userStars, setUserStars] = useState(0);
  const [taskOwnershipHistory, setTaskOwnershipHistory] = useState([]);

  console.log("User");
  console.log(userData.profData.id);
  //Fetch data and send to Single Component
  useEffect(() => {
    // Fetch user profile data
    const getUserProfileData = async () => {
      const profileData = await fetchUserDetails(userData.profData.id); // Fetches UserDetails
      console.log('profileData',profileData);
      setUserProfileData(profileData);
      setUserStars(profileData.stars || 0); // Set stars from UserDetails
    };

    // Fetch task ownership history
    const getTaskOwnershipHistory = async () => {
      const history = await fetchTaskOwnershipHistory(userData.profData.id); // Fetches TaskOwnershipHistory for user
      setTaskOwnershipHistory(history);
    };

    getUserProfileData();
    getTaskOwnershipHistory();
  }, [userData.profData.id]);


  return (
    <div className="user">
      <Profile
        id={userData.profData.id}
        username={userData.profData.username}
        email={userData.profData.email}
        profData={userProfileData}  // User Details data
        stars={userStars}           // Star count from UserDetails model
        taskOwnershipHistory={taskOwnershipHistory} // List of ownership history entries

      />
    </div>
  )
}

export default User