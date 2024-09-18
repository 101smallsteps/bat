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
            <ChartBox {...props.revenue[0]} />
          </div>
          <div className="box box2">
            <ChartBox {...props.grossprofitmargin} />
          </div>
          <div className="box box2">
            <ChartBox {...props.netprofitmargin} />
          </div>
          <div className="box box2">
            <ChartBox {...props.deratio} />
          </div>
          <div className="box box2">
            <ChartBox {...props.tdtaratio} />
          </div>
          <div className="box box2">
            <ChartBox {...props.currentratio} />
          </div>
          <div className="box box2">
            <ChartBox {...props.quickratio} />
          </div>
          <div className="box box2">
            <ChartBox {...props.cashratio} />
          </div>

        </div>
      );
};

export default SingleAnalysis;
