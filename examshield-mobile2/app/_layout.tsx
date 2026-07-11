import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';

export default function Layout() {
  return (
    <>
      <Stack
        screenOptions={{
          headerStyle: {
            backgroundColor: '#ffffff',
          },
          headerTintColor: '#4F46E5', // Indigo-600
          headerTitleStyle: {
            fontWeight: 'bold',
          },
        }}
      >
        <Stack.Screen name="index" options={{ title: 'ExamShield' }} />
        <Stack.Screen name="scan" options={{ title: 'Scan Script' }} />
      </Stack>
      <StatusBar style="auto" />
    </>
  );
}
