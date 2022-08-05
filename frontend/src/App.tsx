import React from 'react';
import './App.css';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import SummarizeIcon from '@mui/icons-material/Summarize';

// import Dashboard from './components/Dashboard'
// import Person from './components/Person';
// import Todo from './components/Todo'
// import Vote from './components/Vote';
import Match from './components/Match';

function App() {
    return (
        <>
            <AppBar position="static">
                <Toolbar variant="dense">
                <SummarizeIcon sx={{ mr: 2 }} />
                    <Typography variant="h5" color="inherit" component="div">
                        TFTChamp
                    </Typography>
                    <Box sx={{ flexGrow: 1 }} />
                </Toolbar>
            </AppBar>
            {/* <Dashboard /> */}
            <Match />
            {/* <Todo />
            <Person />
            <Vote /> */}
        </>
    );
}

export default App;