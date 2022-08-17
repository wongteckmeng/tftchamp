import React from "react";
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Skeleton from '@mui/material/Skeleton';

import { useRegionStore } from '../store/RegionStore';

export default function MediaCard() {
    const [images, setImages] = React.useState([]);
    
    const region = useRegionStore((state) => state.region);

    const imageBase = `http://localhost:8000/image/`;
    const imageQuery = `?platform=${region}&league=challengers&version=12.15.458.1416&patch=2022-08-10`;
    const uri = `http://localhost:8000/image/${imageQuery}`

    React.useEffect(() => {
        let canceled = false;
        async function getImages(uri) {
            if (!canceled) {
                const response = await fetch(uri);
                const data = await (response.json());
                setImages(data.results);
            }
        }

        getImages(uri);
        return () => canceled = true;
    }, [uri])


    return (
        <Box
            sx={{
                display: 'flex',
                flexWrap: 'wrap',
                '& > :not(style)': {
                    m: 1,
                },
            }}
        >
            <Paper sx={{ width: '100%', minHeight: '500', overflow: 'hidden' }}>
                {images.length ? (
                    images.map((image) => (
                        <Card key={image.uri} sx={{ maxWidth: 1200, minHeight: '500' }}>
                            <CardContent>
                                <Typography gutterBottom variant="h4" component="div">
                                    {region}_{image.uri}
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                    {image.description}
                                </Typography>
                            </CardContent>
                            <CardMedia
                                component="img"
                                image={imageBase + image.uri + imageQuery}
                                alt={image.uri}
                            />

                            <CardActions>
                                <Button size="small">Share</Button>
                                <Button size="small">Learn More</Button>
                            </CardActions>
                        </Card>
                    ))
                ) : (<Skeleton variant="rectangular" width="100%" height={300} />)}
            </Paper >

        </Box >
    );
}
