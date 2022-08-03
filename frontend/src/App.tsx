import React from 'react';
import './App.css';
import Dashboard from './components/Dashboard'
import Person from './components/Person';
import Todo from './components/Todo'
import Vote from './components/Vote';

function App() {
    return (
        <>
            {/* <Dashboard /> */}
            <Todo />
            <Person />
            <Vote />
        </>
    );
}

export default App;