import BarChartBox from "../../components/barChartBox/BarChartBox";
import BigChartBox from "../../components/bigChartBox/BigChartBox";
import ChartBox from "../../components/chartBox/ChartBox";
import PieChartBox from "../../components/pieCartBox/PieChartBox";
import Top10 from "../../components/top10/Top10";
import { Navigate } from 'react-router-dom';

import {
  barChartBoxUsers,
  barChartBoxVisit,
  chartBoxConversion,
  chartBoxProduct,
  chartBoxRevenue,
  chartBoxUser,
  barChartBoxRevenue,
  valueCompanies,
  growthCompanies,
  dividendCompanies
} from "../../data_bat";
import "./home.scss";


const Courses = (props) => {

 console.log("Home");
  return (
        <div className="Courses">
            Welcome ! Please check the portfolio menu
        </div>
      );

//  return (
//        <div className="home">
//          <div className="box box1">
//          </div>
//          <div className="box box1">
//            <Top10 data={growthCompanies} head={"growth Companies"}/>
//          </div>
//          <div className="box box1">
//            <Top10 data={dividendCompanies} head={"dividend Companies"}/>
//          </div>
//        </div>
//      );
};

export default Courses
;
