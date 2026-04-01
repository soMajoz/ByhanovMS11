import React, { useEffect } from 'react';
import {
    View,
    Text,
    FlatList,
    StyleSheet,
    TouchableOpacity,
    ActivityIndicator
} from 'react-native';
import { useAppDispatch, useAppSelector } from '../hooks/reduxHooks';
import { loadNotes } from '../store/notesSlice';
import { GeoNote } from '../types';

interface NotesListScreenProps {
    navigation: any;
}

const NotesListScreen: React.FC<NotesListScreenProps> = ({ navigation }) => {
    const dispatch = useAppDispatch();
    const { items: notes, loading, error } = useAppSelector(state => state.notes);

    useEffect(() => {
        dispatch(loadNotes());
    }, [dispatch]);

    const renderNoteItem = ({ item }: { item: GeoNote }) => (
        <TouchableOpacity
            style={styles.card}
            onPress={() => navigation.navigate('NoteDetail', { noteId: item.id })}
        >
            <View style={styles.cardHeader}>
                <Text style={styles.title} numberOfLines={1}>{item.title}</Text>
                <Text style={styles.date}>
                    {new Date(item.createdAt).toLocaleDateString()}
                </Text>
            </View>
            
            <Text style={styles.content} numberOfLines={2}>
                {item.content}
            </Text>
            
            {item.address && (
                <Text style={styles.address} numberOfLines={1}>
                    📍 {item.address}
                </Text>
            )}

            {item.photoUri && (
                <View style={styles.photoBadge}>
                    <Text style={styles.photoBadgeText}>📷</Text>
                </View>
            )}
        </TouchableOpacity>
    );

    if (loading && notes.length === 0) {
        return (
            <View style={styles.centered}>
                <ActivityIndicator size="large" color="#007AFF" />
            </View>
        );
    }

    if (error) {
        return (
            <View style={styles.centered}>
                <Text style={styles.errorText}>{error}</Text>
                <TouchableOpacity
                    style={styles.retryButton}
                    onPress={() => dispatch(loadNotes())}
                >
                    <Text style={styles.retryButtonText}>Повторить</Text>
                </TouchableOpacity>
            </View>
        );
    }

    return (
        <View style={styles.container}>
            <FlatList
                data={notes}
                keyExtractor={item => item.id}
                renderItem={renderNoteItem}
                contentContainerStyle={styles.listContainer}
                ListEmptyComponent={
                    <View style={styles.emptyContainer}>
                        <Text style={styles.emptyText}>У вас пока нет заметок</Text>
                        <Text style={styles.emptySubtext}>Нажмите + чтобы создать новую</Text>
                    </View>
                }
            />
            
            <TouchableOpacity
                style={styles.fab}
                onPress={() => navigation.navigate('AddNote')}
            >
                <Text style={styles.fabIcon}>+</Text>
            </TouchableOpacity>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#f5f5f5'
    },
    centered: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center'
    },
    listContainer: {
        padding: 16
    },
    card: {
        backgroundColor: 'white',
        borderRadius: 8,
        padding: 16,
        marginBottom: 12,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
        elevation: 2,
        position: 'relative'
    },
    cardHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 8
    },
    title: {
        fontSize: 18,
        fontWeight: 'bold',
        color: '#333',
        flex: 1,
        marginRight: 8
    },
    date: {
        fontSize: 12,
        color: '#999'
    },
    content: {
        fontSize: 14,
        color: '#666',
        marginBottom: 8
    },
    address: {
        fontSize: 12,
        color: '#007AFF'
    },
    fab: {
        position: 'absolute',
        bottom: 24,
        right: 24,
        width: 56,
        height: 56,
        borderRadius: 28,
        backgroundColor: '#007AFF',
        justifyContent: 'center',
        alignItems: 'center',
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 4,
        elevation: 6
    },
    fabIcon: {
        fontSize: 32,
        color: 'white',
        lineHeight: 34
    },
    emptyContainer: {
        alignItems: 'center',
        marginTop: 64
    },
    emptyText: {
        fontSize: 18,
        fontWeight: 'bold',
        color: '#333',
        marginBottom: 8
    },
    emptySubtext: {
        fontSize: 14,
        color: '#666'
    },
    errorText: {
        color: 'red',
        marginBottom: 16,
        fontSize: 16
    },
    retryButton: {
        paddingHorizontal: 16,
        paddingVertical: 8,
        backgroundColor: '#007AFF',
        borderRadius: 8
    },
    retryButtonText: {
        color: 'white',
        fontWeight: 'bold'
    },
    photoBadge: {
        position: 'absolute',
        top: 16,
        right: 16,
        backgroundColor: '#007AFF',
        borderRadius: 12,
        paddingHorizontal: 8,
        paddingVertical: 4
    },
    photoBadgeText: {
        color: 'white',
        fontSize: 12
    }
});

export default NotesListScreen;
