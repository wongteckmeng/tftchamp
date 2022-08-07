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
import TableFooter from "@mui/material/TableFooter";
import TableRow from '@mui/material/TableRow';
import TablePagination from '@mui/material/TablePagination';

import Title from './Title';
import useStore from '../store/MatchStore';


function preventDefault(event) { //: React.MouseEvent
    event.preventDefault();
}

export default function Match() {
    const [page, setPage] = React.useState(0);
    const [rowsPerPage, setRowsPerPage] = React.useState(25);
    const matches = useStore((state) => state.Matches);
    const fetch = useStore(state => state.fetch);
    // const [showTable, setShowTable] = useState(false);
    // setShowTable(false);
    const uri = `http://localhost:8000/match/?platform=na1&skip=${page}&limit=${rowsPerPage}`;
    const handleChangePage = (event, newPage) => {
        setPage(newPage);
        fetch(uri)
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(parseInt(event.target.value, 25));
        setPage(0);
        fetch(uri)
    };

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
                                    {Object.entries(matches[matches.length - 1]).map(([k, _]) => { return !k.includes('_id') ? <TableCell key={k}>{k}</TableCell> : null }
                                    )}
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {matches.map((row) => (
                                    <TableRow key={row._id}>
                                        {Object.entries(row).map(([k, v]) => { return !k.includes('_id') ? <TableCell key={k}>{v}</TableCell> : null }
                                        )}
                                    </TableRow>
                                ))}
                            </TableBody>
                            <TableFooter>
                                <TablePagination

                                    count={matches.length}
                                    page={page}
                                    onPageChange={handleChangePage}
                                    rowsPerPage={rowsPerPage}
                                    onRowsPerPageChange={handleChangeRowsPerPage}
                                />
                            </TableFooter>
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

