import create from 'zustand';

type State = {
    region: string;
    league: string;
    latest_version: string;
    latest_patch: string;
    
    setRegion: (region: string) => void;
    setLeague: (league: string) => void;
    setVersion: (latest_version: string) => void;
    setPatch: (latest_patch: string) => void;
};

const useStore = create<State>(set => ({
    region: 'na1',
    league: 'challengers',
    latest_version: '12.15.458.1416',
    latest_patch: '2022-08-10',

    setRegion: (region) => set({ region }),
    setLeague: (league) => set({ league }),
    setVersion: (latest_version) => set({ latest_version }),
    setPatch: (latest_patch) => set({ latest_patch }),
}));

export const useMetadataStore = useStore;