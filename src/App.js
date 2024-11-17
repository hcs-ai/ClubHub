import React from 'react';
import './App.css';
import DataTable from './Components/DataTable';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Club Directory</h1>
        <p>Find and explore clubs easily</p>
      </header>
      <main>
        <DataTable />
      </main>
    </div>
  );
}

export default App;