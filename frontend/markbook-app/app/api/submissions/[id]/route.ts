import { NextResponse } from "next/server";
import { getSubmission, updateQuestion } from "@/lib/store";

export async function GET(
  _req: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const submission = getSubmission(id);
  if (!submission) {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }
  return NextResponse.json(submission);
}

// Body: { questionId: string, mark?: number, comment?: string }
export async function PATCH(
  req: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const body = await req.json();
  const { questionId, mark, comment } = body;
  const patch: { mark?: number; comment?: string } = {};
  if (typeof mark === "number") patch.mark = mark;
  if (typeof comment === "string") patch.comment = comment;

  const submission = updateQuestion(id, questionId, patch);
  if (!submission) {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }
  return NextResponse.json(submission);
}
