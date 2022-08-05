import React from "react";

import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
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
    const matches = useStore((state) => state.Matches);
    const fetch = useStore(state => state.fetch);
    // const [showTable, setShowTable] = useState(false);
    // setShowTable(false);

    return (
        <React.Fragment>
            <CssBaseline />
            <Box
                sx={{
                    display: 'flex',
                    flexWrap: 'wrap',
                    '& > :not(style)': {
                        m: 1,
                    },
                }}
            >
                <Title>Recent Matches</Title>
                <Button
                    fullWidth
                    variant='outlined'
                    color='primary'
                    onClick={() => { fetch(uri) }}
                >
                    Fetch matches
                </Button>
                <Paper style={{ maxHeight: 500, overflow: 'auto' }}>
                    {matches.length ? (
                        <Table size="small">
                            <TableHead>
                                <TableRow>
                                    {Object.entries(matches[matches.length - 1]).map(([k, _]) =>
                                        {return !k.includes('_id') ? <TableCell key={k}>{k}</TableCell> : null}
                                    )}
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {matches.map((row) => (
                                    <TableRow key={row._id}>
                                        {Object.entries(row).map(([k, v]) =>
                                            {return !k.includes('_id') ? <TableCell key={k}>{v}</TableCell> : null}
                                        )}
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    ) : null}
                </Paper>
                <Link color="primary" href="#" onClick={preventDefault} sx={{ mt: 3 }}>
                    See more matches
                </Link>
            </Box>
        </React.Fragment >
    );
}

