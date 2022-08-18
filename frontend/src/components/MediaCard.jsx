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

import { useMetadataStore } from '../store/MetadataStore';

export default function MediaCard() {
    // type image = {
    //     uri: string;
    //     description: string;
    //   };

    const region = useMetadataStore(state => state.region);
    const league = useMetadataStore(state => state.league)
    const latest_version = useMetadataStore(state => state.latest_version);
    const latest_patch = useMetadataStore(state => state.latest_patch)
    const setVersion = useMetadataStore(state => state.setVersion);
    const setPatch = useMetadataStore(state => state.setPatch)

    const [images, setImages] = React.useState([]);
    const [isLoading, setIsLoading] = React.useState(true);

    React.useEffect(() => {
        let canceled = false;
        setIsLoading(true);

        const metadataBase = `http://localhost:8000/metadata`;
        const imageBase = `http://localhost:8000/image/`;
        const imageQuery = `?platform=${region}&league=${league}&version=${latest_version}&patch=${latest_patch}`;
        const uri = `${imageBase}${imageQuery}`

        async function getImages(uri) {
            if (!canceled) {

                const metadata_response = await fetch(metadataBase);
                const metadata = await (metadata_response.json());
                setVersion(metadata.latest_version)
                setPatch(metadata.latest_patch)

                const response = await fetch(uri);
                const data = await (response.json());
                setImages(data.results.map(image => ({ ...image, url: imageBase + image.uri + imageQuery })));
                setIsLoading(false);
            }
        }

        getImages(uri);
        return () => canceled = true;
    }, [region, league, latest_version, latest_patch, setVersion, setPatch])


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
                {!isLoading ? (
                    images.map((image) => (
                        <Card key={image.uri} sx={{ maxWidth: 1200, minHeight: '500' }}>
                            <CardContent>
                                <Typography gutterBottom variant="h4" component="div">
                                    {image.uri}
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                    {image.description}
                                </Typography>
                            </CardContent>
                            <CardMedia
                                component="img"
                                image={image.url}
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
