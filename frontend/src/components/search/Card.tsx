import React from 'react';
import "./card.scss";

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { useEffect,useState } from "react";
import axios from "axios";
import { useHistory } from 'react-router-dom';

const getToken = ()=> {
   var auth_token =window.localStorage.getItem("bat.auth");
    var n_tok=auth_token.replace(/"/g, "");
   return n_tok;
};


const Card = (props: Props) => {
  console.log("card");
  console.log(props);
  const [updatingData,setUpdatingData] = useState([]);



    const AddSymbol = async (p) => {
	  console.log("Add symbol to protfolio requested "+p.symbolName);
	  const post_data={
	  "user_symbol":[
                        {
                        "id":p.id,
                        "symbolName":p.symbolName,
                        "companyName":p.companyName
                        }
                    ]
	  };
       try {
            var tok="Token "+getToken();
            //let tok_str='Token a8a31d16b64a1fa1e02de3401d2a78a1738977cd';
            console.log("token->"+tok);
            const response = await axios.post(
                "http://localhost:8080/api/fin/api/portfolio/",
                post_data,
                {
                    'headers':{
                        "Content-Type": "application/json",
                        "Authorization": `${tok}`
                    }

                }
            );
            window.location.reload();
            return {response,isError:false};
        }
        catch (error){
            return {error,isError:true};
        }
    }

	return(
    <Container fluid="md" className="card">
		<Row>
				<Col> {props.symbol.symbolName} </Col>
				<Col> {props.symbol.companyName} </Col>
				 <Col> <button onClick={() => AddSymbol(props.symbol)}>Add </button></Col>
		</Row>
	</Container>
	);

}

export default Card;