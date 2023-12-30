import React from 'react';
import Card from './Card';
import "./searchList.scss";

const SearchList = (props: Props) => {
  console.log("SearchList before filter");
  console.log(props.filteredSymbols);
  const filtered = props.filteredSymbols.map( sym =>  <Card key={sym.id} symbol={sym} />);
  console.log("SearchList filtered");
  console.log(filtered);
  return (
    <div className="search-list" >
      {filtered}
    </div>
  );
}

export default SearchList;