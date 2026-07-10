import { listSubmissions } from "@/lib/store";
import TeacherDashboard from "@/components/TeacherDashboard";

// Server component: fetch directly from the store (swap for a Supabase
// query once that's wired up). Client component below handles all
// interactivity and re-fetches/updates via the API routes.
export default function TeacherPage() {
  const submissions = listSubmissions();
  return (
    <main className="max-w-4xl mx-auto py-10 px-6">
      <h1 className="font-serif text-2xl text-stone-800 mb-6">
        Grading queue
      </h1>
      <TeacherDashboard initialSubmissions={submissions} />
    </main>
  );
}
