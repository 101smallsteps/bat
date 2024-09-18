import { useEffect,useState } from "react";
import "./portfolioAnalysis.scss";
import DataTable from "../../components/dataTable/DataTable";
import Add from "../../components/add/Add";
import { GridColDef } from "@mui/x-data-grid";
import { symbolAnalysis } from "../../data_bat";
import axios from "axios";
import config from '../../config';

//axios.interceptors.response.use(
 // response => response,
//  error => {
//    if (error.response.status === 401) {
//      window.location.href = '/';
//    }
//  });

const columns: GridColDef[] = [
  { field: "id", headerName: "ID", width: 150 },
  {
    field: "AnalysisStatus",
    headerName: "Analysis Status",
    width: 150,
    renderCell: (params) => {
           console.log("rendercell")
           console.log(params.row)
           if (params.row.AnalysisStatus == 'GOOD')
           {
             return <img src={"/good.svg"} alt="" />;
           }
           else if (params.row.AnalysisStatus == 'BAD')
           {
             return <img src={"/bad.svg"} alt="" />;
           }
           else if (params.row.AnalysisStatus == 'WARNING')
           {
             return <img src={"/ok.svg"} alt="" />;
           }
    },

  },
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
//"Authorization": 'Token a8a31d16b64a1fa1e02de3401d2a78a1738977cd'
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

const PortfolioAnalysis = () => {
  const [analysisData,setAnalysisData] = useState([]);
  const [open, setOpen] = useState(false);


  // TEST THE API
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
                    'id':element.id,
                    'AnalysisStatus':element.AnalysisStatus,
                    'Symbol':element.symbol.symbolName,
                    'sid':element.symbol.id,
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
                    'id':"",
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

  return (
    <div className="portfolioAnalysis">
      <div className="info">
        <h1>Analysis</h1>
        <button onClick={() => setOpen(true)}>Add New Products</button>
      </div>

      <DataTable slug="portfolioAnalysis"  columns={columns} rows={analysisData} clickaction="yes"/>

      {open && <Add slug="product" columns={columns} setOpen={setOpen} />}
    </div>
  );
};

export default PortfolioAnalysis;
