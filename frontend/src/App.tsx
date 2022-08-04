import React from 'react';
import './App.css';
import Dashboard from './components/Dashboard'
import Person from './components/Person';
import Todo from './components/Todo'
import Vote from './components/Vote';
import Match from './components/Match';

function App() {
    return (
        <>
            {/* <Dashboard /> */}
            <Match />
            <Todo />
            <Person />
            <Vote />
        </>
    );
}

export default App;