import React from "react";
import { useTheme } from '@mui/material/styles';
import { LineChart, Line, XAxis, YAxis, Label, ResponsiveContainer } from 'recharts';
import Title from './Title';

import { useFeatureImportanceStore } from '../store/FeatureImportanceStore';

// Generate Sales Data
function createData(time: string, amount?: number) {
  return { time, amount };
}

const data = [
  createData('00:00', 0),
  createData('03:00', 300),
  createData('06:00', 600),
  createData('09:00', 800),
  createData('12:00', 1500),
  createData('15:00', 2000),
  createData('18:00', 2400),
  createData('21:00', 2400),
  createData('24:00', undefined),
];

export default function Chart() {
  const theme = useTheme();

  const payload = useFeatureImportanceStore(state => state.payload);
  const setPayload = useFeatureImportanceStore(state => state.setPayload);

  const [isLoading, setIsLoading] = React.useState(true);

  React.useEffect(() => {
    let canceled:boolean = false;
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
    // return () => canceled = true;
  }, [setPayload]);

  return (
    <React.Fragment>
      <Title>Feature Importance</Title>
      <ResponsiveContainer>
        <LineChart
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
          <Line
            isAnimationActive={false}
            type="monotone"
            dataKey="feature_importance"
            stroke={theme.palette.primary.main}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </React.Fragment>
  );
}
