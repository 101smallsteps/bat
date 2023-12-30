import { GridColDef } from "@mui/x-data-grid";
import "./search.scss";
// import { useMutation, useQueryClient } from "@tanstack/react-query";
import React, { useEffect,useState } from "react";
import Scroll from './Scroll';
import SearchList from './SearchList';


import axios from "axios";

const Search = (props: Props) => {

  const [searchField, setSearchField] = useState("");
  const [searchShow, setSearchShow] = useState(true);

  console.log("Rav == ")
  console.log(props.details)
  const filteredSymbols = props.details.filter(
    sym => {
      return (
        sym
        .symbolName
        .toLowerCase()
        .includes(searchField.toLowerCase()) ||
        sym
        .companyName
        .toLowerCase()
        .includes(searchField.toLowerCase())
      );
    }
  );

  const handleChange = e => {
    setSearchField(e.target.value);
    if(e.target.value===""){
      setSearchShow(false);
    }
    else {
      setSearchShow(true);
    }
  };

  function searchList() {
  	if (searchShow) {
	  	return (
	  		<Scroll>
	  			<SearchList filteredSymbols={filteredSymbols} />
	  		</Scroll>
	  	);
	  }
    return null;
  }

  return (
    <section className="garamond">
			<div className="navy georgia ma0 grow">
				<h2 className="f2">Search Symbols</h2>

			</div>
			<div className="pa2">
				<input
					className="pa3 bb br3 grow b--none bg-lightest-blue ma3"
					type = "search"
					placeholder = "Search Symbols"
					onChange = {handleChange}
				/>
			</div>
			{searchList()}
		</section>
  );
}

export default Search;