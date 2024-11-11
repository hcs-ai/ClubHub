import React from 'react';
import logo from './logo.svg';
import './App.css';
import DataTable from './Components/DataTable'

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <p>
          Here is some more paragraphs for the website
        </p>
        <h2>
          Data Table:
         <DataTable />
        </h2>
      </header>

     
    </div>
  );
}

export default App;
