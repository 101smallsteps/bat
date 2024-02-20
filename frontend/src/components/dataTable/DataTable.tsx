import {
  DataGrid,
  GridColDef,
  GridToolbar,
} from "@mui/x-data-grid";
import "./dataTable.scss";
import { Link } from "react-router-dom";
// import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useEffect,useState } from "react";
import axios from "axios";
import React from 'react';

const getToken = ()=> {
   var auth_token =window.localStorage.getItem("bat.auth");
    var n_tok=auth_token.replace(/"/g, "");
   return n_tok;
};

type Props = {
  columns: GridColDef[];
  rows: object[];
  slug: string;
  clickaction: string;
};

const DataTable = (props: Props) => {

  // TEST THE API

  // const queryClient = useQueryClient();
  // // const mutation = useMutation({
  // //   mutationFn: (id: number) => {
  // //     return fetch(`http://localhost:8800/api/${props.slug}/${id}`, {
  // //       method: "delete",
  // //     });
  // //   },
  // //   onSuccess: ()=>{
  // //     queryClient.invalidateQueries([`all${props.slug}`]);
  // //   }
  // // });

  const handleDelete = async (id: number) => {
    console.log("delete symbol with id "+id);
    //delete the item
    // mutation.mutate(id)
       try {
            var tok="Token "+getToken();
            //let tok_str='Token a8a31d16b64a1fa1e02de3401d2a78a1738977cd';
            console.log("token->"+tok);
            const response = await axios.delete(
                `http://localhost:8080/api/fin/api/portfolio/${id}/`,
                {
                    'headers':{
                        "Content-Type": "application/json",
                        "Authorization": `${tok}`
                    }

                }
            );
            console.log(response);
            window.location.reload();
            return {response,isError:false};
        }
        catch (error){
            return {error,isError:true};
        }

  };

  const actionColumn: GridColDef = {
    field: "action",
    headerName: "Action",
    width: 200,
    renderCell: (params) => {
        if (props.clickaction == "no")
        {
          return (
            <div className="action">
              <div className="delete" onClick={() => handleDelete(params.row.id)}>
                <img src="/delete.svg" alt="" />
              </div>
            </div>
          );
        }
        else
        {
          return (
            <div className="action">
              <Link to={`/${props.slug}/${params.row.sid}`}>
                <img src="/view.svg" alt="" />
              </Link>
            </div>
          );
        }
    },
  };

  return (
    <div className="dataTable">
      <DataGrid
        className="dataGrid"
        rows={props.rows}
        columns={[...props.columns, actionColumn]}
        initialState={{
          pagination: {
            paginationModel: {
              pageSize: 10,
            },
          },
        }}
        slots={{ toolbar: GridToolbar }}
        slotProps={{
          toolbar: {
            showQuickFilter: true,
            quickFilterProps: { debounceMs: 500 },
          },
        }}
        pageSizeOptions={[5]}
        checkboxSelection
        disableRowSelectionOnClick
        disableColumnFilter
        disableDensitySelector
        disableColumnSelector
      />
    </div>
  );
};

export default DataTable;
