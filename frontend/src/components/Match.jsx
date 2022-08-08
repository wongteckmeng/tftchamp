import React from "react";

import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Button from '@mui/material/Button';
import TableContainer from '@mui/material/TableContainer';
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
    const [rowsPerPage, setRowsPerPage] = React.useState(100);
    const matches = useStore((state) => state.Matches);
    const fetch = useStore(state => state.fetch);
    // const [showTable, setShowTable] = useState(false);
    // setShowTable(false);
    const uri = `http://localhost:8000/match/?platform=na1&skip=${page * rowsPerPage}&limit=${rowsPerPage}`;
    const handleChangePage = (event, newPage) => {
        // fetch(uri)
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        // fetch(uri)
        setRowsPerPage(+event.target.value);
        setPage(0);
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
                <Paper sx={{ width: '100%', overflow: 'hidden' }}>
                    {matches.length ? (
                        <TableContainer sx={{ maxHeight: 550 }}>
                            <Table size="small" stickyHeader aria-label="sticky table">
                                <TableHead>
                                    <TableRow>
                                        {Object.entries(matches[matches.length - 1]).map(([k, _]) => { return !k.includes('_id') ? <TableCell key={k}>{k}</TableCell> : null }
                                        )}
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {matches.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((row) => (
                                        <TableRow key={row._id}>
                                            {Object.entries(row).map(([k, v]) => { return !k.includes('_id') ? <TableCell key={k}>{v}</TableCell> : null }
                                            )}
                                        </TableRow>
                                    ))}
                                </TableBody>
                                <TableFooter>

                                </TableFooter>
                            </Table>
                        </TableContainer>
                    ) : null}
                </Paper>
                <TablePagination
                    component="div"
                    count={matches.length}
                    page={page}
                    onPageChange={handleChangePage}
                    rowsPerPage={rowsPerPage}
                    rowsPerPageOptions={[10, 25, 50, 100]}
                    onRowsPerPageChange={handleChangeRowsPerPage}
                />
            </Box>
        </React.Fragment >
    );
}

