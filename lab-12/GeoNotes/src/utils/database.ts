import * as SQLite from 'expo-sqlite';
import { GeoNote } from '../types';

// Oткрытие базы данных
// Используем any для db и tx, чтобы избежать проблем с типизацией в данной среде, 
// так как полная типизация expo-sqlite требует сложной настройки.
const db: any = SQLite.openDatabaseSync('geonotes.db');

export const database = {
    initDatabase: async (): Promise<void> => {
        return new Promise((resolve, reject) => {
            try {
                db.withTransactionSync(() => {
                    db.runSync(
                        `CREATE TABLE IF NOT EXISTS notes (
                            id TEXT PRIMARY KEY NOT NULL,
                            title TEXT NOT NULL,
                            content TEXT NOT NULL,
                            latitude REAL NOT NULL,
                            longitude REAL NOT NULL,
                            address TEXT,
                            photoUri TEXT,
                            createdAt INTEGER NOT NULL
                        );`
                    );
                    console.log('Database initialized successfully');
                    resolve();
                });
            } catch (error) {
                console.error('Database initialization error:', error);
                reject(error);
            }
        });
    },

    fetchNotes: async (): Promise<GeoNote[]> => {
        return new Promise((resolve, reject) => {
            try {
                const results = db.getAllSync('SELECT * FROM notes ORDER BY createdAt DESC;');
                resolve(results as GeoNote[]);
            } catch (error) {
                console.error('Fetch notes error:', error);
                reject(error);
            }
        });
    },

    addNote: async (note: GeoNote): Promise<void> => {
        return new Promise((resolve, reject) => {
            try {
                db.runSync(
                    'INSERT INTO notes (id, title, content, latitude, longitude, address, photoUri, createdAt) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                    [note.id, note.title, note.content, note.latitude, note.longitude, note.address || null, note.photoUri || null, note.createdAt]
                );
                resolve();
            } catch (error) {
                console.error('Add note error:', error);
                reject(error);
            }
        });
    },

    deleteNote: async (id: string): Promise<void> => {
        return new Promise((resolve, reject) => {
            try {
                db.runSync('DELETE FROM notes WHERE id = ?', [id]);
                resolve();
            } catch (error) {
                console.error('Delete note error:', error);
                reject(error);
            }
        });
    },

    updateNote: async (note: GeoNote): Promise<void> => {
        return new Promise((resolve, reject) => {
            try {
                db.runSync(
                    'UPDATE notes SET title = ?, content = ?, address = ?, photoUri = ? WHERE id = ?',
                    [note.title, note.content, note.address || null, note.photoUri || null, note.id]
                );
                resolve();
            } catch (error) {
                console.error('Update note error:', error);
                reject(error);
            }
        });
    }
};

// Экспортируем функции отдельно для обратной совместимости с ранее написанным кодом
export const initDatabase = database.initDatabase;
export const fetchNotes = database.fetchNotes;
export const addNote = database.addNote;
export const deleteNote = database.deleteNote;
export const updateNote = database.updateNote;
