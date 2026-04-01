import React, { useState, useEffect } from 'react';
import {
    View,
    Text,
    TextInput,
    StyleSheet,
    TouchableOpacity,
    ScrollView,
    Alert,
    Image,
    ActivityIndicator
} from 'react-native';
import * as Location from 'expo-location';
import * as ImagePicker from 'expo-image-picker';
import { useAppDispatch } from '../hooks/reduxHooks';
import { saveNote } from '../store/notesSlice';
import { GeoNote } from '../types';

interface AddNoteScreenProps {
    navigation: any;
}

const AddNoteScreen: React.FC<AddNoteScreenProps> = ({ navigation }) => {
    const dispatch = useAppDispatch();
    
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const [location, setLocation] = useState<Location.LocationObject | null>(null);
    const [address, setAddress] = useState<string>('');
    const [photoUri, setPhotoUri] = useState<string | undefined>();
    const [isLocating, setIsLocating] = useState(false);
    const [isSaving, setIsSaving] = useState(false);

    useEffect(() => {
        getLocation();
    }, []);

    const getLocation = async () => {
        setIsLocating(true);
        try {
            let { status } = await Location.requestForegroundPermissionsAsync();
            if (status !== 'granted') {
                Alert.alert('Ошибка', 'Нет доступа к геолокации');
                return;
            }

            let currentLocation = await Location.getCurrentPositionAsync({});
            setLocation(currentLocation);

            // Обратное геокодирование (получение адреса по координатам)
            let geocode = await Location.reverseGeocodeAsync({
                latitude: currentLocation.coords.latitude,
                longitude: currentLocation.coords.longitude
            });

            if (geocode && geocode.length > 0) {
                const place = geocode[0];
                setAddress(`${place.city || place.subregion || ''}, ${place.street || ''} ${place.streetNumber || ''}`.replace(/^[,\s]+|[,\s]+$/g, ''));
            }
        } catch (error) {
            Alert.alert('Ошибка', 'Не удалось определить местоположение');
            console.error(error);
        } finally {
            setIsLocating(false);
        }
    };

    const takePhoto = async () => {
        const { status } = await ImagePicker.requestCameraPermissionsAsync();
        if (status !== 'granted') {
            Alert.alert('Ошибка', 'Нужно разрешение на использование камеры');
            return;
        }

        const result = await ImagePicker.launchCameraAsync({
            mediaTypes: ImagePicker.MediaTypeOptions.Images,
            allowsEditing: true,
            aspect: [4, 3],
            quality: 0.7,
        });

        if (!result.canceled) {
            setPhotoUri(result.assets[0].uri);
        }
    };

    const handleSave = async () => {
        if (!title.trim() || !content.trim() || !location) {
            Alert.alert('Ошибка', 'Пожалуйста, заполните все поля и дождитесь определения геопозиции');
            return;
        }

        setIsSaving(true);
        try {
            const newNote: GeoNote = {
                id: Date.now().toString(),
                title: title.trim(),
                content: content.trim(),
                latitude: location.coords.latitude,
                longitude: location.coords.longitude,
                address: address || undefined,
                photoUri: photoUri,
                createdAt: Date.now()
            };

            await dispatch(saveNote(newNote)).unwrap();
            navigation.goBack();
        } catch (error) {
            Alert.alert('Ошибка', 'Не удалось сохранить заметку');
            console.error(error);
        } finally {
            setIsSaving(false);
        }
    };

    return (
        <ScrollView style={styles.container}>
            <View style={styles.form}>
                <Text style={styles.label}>Заголовок</Text>
                <TextInput
                    style={styles.input}
                    value={title}
                    onChangeText={setTitle}
                    placeholder="Введите заголовок"
                />

                <Text style={styles.label}>Текст заметки</Text>
                <TextInput
                    style={[styles.input, styles.textArea]}
                    value={content}
                    onChangeText={setContent}
                    placeholder="О чем эта заметка?"
                    multiline
                    numberOfLines={6}
                    textAlignVertical="top"
                />

                <View style={styles.locationContainer}>
                    <Text style={styles.label}>Местоположение</Text>
                    {isLocating ? (
                        <Text style={styles.locationText}>Определение местоположения...</Text>
                    ) : location ? (
                        <View>
                            <Text style={styles.locationText}>
                                {address || `Lat: ${location.coords.latitude.toFixed(4)}, Lng: ${location.coords.longitude.toFixed(4)}`}
                            </Text>
                            <TouchableOpacity onPress={getLocation}>
                                <Text style={styles.updateLocationText}>Обновить</Text>
                            </TouchableOpacity>
                        </View>
                    ) : (
                        <TouchableOpacity onPress={getLocation} style={styles.locationButton}>
                            <Text style={styles.locationButtonText}>Определить местоположение</Text>
                        </TouchableOpacity>
                    )}
                </View>

                <View style={styles.photoSection}>
                    <Text style={styles.label}>Фотография</Text>
                    <TouchableOpacity style={styles.photoButton} onPress={takePhoto}>
                        <Text style={styles.photoButtonText}>
                            {photoUri ? 'Изменить фото' : 'Сделать фото'}
                        </Text>
                    </TouchableOpacity>

                    {photoUri && (
                        <View style={styles.previewContainer}>
                            <Image source={{ uri: photoUri }} style={styles.preview} />
                            <TouchableOpacity
                                style={styles.removePhotoButton}
                                onPress={() => setPhotoUri(undefined)}
                            >
                                <Text style={styles.removePhotoText}>✕</Text>
                            </TouchableOpacity>
                        </View>
                    )}
                </View>

                <TouchableOpacity
                    style={[
                        styles.saveButton,
                        (!title.trim() || !content.trim() || !location || isSaving) && styles.saveButtonDisabled
                    ]}
                    onPress={handleSave}
                    disabled={!title.trim() || !content.trim() || !location || isSaving}
                >
                    {isSaving ? (
                        <ActivityIndicator color="white" />
                    ) : (
                        <Text style={styles.saveButtonText}>Сохранить заметку</Text>
                    )}
                </TouchableOpacity>
            </View>
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff'
    },
    form: {
        padding: 20
    },
    label: {
        fontSize: 16,
        fontWeight: 'bold',
        color: '#333',
        marginBottom: 8,
        marginTop: 16
    },
    input: {
        borderWidth: 1,
        borderColor: '#ddd',
        borderRadius: 8,
        padding: 12,
        fontSize: 16,
        backgroundColor: '#fafafa'
    },
    textArea: {
        height: 120
    },
    locationContainer: {
        marginTop: 16,
        padding: 16,
        backgroundColor: '#f0f8ff',
        borderRadius: 8,
        borderWidth: 1,
        borderColor: '#cce5ff'
    },
    locationText: {
        fontSize: 14,
        color: '#333',
        marginBottom: 8
    },
    updateLocationText: {
        fontSize: 14,
        color: '#007AFF',
        fontWeight: 'bold'
    },
    locationButton: {
        backgroundColor: '#007AFF',
        padding: 10,
        borderRadius: 6,
        alignItems: 'center'
    },
    locationButtonText: {
        color: 'white',
        fontWeight: 'bold'
    },
    photoSection: {
        marginTop: 8
    },
    photoButton: {
        backgroundColor: '#f0f0f0',
        padding: 12,
        borderRadius: 8,
        alignItems: 'center',
        borderWidth: 1,
        borderColor: '#ddd'
    },
    photoButtonText: {
        color: '#333',
        fontWeight: 'bold'
    },
    previewContainer: {
        marginTop: 12,
        position: 'relative'
    },
    preview: {
        width: '100%',
        height: 200,
        borderRadius: 8
    },
    removePhotoButton: {
        position: 'absolute',
        top: 8,
        right: 8,
        backgroundColor: 'rgba(0,0,0,0.5)',
        width: 30,
        height: 30,
        borderRadius: 15,
        justifyContent: 'center',
        alignItems: 'center'
    },
    removePhotoText: {
        color: 'white',
        fontSize: 16,
        fontWeight: 'bold'
    },
    saveButton: {
        backgroundColor: '#34c759',
        padding: 16,
        borderRadius: 8,
        alignItems: 'center',
        marginTop: 32,
        marginBottom: 40
    },
    saveButtonDisabled: {
        backgroundColor: '#a2e4b1'
    },
    saveButtonText: {
        color: 'white',
        fontSize: 18,
        fontWeight: 'bold'
    }
});

export default AddNoteScreen;
