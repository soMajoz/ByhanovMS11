import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { GeoNote } from '../types';
import * as database from '../utils/database';

interface NotesState {
    items: GeoNote[];
    loading: boolean;
    error: string | null;
}

const initialState: NotesState = {
    items: [],
    loading: false,
    error: null
};

export const loadNotes = createAsyncThunk(
    'notes/loadNotes',
    async () => {
        const notes = await database.fetchNotes();
        return notes;
    }
);

export const saveNote = createAsyncThunk(
    'notes/saveNote',
    async (note: GeoNote) => {
        await database.addNote(note);
        return note;
    }
);

export const removeNote = createAsyncThunk(
    'notes/removeNote',
    async (id: string) => {
        await database.deleteNote(id);
        return id;
    }
);

const notesSlice = createSlice({
    name: 'notes',
    initialState,
    reducers: {},
    extraReducers: (builder) => {
        builder
            .addCase(loadNotes.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(loadNotes.fulfilled, (state, action: PayloadAction<GeoNote[]>) => {
                state.loading = false;
                state.items = action.payload;
            })
            .addCase(loadNotes.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message || 'Failed to load notes';
            })
            .addCase(saveNote.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(saveNote.fulfilled, (state, action: PayloadAction<GeoNote>) => {
                state.loading = false;
                state.items.push(action.payload);
                state.items.sort((a, b) => b.createdAt - a.createdAt);
            })
            .addCase(saveNote.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message || 'Failed to save note';
            })
            .addCase(removeNote.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(removeNote.fulfilled, (state, action: PayloadAction<string>) => {
                state.loading = false;
                state.items = state.items.filter(note => note.id !== action.payload);
            })
            .addCase(removeNote.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message || 'Failed to delete note';
            });
    }
});

export default notesSlice.reducer;
