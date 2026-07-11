import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function ResultsScreen() {
  const router = useRouter();
  const { id } = useLocalSearchParams();

  // Mock data for UI layout
  const mockResult = {
    student_id: '12345',
    total_marks: 8.5,
    percentage: 85.0,
    grade: 'A',
    questions: [
      { id: 'Q1', awarded_marks: 4.5, feedback: 'Good conceptual understanding, missed one point.' },
      { id: 'Q2', awarded_marks: 4.0, feedback: 'Excellent explanation.' }
    ]
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.headerCard}>
           <Text style={styles.headerTitle}>Evaluation Complete</Text>
           <Text style={styles.scoreText}>{mockResult.percentage}%</Text>
           <View style={styles.badge}>
             <Text style={styles.badgeText}>Grade {mockResult.grade}</Text>
           </View>
           <Text style={styles.detailText}>Total Marks: {mockResult.total_marks}</Text>
        </View>

        <Text style={styles.sectionTitle}>Question Breakdown</Text>
        
        {mockResult.questions.map((q, idx) => (
          <View key={idx} style={styles.questionCard}>
            <View style={styles.qHeader}>
               <Text style={styles.qTitle}>Question {q.id}</Text>
               <Text style={styles.qMarks}>{q.awarded_marks} Marks</Text>
            </View>
            <Text style={styles.feedbackLabel}>AI Feedback:</Text>
            <Text style={styles.feedbackText}>{q.feedback}</Text>
            
            <TouchableOpacity style={styles.editButton}>
              <Text style={styles.editButtonText}>Edit / Override</Text>
            </TouchableOpacity>
          </View>
        ))}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f1f5f9', // slate-100
  },
  scrollContent: {
    padding: 16,
  },
  headerCard: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 24,
    alignItems: 'center',
    marginBottom: 24,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  headerTitle: {
    fontSize: 18,
    color: '#64748b',
    marginBottom: 8,
  },
  scoreText: {
    fontSize: 48,
    fontWeight: 'bold',
    color: '#4F46E5', // indigo-600
    marginBottom: 8,
  },
  badge: {
    backgroundColor: '#dcfce7', // green-100
    paddingVertical: 4,
    paddingHorizontal: 12,
    borderRadius: 16,
    marginBottom: 12,
  },
  badgeText: {
    color: '#166534', // green-800
    fontWeight: 'bold',
  },
  detailText: {
    fontSize: 16,
    color: '#334155',
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#0f172a',
    marginBottom: 16,
  },
  questionCard: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    borderLeftWidth: 4,
    borderLeftColor: '#4F46E5',
  },
  qHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  qTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1e293b',
  },
  qMarks: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#4F46E5',
  },
  feedbackLabel: {
    fontSize: 14,
    color: '#64748b',
    marginBottom: 4,
  },
  feedbackText: {
    fontSize: 15,
    color: '#334155',
    lineHeight: 22,
    marginBottom: 16,
  },
  editButton: {
    alignSelf: 'flex-start',
    backgroundColor: '#f1f5f9',
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 6,
  },
  editButtonText: {
    color: '#475569',
    fontWeight: '500',
  }
});
