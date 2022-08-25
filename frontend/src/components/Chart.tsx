import React from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer, LabelList, Tooltip } from 'recharts';
import Skeleton from '@mui/material/Skeleton';

import Title from './Title';

import { useFeatureImportanceStore } from '../store/FeatureImportanceStore';
import { useMetadataStore } from '../store/MetadataStore';


export default function Chart() {

  const payload = useFeatureImportanceStore(state => state.payload);
  const setPayload = useFeatureImportanceStore(state => state.setPayload);
  const region = useMetadataStore(state => state.region);
  const league = useMetadataStore(state => state.league);
  const latest_version = useMetadataStore(state => state.latest_version);
  const latest_patch = useMetadataStore(state => state.latest_patch);
  const setVersion = useMetadataStore(state => state.setVersion);
  const setPatch = useMetadataStore(state => state.setPatch);

  const [isLoading, setIsLoading] = React.useState(true);

  React.useEffect(() => {
    let canceled: boolean = false;
    setIsLoading(true);

    const metadataBase = `http://localhost:8000/metadata`;
    const query = `?platform=${region}&league=${league}&version=${latest_version}&patch=${latest_patch}`;
    const uri = `http://localhost:8000/feature_importance/${query}`

    async function getFeatureImportance(uri: string) {
      if (!canceled) {
        const metadata_response = await fetch(metadataBase);
        const metadata = await (metadata_response.json());
        setVersion(metadata.latest_version)
        setPatch(metadata.latest_patch)

        const response = await fetch(uri);
        const data = await (response.json());
        setPayload(data.results);
        setIsLoading(false);
      }
    }
    getFeatureImportance(uri);
    return (): any => canceled = true;
  }, [region, league, latest_version, latest_patch, setVersion, setPatch, setPayload]);

  return (
    <React.Fragment>
      <Title>Feature Importances({region} {league})</Title>
      <ResponsiveContainer>
        {!isLoading ? (
          <BarChart
            barSize={10}
            data={payload as any}
            margin={{ top: 16, right: 16, bottom: 32, left: 280 }}
            layout="vertical"
          >
            <XAxis type="number" />
            <YAxis dataKey="label" type="category" />
            <Tooltip />
            <CartesianGrid stroke="#f5f5f5" />
            <Bar dataKey="feature_importance" fill="#387908">
              <LabelList position="right" />
            </Bar>
          </BarChart>
        ) : (<Skeleton variant="rectangular" width="100%" height={100} />)}
      </ResponsiveContainer>
    </React.Fragment>
  );
}
