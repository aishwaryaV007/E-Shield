import { listSubmissions } from "@/lib/store";
import StudentReport from "@/components/StudentReport";

export default function StudentPage() {
  const submissions = listSubmissions();
  return (
    <main className="max-w-2xl mx-auto py-10 px-6">
      <h1 className="font-serif text-2xl text-stone-800 mb-6">
        Your results
      </h1>
      <StudentReport
        submissions={submissions}
        initialStudentId={submissions[1]?.id ?? submissions[0]?.id}
      />
    </main>
  );
}
