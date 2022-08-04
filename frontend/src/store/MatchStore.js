import create from 'zustand'
// import { State } from "../model/Match";

// interface MatchState {
//     todos: State[];
//     addTodo: (description: string) => void;
//     removeTodo: (id: string) => void;
//     toggleCompletedState: (id: string) => void;
// }

const uri = "http://localhost:8000/match/?platform=na1&skip=0&limit=5";

const useStore = create((set) => ({
    uri: uri,
    Matches: [],
    fetch: async (uri) => { //: RequestInfo | URL
        const response = await fetch(uri);
        const json = await response.json();
        set({ Matches: json })
    },
}));

export default useStore;