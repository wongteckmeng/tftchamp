import React from 'react';
import './App.css';
import Dashboard from './components/Dashboard'
import Person from './components/Person';
import Vote from './components/Vote';

function App() {
    return (
        <>
            {/* <Dashboard /> */}
            <Person />
            <Vote />
        </>
    );
}

export default App;