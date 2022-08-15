import React from "react";
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';

export default function MediaCard() {
    const uri = "http://localhost:8000/image/na1_challengers_12.15.458.1416_2022-08-10_feature_importances?platform=na1&league=challengers&version=12.15.458.1416&patch=2022-08-10";
    // const [image, setImage] = React.useState([])  

    // useEffect(() => {
    //     fetch: async (uri) => { //: RequestInfo | URL
    //     const response = await fetch(uri);
    //     setImage(response)

    // }, [uri]); 

    return (
        <Card sx={{ maxWidth: 1000 }}>
            <CardMedia
                component="img"
                image={uri}
                alt="Feature Importance"
            />
            <CardContent>
                <Typography gutterBottom variant="h5" component="div">
                Feature Importance
                </Typography>
                <Typography variant="body2" color="text.secondary">
                Feature Importance refers to techniques that calculate a score
                for all the input features for a given model —
                the scores simply represent the “importance” of each feature.
                A higher score means that the specific feature will have a larger
                effect on the model that is being used to predict a certain variable.
                </Typography>
            </CardContent>
            <CardActions>
                <Button size="small">Share</Button>
                <Button size="small">Learn More</Button>
            </CardActions>
        </Card>
    );
}
