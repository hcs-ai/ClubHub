import React, { useEffect, useState } from 'react';
import Papa from 'papaparse'; //Parsing csv

const DataTable = () => {
    const [data, setData] = useState([]);
  
    useEffect(() => {
      const fetchData = async () => {
        //Loading in the data.csv file 
        const response = await fetch('/data.csv');
        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');
        const { value } = await reader.read();
        const csv = decoder.decode(value);
        
        // Here, we parse CSV data
        Papa.parse(csv, {
          header: true,     
          skipEmptyLines: true, // Ignore empty rows
          complete: (results) => {
            setData(results.data); // Save parsed data to state
          },
        });
      };
  
      fetchData();
    }, []);

  return (
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Age</th>
          <th>Location</th>
        </tr>
      </thead>
      <tbody>
        {data.map((item) => (
          <tr key={item.id}>
            <td>{item.id}</td>
            <td>{item.name}</td>
            <td>{item.age}</td>
            <td>{item.location}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default DataTable;
