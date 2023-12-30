import "./top10.scss"


const Top10 = (props:Prop) => {
  return (
    <div className="topBox">
      <h1>Top 10 {props.head}</h1>
      <div className="list">
        {props.data.map(sym=>(

            <div className="user">
              <div className="userTexts">
                <span className="username">{sym.id}  {sym.symbol}</span>
               </div>
            </div>


        ))}
      </div>
    </div>

  )
}

export default Top10