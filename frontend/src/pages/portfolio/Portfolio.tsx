import { useEffect,useState } from "react";
import "./portfolio.scss";
import DataTable from "../../components/dataTable/DataTable";
import AddSymbol from "../../components/addSymbol/AddSymbol";
import Search from "../../components/search/Search";
import { GridColDef } from "@mui/x-data-grid";
import { portfolio } from "../../data_bat";
import { products } from "../../data";
import config from '../../config';
import axios from "axios";

const columns: GridColDef[] = [
  { field: "id", headerName: "ID", width: 90 },
  {
    field: "Symbol",
    type: "string",
    headerName: "Symbol",
    width: 250,
  },
  {
    field: "CompanyName",
    type: "string",
    headerName: "CompanyName",
    width: 150,
  },
  {
    field: "updatedAt",
    headerName: "Updated At",
    width: 200,
    type: "string",
  },

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
        const backend_server = config.backend_server;
        const response = await axios.get(
            `${backend_server}/api/fin/api/symbols/`,
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

const retrieveAnalysis = async () => {
    try {
        var tok="Token "+getToken();
        const backend_server = config.backend_server;
        //let tok_str='Token a8a31d16b64a1fa1e02de3401d2a78a1738977cd';
        console.log("token->"+tok);
        const response = await axios.get(
             `${backend_server}/api/fin/api/symanalysis/`,
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
    catch (error) {
        console.log(error);
        return {error,isError:true};
    }
};

const retrievePortfolio = async () => {
    try {
        var tok="Token "+getToken();
        //let tok_str='Token a8a31d16b64a1fa1e02de3401d2a78a1738977cd';
        console.log("token->"+tok);
        const backend_server = config.backend_server;
        const response = await axios.get(
            `${backend_server}/api/fin/api/portfolio/`,
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
  const [analysisData,setAnalysisData] = useState([]);
  const [mergedData, setMergedData] = useState([]);
  const [symbolData,setSymbolData] = useState([]);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const fetchAnalysisData = async () => {
      const {  response, isError } = await retrieveAnalysis();
      if (isError) {
        console.log('error occured');
        setAnalysisData([]);
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
        if (response) {
            console.log(response.data);


            const extracted_data=response.data.map((element) => {
                return{
                    'AnalysisStatus':element.AnalysisStatus,
                    'Symbol':element.symbol.symbolName,
                    'CompanyName':element.symbol.companyName,
                    'updatedAt':element.updated_date
                };

            });
            console.log(analysisData);
            console.log(extracted_data);
            if (extracted_data.length > 0)
            {
                setAnalysisData(extracted_data);
            }
            else{
                const dummy_data=[
                    {
                    'AnalysisStatus':"",
                    'Symbol':"",
                    'sid':'',
                    'CompanyName':""
                    }
                ];
                setAnalysisData(dummy_data);
            }
        };
      }
    };
    fetchAnalysisData();
  }, []);

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

  // Merge AnalysisData and PortfolioData by Symbol
  useEffect(() => {
    const mergeData = () => {
      const merged = analysisData.map((analysisItem) => {
        const portfolioItem = portfolioData.find(
          (portfolio) => portfolio.SymbolName === analysisItem.Symbol
        );

        return {
          ...analysisItem,
          id: portfolioItem ? portfolioItem.id : null,
          PortfolioCompanyName: portfolioItem ? portfolioItem.CompanyName : null,
        };
      });
      console.log(merged)
      setMergedData(merged);
    };

    if (analysisData.length > 0 && portfolioData.length > 0) {
      mergeData();
    }
  }, [analysisData, portfolioData]);


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
      <Search details={symbolData} />
      <DataTable slug="portfolioAnalysis" columns={columns} rows={mergedData}  />
      {open && <Add slug="product" columns={columns} setOpen={setOpen} />}

    </div>
  );
};

//{open && <AddSymbol slug="portfolio" columns={columns} setOpen={setOpen} />}
export default Portfolio;
