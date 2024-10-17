import SingleAnalysis from "../../components/singleAnalysis/SingleAnalysis";
//import { singleAnalysisProduct } from "../../data_bat"
import "./analysis.scss"
import axios from "axios";
import { useEffect,useState } from "react";
import React from 'react';
import { useParams } from 'react-router-dom';
import config from '../../config';


import {
  chartBoxRevenue,
  chartBoxDERatio,
//  barChartBoxVisit,
//  chartBoxConversion,
//  chartBoxProduct,
//  chartBoxRevenue,
//  chartBoxUser,
} from "../../data_analysis";

const getToken = ()=> {
   var auth_token =window.localStorage.getItem("bat.auth");
    var n_tok=auth_token.replace(/"/g, "");
   return n_tok;
};


const retrieveOverallAnalysis = async (id:number) => {
          try {
                var tok="Token "+getToken();
                //let tok_str='Token a8a31d16b64a1fa1e02de3401d2a78a1738977cd';
                console.log("token->"+tok);
                const backend_server = config.backend_server;
                const response = await axios.get(
                    `${backend_server}/api/fin/api/overall/${id}/`,
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

const retrieveIncomeStatementTotalRevenue = async (id:number) => {
          try {
                var tok="Token "+getToken();
                //let tok_str='Token a8a31d16b64a1fa1e02de3401d2a78a1738977cd';
                console.log("token->"+tok);
                const backend_server = config.backend_server;
                const response = await axios.get(
                    `${backend_server}/api/fin/api/incstmt/TotalRevenue/${id}/4/`,
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

const retrieveRatioDERatio = async (id:number) => {
          try {
                var tok="Token "+getToken();
                //let tok_str='Token a8a31d16b64a1fa1e02de3401d2a78a1738977cd';
                console.log("token->"+tok);
                const backend_server = config.backend_server;
                const response = await axios.get(
                    `${backend_server}/api/fin/api/ratio/DEratio/${id}/10/`,
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

const retrieveRatioTDTAratio = async (id:number) => {
          try {
                var tok="Token "+getToken();
                //let tok_str='Token a8a31d16b64a1fa1e02de3401d2a78a1738977cd';
                console.log("token->"+tok);
                const backend_server = config.backend_server;
                const response = await axios.get(
                    `${backend_server}/api/fin/api/ratio/TDTAratio/${id}/10/`,
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
const retrieveRatioCurrentratio = async (id:number) => {
          try {
                var tok="Token "+getToken();
                //let tok_str='Token a8a31d16b64a1fa1e02de3401d2a78a1738977cd';
                console.log("token->"+tok);
                const backend_server = config.backend_server;
                const response = await axios.get(
                    `${backend_server}/api/fin/api/ratio/Currentratio/${id}/10/`,
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
const retrieveRatioQuickratio = async (id:number) => {
          try {
                var tok="Token "+getToken();
                //let tok_str='Token a8a31d16b64a1fa1e02de3401d2a78a1738977cd';
                console.log("token->"+tok);
                const backend_server = config.backend_server;
                const response = await axios.get(
                    `${backend_server}/api/fin/api/ratio/Quickratio/${id}/10/`,
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
const retrieveRatioCashratio = async (id:number) => {
          try {
                var tok="Token "+getToken();
                //let tok_str='Token a8a31d16b64a1fa1e02de3401d2a78a1738977cd';
                console.log("token->"+tok);
                const backend_server = config.backend_server;
                const response = await axios.get(
                    `${backend_server}/api/fin/api/ratio/Cashratio/${id}/10/`,
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

const retrieveGrossProfitMargin = async (id:number) => {
          try {
                var tok="Token "+getToken();
                //let tok_str='Token a8a31d16b64a1fa1e02de3401d2a78a1738977cd';
                console.log("token->"+tok);
                const backend_server = config.backend_server;
                const response = await axios.get(
                    `${backend_server}/api/fin/api/ratio/GrossProfitMargin/${id}/10/`,
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

const retrieveNetProfitMargin = async (id:number) => {
          try {
                var tok="Token "+getToken();
                //let tok_str='Token a8a31d16b64a1fa1e02de3401d2a78a1738977cd';
                console.log("token->"+tok);
                const backend_server = config.backend_server;
                const response = await axios.get(
                    `${backend_server}/api/fin/api/ratio/NetProfitMargin/${id}/10/`,
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


const Analysis = () => {
      const [overallAnalysisData,setOverallAnalysisData] = useState([]);
      const [totalRevenueData,setTotalRevenueData] = useState([]);
      const [dERatioData,setDERatioData] = useState([]);
      const [TDTAratioData,setTDTAratioData] = useState([]);
      const [CurrentratioData,setCurrentratioData] = useState([]);
      const [QuickratioData,setQuickratioData] = useState([]);
      const [CashratioData,setCashratioData] = useState([]);
      const [GrossProfitMarginData,setGrossProfitMarginData] = useState([]);
      const [NetProfitMarginData,setNetProfitMarginData] = useState([]);

      const  params = useParams();
      const { id } = params;
      console.log("+++pk++++");
      console.log(id);


      useEffect(() => {
      const fetchoverallAnalysisData = async () => {
          const {  response, isError } = await retrieveOverallAnalysis(id);
          if (isError) {
            console.log('error occured');
                const dummy_data=[
                    {
                    'analysisResult':'',
                    'metric':'',
                    'metricDisplay':''
                    }
                ];
                setOverallAnalysisData(dummy_data);

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

                const extracted_data=response.data.map((element) => {
                    return{
                        'analysisResult':element.analysisResult,
                        'metric':element.metric,
                        'metricDisplay':element.metricDisplay
                    };

                });
                console.log(extracted_data);
                    setOverallAnalysisData(extracted_data);
                    console.log('setoverallAnalysisData');
                    console.log(overallAnalysisData);
          }

    };
    fetchoverallAnalysisData();
  }, []);

      useEffect(() => {
      const fetchtotalRevenueData = async () => {
          const {  response, isError } = await retrieveIncomeStatementTotalRevenue(id);
          if (isError) {
            console.log('error occured');
                const dummy_data=[
                    {
                        color: "teal",
                        icon: "/revenueIcon.svg",
                        title: "Total Revenue dummy",
                        number: "$56.432",
                        dataKey: "revenue",
                        percentage: -12,
                        chartData: [
                            { name: "Sun", revenue: 400 },
                            { name: "Mon", revenue: 600 },
                            { name: "Tue", revenue: 500 },
                            { name: "Wed", revenue: 700 },
                            { name: "Thu", revenue: 400 },
                            { name: "Fri", revenue: 500 },
                            { name: "Sat", revenue: 450 },
                        ],
                    }
                ];
                setTotalRevenueData(dummy_data);

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

                const extracted_data=response.data.map((element) => {
                    return{
                        color: "teal",
                        icon: "/revenueIcon.svg",
                        title: "Total Revenue",
                        number: element['last_metric_value'],
                        dataKey: "metricValue",
                        percentage: element['percentChange'],
                        chartData: element['chartData'],
                    };

                });
                    setTotalRevenueData(extracted_data[0]);
                    console.log('setDERatioData');
                    console.log(extracted_data);
          }

    };
    fetchtotalRevenueData();
  }, []);

      useEffect(() => {
      const fetchDERatioData = async () => {
          const {  response, isError } = await retrieveRatioDERatio(id);
          if (isError) {
            console.log('error occured');
                const dummy_data=[
                    {
                        color: "teal",
                        icon: "/revenueIcon.svg",
                        title: "DE Ratio",
                        number: "$56.432",
                        dataKey: "deratio",
                        percentage: -12,
                        chartData: [
                            { name: "Sun", deratio: 400 },
                            { name: "Mon", deratio: 600 },
                            { name: "Tue", deratio: 500 },
                            { name: "Wed", deratio: 700 },
                            { name: "Thu", deratio: 400 },
                            { name: "Fri", deratio: 500 },
                            { name: "Sat", deratio: 450 },
                        ],
                    }
                    ];
                setDERatioData(dummy_data);

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

                const extracted_data=response.data.map((element) => {
                    return{
                        color: "teal",
                        icon: "/revenueIcon.svg",
                        title: "DE Ratio",
                        number: element['last_metric_value'],
                        dataKey: "metricValue",
                        percentage: element['percentChange'],
                        chartData: element['chartData'],
                    };

                });
                    setDERatioData(extracted_data[0]);
                    console.log('setTotalRevenueData');
                    console.log(extracted_data);
          }

    };
    fetchDERatioData();
  }, []);

      useEffect(() => {
      const fetchTDTAratioData = async () => {
          const {  response, isError } = await retrieveRatioTDTAratio(id);
          if (isError) {
            console.log('error occured');
                const dummy_data=[
                    {
                        color: "teal",
                        icon: "/revenueIcon.svg",
                        title: "DE Ratio",
                        number: "$56.432",
                        dataKey: "deratio",
                        percentage: -12,
                        chartData: [
                            { name: "Sun", deratio: 400 },
                            { name: "Mon", deratio: 600 },
                            { name: "Tue", deratio: 500 },
                            { name: "Wed", deratio: 700 },
                            { name: "Thu", deratio: 400 },
                            { name: "Fri", deratio: 500 },
                            { name: "Sat", deratio: 450 },
                        ],
                    }
                    ];
                setTDTAratioData(dummy_data);

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

                const extracted_data=response.data.map((element) => {
                    return{
                        color: "teal",
                        icon: "/revenueIcon.svg",
                        title: "TD TA ratio",
                        number: element['last_metric_value'],
                        dataKey: "metricValue",
                        percentage: element['percentChange'],
                        chartData: element['chartData'],
                    };

                });
                    setTDTAratioData(extracted_data[0]);
                    console.log('setTotalRevenueData');
                    console.log(extracted_data);
          }

    };
    fetchTDTAratioData();
  }, []);
      useEffect(() => {
      const fetchCurrentratioData = async () => {
          const {  response, isError } = await retrieveRatioCurrentratio(id);
          if (isError) {
            console.log('error occured');
                const dummy_data=[
                    {
                        color: "teal",
                        icon: "/revenueIcon.svg",
                        title: "Current Ratio",
                        number: "$56.432",
                        dataKey: "deratio",
                        percentage: -12,
                        chartData: [
                            { name: "Sun", deratio: 400 },
                            { name: "Mon", deratio: 600 },
                            { name: "Tue", deratio: 500 },
                            { name: "Wed", deratio: 700 },
                            { name: "Thu", deratio: 400 },
                            { name: "Fri", deratio: 500 },
                            { name: "Sat", deratio: 450 },
                        ],
                    }
                    ];
                setCurrentratioData(dummy_data);

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

                const extracted_data=response.data.map((element) => {
                    return{
                        color: "teal",
                        icon: "/revenueIcon.svg",
                        title: "Current ratio",
                        number: element['last_metric_value'],
                        dataKey: "metricValue",
                        percentage: element['percentChange'],
                        chartData: element['chartData'],
                    };

                });
                    setCurrentratioData(extracted_data[0]);
                    console.log('setTotalRevenueData');
                    console.log(extracted_data);
          }

    };
    fetchCurrentratioData();
  }, []);
      useEffect(() => {
      const fetchQuickratioData = async () => {
          const {  response, isError } = await retrieveRatioQuickratio(id);
          if (isError) {
            console.log('error occured');
                const dummy_data=[
                    {
                        color: "teal",
                        icon: "/revenueIcon.svg",
                        title: "Quick Ratio",
                        number: "$56.432",
                        dataKey: "deratio",
                        percentage: -12,
                        chartData: [
                            { name: "Sun", deratio: 400 },
                            { name: "Mon", deratio: 600 },
                            { name: "Tue", deratio: 500 },
                            { name: "Wed", deratio: 700 },
                            { name: "Thu", deratio: 400 },
                            { name: "Fri", deratio: 500 },
                            { name: "Sat", deratio: 450 },
                        ],
                    }
                    ];
                setQuickratioData(dummy_data);

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

                const extracted_data=response.data.map((element) => {
                    return{
                        color: "teal",
                        icon: "/revenueIcon.svg",
                        title: "Quick Ratio",
                        number: element['last_metric_value'],
                        dataKey: "metricValue",
                        percentage: element['percentChange'],
                        chartData: element['chartData'],
                    };

                });
                    setQuickratioData(extracted_data[0]);
                    console.log('setTotalRevenueData');
                    console.log(extracted_data);
          }

    };
    fetchQuickratioData();
  }, []);
      useEffect(() => {
      const fetchCashratioData = async () => {
          const {  response, isError } = await retrieveRatioCashratio(id);
          if (isError) {
            console.log('error occured');
                const dummy_data=[
                    {
                        color: "teal",
                        icon: "/revenueIcon.svg",
                        title: "Cash Ratio",
                        number: "$56.432",
                        dataKey: "deratio",
                        percentage: -12,
                        chartData: [
                            { name: "Sun", deratio: 400 },
                            { name: "Mon", deratio: 600 },
                            { name: "Tue", deratio: 500 },
                            { name: "Wed", deratio: 700 },
                            { name: "Thu", deratio: 400 },
                            { name: "Fri", deratio: 500 },
                            { name: "Sat", deratio: 450 },
                        ],
                    }
                    ];
                setCashratioData(dummy_data);

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

                const extracted_data=response.data.map((element) => {
                    return{
                        color: "teal",
                        icon: "/revenueIcon.svg",
                        title: "Cash Ratio",
                        number: element['last_metric_value'],
                        dataKey: "metricValue",
                        percentage: element['percentChange'],
                        chartData: element['chartData'],
                    };

                });
                    setCashratioData(extracted_data[0]);
                    console.log('setTotalRevenueData');
                    console.log(extracted_data);
          }

    };
    fetchCashratioData();
  }, []);


      useEffect(() => {
      const fetchGrossProfitMarginData = async () => {
          const {  response, isError } = await retrieveGrossProfitMargin(id);
          if (isError) {
            console.log('error occured');
                const dummy_data=[
                    {
                        color: "teal",
                        icon: "/revenueIcon.svg",
                        title: "Cash Ratio",
                        number: "$56.432",
                        dataKey: "deratio",
                        percentage: -12,
                        chartData: [
                            { name: "Sun", deratio: 400 },
                            { name: "Mon", deratio: 600 },
                            { name: "Tue", deratio: 500 },
                            { name: "Wed", deratio: 700 },
                            { name: "Thu", deratio: 400 },
                            { name: "Fri", deratio: 500 },
                            { name: "Sat", deratio: 450 },
                        ],
                    }
                    ];
                setGrossProfitMarginData(dummy_data);

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

                const extracted_data=response.data.map((element) => {
                    return{
                        color: "teal",
                        icon: "/revenueIcon.svg",
                        title: "Gross Profit Margin",
                        number: element['last_metric_value'],
                        dataKey: "metricValue",
                        percentage: element['percentChange'],
                        chartData: element['chartData'],
                    };

                });
                    setGrossProfitMarginData(extracted_data[0]);
                    console.log('setTotalRevenueData');
                    console.log(extracted_data);
          }

    };
    fetchGrossProfitMarginData();
  }, []);

      useEffect(() => {
      const fetchNetProfitMarginData = async () => {
          const {  response, isError } = await retrieveNetProfitMargin(id);
          if (isError) {
            console.log('error occured');
                const dummy_data=[
                    {
                        color: "teal",
                        icon: "/revenueIcon.svg",
                        title: "Cash Ratio",
                        number: "$56.432",
                        dataKey: "deratio",
                        percentage: -12,
                        chartData: [
                            { name: "Sun", deratio: 400 },
                            { name: "Mon", deratio: 600 },
                            { name: "Tue", deratio: 500 },
                            { name: "Wed", deratio: 700 },
                            { name: "Thu", deratio: 400 },
                            { name: "Fri", deratio: 500 },
                            { name: "Sat", deratio: 450 },
                        ],
                    }
                    ];
                setGrossProfitMarginData(dummy_data);

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

                const extracted_data=response.data.map((element) => {
                    return{
                        color: "teal",
                        icon: "/revenueIcon.svg",
                        title: "Net Profit Margin",
                        number: element['last_metric_value'],
                        dataKey: "metricValue",
                        percentage: element['percentChange'],
                        chartData: element['chartData'],
                    };

                });
                    setNetProfitMarginData(extracted_data[0]);
                    console.log('setTotalRevenueData');
                    console.log(extracted_data);
          }

    };
    fetchNetProfitMarginData();
  }, []);

                const dummy_data=[
                    {
                        color: "teal",
                        icon: "/revenueIcon.svg",
                        title: "Current ratio",
                        number: "$56.432",
                        dataKey: "currentratio",
                        percentage: -12,
                        chartData: [
                            { name: "Sun", currentratio: 400 },
                            { name: "Mon", currentratio: 600 },
                            { name: "Tue", currentratio: 500 },
                            { name: "Wed", currentratio: 700 },
                            { name: "Thu", currentratio: 400 },
                            { name: "Fri", currentratio: 500 },
                            { name: "Sat", currentratio: 450 },
                        ],
                    }
                ];

  //Fetch data and send to Single Component
  return (
    <div className="product">
       <SingleAnalysis overall={overallAnalysisData} revenue={totalRevenueData} grossprofitmargin={GrossProfitMarginData} netprofitmargin={NetProfitMarginData} deratio={dERatioData} tdtaratio={TDTAratioData} currentratio={CurrentratioData} quickratio={QuickratioData} cashratio={CashratioData}/>
    </div>
  );
};

export default Analysis