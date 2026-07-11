import { View, Text, StyleSheet, Button, TouchableOpacity } from 'react-native';
import { CameraView, useCameraPermissions } from 'expo-camera';
import { useState } from 'react';
import * as DocumentPicker from 'expo-document-picker';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function ScanScreen() {
  const [facing, setFacing] = useState<'back' | 'front'>('back');
  const [permission, requestPermission] = useCameraPermissions();
  const [scannedFile, setScannedFile] = useState<any>(null);

  if (!permission) {
    return <View />;
  }

  if (!permission.granted) {
    return (
      <View style={styles.container}>
        <Text style={styles.message}>We need your permission to show the camera</Text>
        <Button onPress={requestPermission} title="grant permission" />
      </View>
    );
  }

  const pickDocument = async () => {
    let result = await DocumentPicker.getDocumentAsync({
      type: 'application/pdf',
    });
    if (!result.canceled) {
      setScannedFile(result.assets[0]);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <CameraView style={styles.camera} facing={facing} />
      <View style={[styles.buttonContainer, { position: 'absolute', bottom: 0, left: 0, right: 0 }]}>
        <TouchableOpacity style={styles.actionButton} onPress={pickDocument}>
          <Text style={styles.text}>Upload PDF</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.actionButton}>
          <Text style={styles.text}>Snap Photo</Text>
        </TouchableOpacity>
      </View>
      {scannedFile && (
        <View style={styles.previewContainer}>
          <Text style={styles.previewText}>Selected: {scannedFile.name}</Text>
          <TouchableOpacity style={styles.submitButton}>
             <Text style={styles.submitText}>Submit for Grading</Text>
          </TouchableOpacity>
        </View>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
  },
  message: {
    textAlign: 'center',
    paddingBottom: 10,
  },
  camera: {
    flex: 1,
  },
  buttonContainer: {
    flex: 1,
    flexDirection: 'row',
    backgroundColor: 'transparent',
    margin: 64,
    justifyContent: 'space-between',
    alignItems: 'flex-end',
  },
  actionButton: {
    backgroundColor: 'rgba(0,0,0,0.5)',
    padding: 12,
    borderRadius: 8,
  },
  text: {
    fontSize: 16,
    fontWeight: 'bold',
    color: 'white',
  },
  previewContainer: {
    padding: 20,
    backgroundColor: 'white',
    alignItems: 'center',
  },
  previewText: {
    fontSize: 16,
    marginBottom: 10,
    color: '#333'
  },
  submitButton: {
    backgroundColor: '#4F46E5',
    padding: 12,
    borderRadius: 8,
    width: '100%',
    alignItems: 'center',
  },
  submitText: {
    color: 'white',
    fontWeight: 'bold',
  }
});
