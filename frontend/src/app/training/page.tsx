export default function TrainingPage() {
  return (
    <main style={{ maxWidth: 960, margin: "0 auto", padding: 40 }}>
      <h2>Training</h2>
      <p style={{ color: "#94a3b8" }}>
        Model B is trained offline (see <code>dataset/processed/model_b_metrics.json</code>). Grade a
        script on the <a href="/" style={{ color: "#3b82f6" }}>home page</a>.
      </p>
    </main>
  );
}
