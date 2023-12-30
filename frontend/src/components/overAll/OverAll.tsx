import "./overAll.scss"
import {overallAnalysis} from "../../data_analysis.ts"

const OverAll = (props: Props) => {
 console.log(props);
 const overallAnalysisDataLen=props.overall?.length>0;
 console.log(overallAnalysisDataLen);
 function getImage(result){
       if (result == "OK") {
            return "/ok.svg";
       }
       else if (result == "GOOD") {
            return "/good.svg";
       }
       else if (result == "BAD") {
            return "/bad.svg";
       }
 }

  return (
    <div className="topBox">
      <h1>Overall</h1>
      <div className="list">
        {
                  overallAnalysisDataLen ? (props.overall.map(result=>(
                  <div className="listItem" key={result.id}>
                    <div className="user">
                      <img src={ getImage(result.analysisResult) } alt="" />
                      <div className="userTexts">
                        <span className="username">{result.metric}</span>
                        <span className="email">{result.analysisResult}</span>
                      </div>
                    </div>
                    <span className="amount">{result.metricDisplay}</span>
                  </div>
                  )
                  )
              ):(<div></div>)
        }
      </div>
    </div>
  )
}

export default OverAll