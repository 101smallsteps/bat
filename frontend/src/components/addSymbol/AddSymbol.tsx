import { GridColDef } from "@mui/x-data-grid";
import "./addSymbol.scss";
// import { useMutation, useQueryClient } from "@tanstack/react-query";
import React, { useEffect,useState } from "react";

import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';

import axios from "axios";

type Props = {
  slug: string;
  columns: GridColDef[];
  setOpen: React.Dispatch<React.SetStateAction<boolean>>;
};

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
        console.log("error");
        return {error,isError:true};
    }
};

const AddSymbol = (props: Props) => {

const [myOptions, setMyOptions] = useState([]);

  useEffect(() => {
    const fetchSymbols = async () => {
      const { response, isError } = await retrieveSymbols();
      if (isError) {
        setMyOptions([]);
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


              for (var i = 0; i < response.data.length; i++) {
                myOptions.push(response.data[i].symbol)
              }
              setMyOptions(myOptions);
              console.log("myOptions="+myOptions);
        }
        else{
            console.log("no response");
        }
        ;
      }
    };
    fetchSymbols();
  }, []);



  // TEST THE API

  // const queryClient = useQueryClient();

  // const mutation = useMutation({
  //   mutationFn: () => {
  //     return fetch(`http://localhost:8800/api/${props.slug}s`, {
  //       method: "post",
  //       headers: {
  //         Accept: "application/json",
  //         "Content-Type": "application/json",
  //       },
  //       body: JSON.stringify({
  //         id: 111,
  //         img: "",
  //         lastName: "Hello",
  //         firstName: "Test",
  //         email: "testme@gmail.com",
  //         phone: "123 456 789",
  //         createdAt: "01.02.2023",
  //         verified: true,
  //       }),
  //     });
  //   },
  //   onSuccess: () => {
  //     queryClient.invalidateQueries([`all${props.slug}s`]);
  //   },
  // });

  return (
    <Autocomplete
      disablePortal
      id="combo-box-demo"
      options={myOptions}
      sx={{ width: 300 }}
      renderInput={(params) => <TextField {...params} label="Search Symbol" />}
    />
  );

};

export default AddSymbol;
