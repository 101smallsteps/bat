import { useEffect,useState } from "react";
import "./portfolio.scss";
import DataTable from "../../components/dataTable/DataTable";
import AddSymbol from "../../components/addSymbol/AddSymbol";
import Search from "../../components/search/Search";
import { GridColDef } from "@mui/x-data-grid";
import { portfolio } from "../../data_bat";
import { products } from "../../data";

import axios from "axios";

const columns: GridColDef[] = [
  { field: "id", headerName: "ID", width: 90 },
  {
    field: "SymbolName",
    type: "string",
    headerName: "Symbol",
    width: 250,
  },
  {
    field: "CompanyName",
    type: "string",
    headerName: "CompanyName",
    width: 150,
  }
];

const getToken = ()=> {
   var auth_token =window.localStorage.getItem("bat.auth");
    var n_tok=auth_token.replace(/"/g, "");
   return n_tok;
};

const retrieveSymbols = async () => {
    try {
        var tok="Token "+getToken();
        //let tok_str='Token a8a31d16b64a1fa1e02de3401d2a78a1738977cd';
        console.log("token->"+tok);
        const response = await axios.get(
            "http://localhost:8080/api/fin/api/symbols/",
            {
                'headers':{
                    "Content-Type": "application/json",
                    "Authorization": `${tok}`
                }
            }
        );
        console.log(response);
        return {response,isError:false};
    }
    catch (error){
        return {error,isError:true};
    }
};

const retrievePortfolio = async () => {
    try {
        var tok="Token "+getToken();
        //let tok_str='Token a8a31d16b64a1fa1e02de3401d2a78a1738977cd';
        console.log("token->"+tok);
        const response = await axios.get(
            "http://localhost:8080/api/fin/api/portfolio/",
            {
                'headers':{
                    "Content-Type": "application/json",
                    "Authorization": `${tok}`
                }
            }
        );
        console.log(response);
        return {response,isError:false};
    }
    catch (error){
        return {error,isError:true};
    }
};


const Portfolio = () => {
  const [portfolioData,setPortfolioData] = useState([]);
  const [symbolData,setSymbolData] = useState([]);
  const [open, setOpen] = useState(false);


  // TEST THE API
  useEffect(() => {
    const fetchPortfolio = async () => {
      const { response, isError } = await retrievePortfolio();
      if (isError) {
        setPortfolioData([]);
        if (response.response) {
            return <div>An error occurred: {response.response.status}</div>;
        }
        else if (response.request) {
            return <div>An error occurred:Network error: {response.request}</div>;
        }
        else {
            return <div>An error occurred: {response.message}</div>;
        }

      } else {
        console.log(response);
        if (response) {
            console.log(response.data);

            const portfolioData=response.data.map((element) => {
                return{
                    'id':element.symbol.id,
                    'SymbolName':element.symbol.symbolName,
                    'CompanyName':element.symbol.companyName
                };

            });
            console.log(portfolioData);
            console.log("extracted_data-1= "+portfolioData);
            setPortfolioData(portfolioData);

        }
        else{
            console.log("no response");
        }
        ;
      }
    };
    fetchPortfolio();
  }, []);


  useEffect(() => {
    const fetchSymbols = async () => {
      const { response, isError } = await retrieveSymbols();
      if (isError) {
        setSymbolData([]);
        if (response.response) {
            return <div>An error occurred: {response.response.status}</div>;
        }
        else if (response.request) {
            return <div>An error occurred:Network error: {response.request}</div>;
        }
        else {
            return <div>An error occurred: {response.message}</div>;
        }

      } else {
        console.log(response);
        if (response) {
            console.log("Symbol Dataaaaa");
            console.log(response.data);

            const extracted_data=response.data.map((element) => {
                return{
                    'id':element.id,
                    'symbolName':element.symbolName,
                    'companyName':element.companyName
                };

            });
            console.log(extracted_data);
            console.log("extracted_data-2= "+extracted_data);
            setSymbolData(extracted_data);

        }
        else{
            console.log("no response");
        }
        ;
      }
    };
    fetchSymbols();
  }, []);

const initialDetails = [
  {
    id: 1,
    imgPath: "/assets/img/1.png",
    name: "Jane Doe",
    email: "janedoe@gmail.com",
    address: "New Delhi, India",
  },
  {
    id: 2,
    imgPath: "/assets/img/2.png",
    name: "Mary Rosamund",
    email: "agra@rosie.com",
    address: "Tbilisi, India",
  },
  ];

  return (
    <div className="portfolio">
      <div className="info">
        <h1>My Portfolio</h1>

      </div>
      <DataTable slug="portfolio" columns={columns} rows={portfolioData}  clickaction="no"/>

      <Search details={symbolData} />
    </div>
  );
};

//{open && <AddSymbol slug="portfolio" columns={columns} setOpen={setOpen} />}
export default Portfolio;
