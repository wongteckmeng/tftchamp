import React from "react";

import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
// import Button from '@mui/material/Button';
import TableContainer from '@mui/material/TableContainer';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableFooter from "@mui/material/TableFooter";
import TableRow from '@mui/material/TableRow';
import TablePagination from '@mui/material/TablePagination';
import Skeleton from '@mui/material/Skeleton';

import Title from './Title';
import useStore from '../store/MatchStore';
// import {usePrevious} from '../store/usePrevious';

// function preventDefault(event) { //: React.MouseEvent
//     event.preventDefault();
// }

export default function Match() {
    const [page, setPage] = React.useState(0);
    const [rowsPerPage, setRowsPerPage] = React.useState(100);

    const count = useStore((state) => state.count);
    const matches = useStore((state) => state.Matches);
    const fetch = useStore((state) => state.fetch);
    // const [showTable, setShowTable] = useState(false);
    // setShowTable(false);
    const uri = `http://localhost:8000/match/?platform=na1&skip=${page * rowsPerPage}&limit=${rowsPerPage}`;
    const handleChangePage = (event, newPage) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setPage(0);
        setRowsPerPage(+event.target.value);
    };

    // const prevPageRef = usePrevious(page)

    React.useEffect(() => {
        // console.log(page, prevPageRef, matches.length)
        if ((page*rowsPerPage) >= (matches.length)) { fetch(uri); }

    }, [fetch, uri, page, rowsPerPage, matches.length]);

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
                {/* <Button
                    fullWidth
                    variant='outlined'
                    color='primary'
                    onClick={() => { setPage(0);fetch(uri); }}
                >
                    Fetch matches
                </Button> */}
                <Paper sx={{ width: '100%', overflow: 'hidden' }}>
                    {matches.length ? (
                        <TableContainer sx={{ maxHeight: 700 }}>
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
                    ) : (<Skeleton variant="rectangular" width="100%" height={300} />)}
                </Paper>
                <TablePagination
                    component="div"
                    count={count}
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

