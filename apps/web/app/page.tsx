const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export default async function Home() {
  let capabilities: Record<string, unknown> = { status: "API unavailable" };
  try {
    const response = await fetch(`${apiBase}/api/v1/capabilities`, { cache: "no-store" });
    if (response.ok) capabilities = await response.json();
  } catch {
    // The page remains useful as a boot diagnostic when the API is down.
  }

  return (
    <main>
      <p className="eyebrow">Walking skeleton</p>
      <h1>Architected AI Starter</h1>
      <p>
        Replace this page with the first real vertical slice. The capability block below is
        intentionally wired to the API so a fresh clone proves browser → API connectivity.
      </p>
      <pre>{JSON.stringify(capabilities, null, 2)}</pre>
    </main>
  );
}
