import * as React from 'react';

import CssBaseline from '@mui/material/CssBaseline';
import Button from '@mui/material/Button';
import Link from '@mui/material/Link';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';

import Title from './Title';
import useStore from '../store/MatchStore';

const uri = "http://localhost:8000/match/?platform=na1&skip=0&limit=20";
function preventDefault(event) { //: React.MouseEvent
    event.preventDefault();
}

export default function Match() {
    const matches = useStore((state) => state.Matches)
    const fetch = useStore(state => state.fetch)
    // const { uri, Matches, fetch } = useStore();

    return (
        <React.Fragment>
            <CssBaseline />
            <Title>Recent Matches</Title>
            <Button
                    fullWidth
                    variant='outlined'
                    color='primary'
                    onClick={() => { fetch(uri) }}
                >
                    Fetch matches
                </Button>
            <Table size="small">
                <TableHead>
                    <TableRow>
                        <TableCell>placement</TableCell>
                        <TableCell>augment0</TableCell>
                        <TableCell>augment1</TableCell>
                        <TableCell>augment2</TableCell>
                        <TableCell align="right">Set7_Astral</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {matches.map((row) => (
                        <TableRow key={row._id}>
                            <TableCell>{row.placement}</TableCell>
                            <TableCell>{row.augment0}</TableCell>
                            <TableCell>{row.augment1}</TableCell>
                            <TableCell>{row.augment2}</TableCell>
                            <TableCell align="right">lvl {row.Set7_Astral}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
            <Link color="primary" href="#" onClick={preventDefault} sx={{ mt: 3 }}>
                See more orders
            </Link>
        </React.Fragment>
    );
}

