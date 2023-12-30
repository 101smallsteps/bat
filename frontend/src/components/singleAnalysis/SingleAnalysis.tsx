import BarChartBox from "../../components/barChartBox/BarChartBox";
import BigChartBox from "../../components/bigChartBox/BigChartBox";
import ChartBox from "../../components/chartBox/ChartBox";
import PieChartBox from "../../components/pieCartBox/PieChartBox";
import OverAll from "../../components/overAll/OverAll";
import "./singleanalysis.scss";


const SingleAnalysis = (props: Props) => {
 console.log(props)
  return (
        <div className="home">
          <div className="box box1">
            <OverAll {...props}/>
          </div>
          <div className="box box2">
            <ChartBox {...props.revenue} />
          </div>
          <div className="box box2">
            <ChartBox {...props.deratio} />
          </div>
          <div className="box box2">
            <ChartBox {...props.currentratio} />
          </div>
        </div>
      );
};

export default SingleAnalysis;
