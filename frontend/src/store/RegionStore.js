import create from 'zustand';

const useStore = create(set => ({
    region: 'na1',
    setRegion: (newRegion) =>
        set({
            region: newRegion
        })
}));

export const useRegionStore = useStore;