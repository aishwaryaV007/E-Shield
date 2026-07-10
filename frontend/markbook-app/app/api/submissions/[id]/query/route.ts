import { NextResponse } from "next/server";
import { createQuery, replyToQuery } from "@/lib/store";

// Student raises a query. Body: { questionId: string, text: string }
export async function POST(
  req: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const { questionId, text } = await req.json();
  const submission = createQuery(id, questionId, text);
  if (!submission) {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }
  return NextResponse.json(submission);
}

// Teacher replies. Body: { reply: string }
export async function PATCH(
  req: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const { reply } = await req.json();
  const submission = replyToQuery(id, reply);
  if (!submission) {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }
  return NextResponse.json(submission);
}
