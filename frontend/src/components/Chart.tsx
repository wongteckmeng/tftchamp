import React from "react";
import { useTheme } from '@mui/material/styles';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, Label, CartesianGrid, ResponsiveContainer, LabelList, Tooltip } from 'recharts';
import Title from './Title';

import { useFeatureImportanceStore } from '../store/FeatureImportanceStore';

// Generate Sales Data
function createData(time: string, amount?: number) {
  return { time, amount };
}


export default function Chart() {
  const theme = useTheme();

  const payload = useFeatureImportanceStore(state => state.payload);
  const setPayload = useFeatureImportanceStore(state => state.setPayload);

  const [isLoading, setIsLoading] = React.useState(true);

  React.useEffect(() => {
    let canceled: boolean = false;
    setIsLoading(true);

    const uri = `http://localhost:8000/feature_importance`

    async function getFeatureImportance(uri: string) {
      if (!canceled) {
        const response = await fetch(uri);
        const data = await (response.json());
        setPayload(data.results);
        setIsLoading(false);
      }
    }
    getFeatureImportance(uri);
    return (): any => canceled = true;
  }, [setPayload]);

  return (
    <React.Fragment>
      <Title>Feature Importance</Title>
      <ResponsiveContainer>
        <BarChart
          barSize={10}
          data={payload as any}
          margin={{ top: 16, right: 16, bottom: 16, left: 280 }}
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
        {/* <LineChart
          data={payload as any}
          margin={{
            top: 16,
            right: 16,
            bottom: 16,
            left: 16,
          }}
        >
          <XAxis
            dataKey="label"
            stroke={theme.palette.text.secondary}
            style={theme.typography.body2}>
            <Label position="bottom" style={{
              textAnchor: 'middle',
              fill: theme.palette.text.primary,
              ...theme.typography.body1,
            }}>Features</Label>
          </XAxis>
          <YAxis
            stroke={theme.palette.text.secondary}
            style={theme.typography.body2}
          >
            <Label
              angle={270}
              position="left"
              style={{
                textAnchor: 'middle',
                fill: theme.palette.text.primary,
                ...theme.typography.body1,
              }}
            >
              Correlation(abs)
            </Label>
          </YAxis>
          <CartesianGrid stroke="#f5f5f5" />
          <Line
            isAnimationActive={false}
            type="monotone"
            dataKey="feature_importance"
            stroke={theme.palette.primary.main}
            dot={false}
          />
        </LineChart> */}
      </ResponsiveContainer>
    </React.Fragment>
  );
}
