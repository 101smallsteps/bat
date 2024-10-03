import { Link } from "react-router-dom";
import "./menu.scss";
import { menu } from "../../data_bat";

const Menu = () => {
  return (
    <div className="menu">
      {menu.map((item) => (
        <div className="item" key={item.id}>
          <Link to={item.url} className="listItem">
            <img src={item.icon} alt={item.title} className="icon" />
            <span className="title">{item.title}</span>
          </Link>
        </div>
      ))}
    </div>
  );
};

export default Menu;
