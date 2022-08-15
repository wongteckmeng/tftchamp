import create from 'zustand'
// import { State } from "../model/Match";

// interface MatchState {
//     todos: State[];
//     addTodo: (description: string) => void;
//     removeTodo: (id: string) => void;
//     toggleCompletedState: (id: string) => void;
// }

const uri = "http://localhost:8000/match/?platform=na1&skip=0&limit=5";

const useStore = create((set, get) => ({
    uri: uri,
    count: 0,
    Matches: [],
    fetch: async (uri) => { //: RequestInfo | URL
        const response = await fetch(uri);
        const json = await response.json();
        let results = json.results;
        let new_array = [...get().Matches, ...results];
        let res = new_array.splice(1).reduce((acc, elem) => acc.every(({_id}) => _id !== elem._id) ? [...acc, elem] : acc, [new_array[0]]);
        set({ count: json.count });
        set({ Matches: res});
    },
}));

export default useStore;