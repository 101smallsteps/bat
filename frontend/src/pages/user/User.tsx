import Single from "../../components/single/Single"
import Profile from "../../components/profile/Profile"
import { singleUser } from "../../data"
import "./user.scss"

const User = (props:Prop) => {
  console.log("User");
  console.log(props);
  //Fetch data and send to Single Component
  
  return (
    <div className="user">
      <Profile {...props}/>
    </div>
  )
}

export default User