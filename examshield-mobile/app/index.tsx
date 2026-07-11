import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function Home() {
  const router = useRouter();

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>ExamShield Mobile</Text>
        <Text style={styles.subtitle}>
          Scan handwritten scripts and review AI evaluations on the go.
        </Text>

        <TouchableOpacity 
          style={styles.primaryButton}
          onPress={() => router.push('/scan')}
        >
          <Text style={styles.primaryButtonText}>Scan New Script</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc', // slate-50
  },
  content: {
    flex: 1,
    padding: 24,
    justifyContent: 'center',
    alignItems: 'center',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#0f172a', // slate-900
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#64748b', // slate-500
    textAlign: 'center',
    marginBottom: 32,
  },
  primaryButton: {
    backgroundColor: '#4F46E5', // indigo-600
    paddingVertical: 14,
    paddingHorizontal: 32,
    borderRadius: 8,
    shadowColor: '#4F46E5',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 8,
    elevation: 4,
  },
  primaryButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  }
});
