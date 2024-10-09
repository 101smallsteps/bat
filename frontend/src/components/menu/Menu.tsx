import { Link } from "react-router-dom";
import "./menu.scss";
import { menu } from "../../data_bat";

// Pass userData as a prop to check if the user is a SuperUser
const Menu = ({ userData }) => {
 console.log("userData in Menu:", userData);

  return (
    <div className="menu">
      {menu.map((item) => (
        // Conditionally render the NewApplications item if the user is a SuperUser
        (item.title !== "New Applications" || userData?.isSuperUser) && (
          <div className="item" key={item.id}>
            <Link to={item.url} className="listItem">
              <img src={item.icon} alt={item.title} className="icon" />
              <span className="title">{item.title}</span>
            </Link>
          </div>
        )
      ))}
    </div>
  );
};

export default Menu;
