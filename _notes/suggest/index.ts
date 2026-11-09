// Supabase Edge Function "abbey-suggest": receives a note (and an optional screenshot) from the "Suggest a change" button
// (assets/suggest.js) and opens an issue on GitHub. Deploy with Verify JWT OFF (the button is public).
// Secrets (Edge Function secrets, never in the repo):
//   GITHUB_TOKEN   fine-grained token for munkachy/newmonksite, permission "Issues: Read and write" only
//   GITHUB_REPO    optional, default "munkachy/newmonksite"
// Screenshots go to the public Storage bucket "suggestion-shots" (random file names) and are linked in the issue.
import { createClient } from "npm:@supabase/supabase-js@2";

const REPO = Deno.env.get("GITHUB_REPO") ?? "munkachy/newmonksite";
const ALLOWED = ["https://munkachy.github.io", "https://www.stbernardabbey.com", "https://stbernardabbey.com",
  "https://www.stbernardprep.com", "https://stbernardprep.com", "http://localhost:8123"];
const hits: number[] = [];            // best-effort limit: 40 suggestions an hour for the whole site
const perIp = new Map<string, number[]>();

function cors(origin: string | null) {
  const o = origin && ALLOWED.includes(origin) ? origin : ALLOWED[0];
  return { "Access-Control-Allow-Origin": o, "Access-Control-Allow-Headers": "content-type", "Access-Control-Allow-Methods": "POST, OPTIONS", "Vary": "Origin" };
}
const json = (b: unknown, s: number, h: Record<string, string>) => new Response(JSON.stringify(b), { status: s, headers: { ...h, "Content-Type": "application/json" } });
const clip = (s: unknown, n: number) => String(s ?? "").replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/g, "").slice(0, n);
const esc = (s: string) => s.replace(/([\\`*_{}\[\]<>#|])/g, "\\$1");

Deno.serve(async (req) => {
  const h = cors(req.headers.get("origin"));
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: h });
  if (req.method !== "POST") return json({ ok: false, error: "post only" }, 405, h);
  const origin = req.headers.get("origin");
  if (origin && !ALLOWED.includes(origin)) return json({ ok: false, error: "origin" }, 403, h);

  const now = Date.now();
  while (hits.length && now - hits[0] > 3600_000) hits.shift();
  const ip = (req.headers.get("x-forwarded-for") ?? "").split(",")[0].trim() || "x";
  const mine = (perIp.get(ip) ?? []).filter((t) => now - t < 3600_000);
  if (hits.length >= 40 || mine.length >= 8) return json({ ok: false, error: "slow down" }, 429, h);

  let b: Record<string, unknown>;
  try { b = JSON.parse(await req.text()); } catch { return json({ ok: false, error: "bad json" }, 400, h); }
  if (b.website) return json({ ok: true, issue: 0 }, 200, h);            // honeypot: pretend it worked
  const message = clip(b.message, 4000).trim();
  if (message.length < 3) return json({ ok: false, error: "empty" }, 400, h);
  const name = clip(b.name, 100).trim();
  const page = clip(b.page, 500), title = clip(b.title, 200), viewport = clip(b.viewport, 20), agent = clip(b.agent, 300);

  let shotUrl = "";
  const shot = typeof b.screenshot === "string" ? b.screenshot : "";
  if (shot.startsWith("data:image/jpeg;base64,") && shot.length < 2_000_000) {
    try {
      const sb = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
      const bytes = Uint8Array.from(atob(shot.split(",")[1]), (c) => c.charCodeAt(0));
      const path = `${new Date().toISOString().slice(0, 10)}/${crypto.randomUUID()}.jpg`;
      const up = await sb.storage.from("suggestion-shots").upload(path, bytes, { contentType: "image/jpeg" });
      if (!up.error) shotUrl = sb.storage.from("suggestion-shots").getPublicUrl(path).data.publicUrl;
    } catch (_) { /* the note is still sent without the picture */ }
  }

  const first = message.split("\n")[0].slice(0, 70);
  const body = [
    message, "", "---",
    `**Page:** ${page}`, title ? `**Title:** ${esc(title)}` : "", `**From:** ${name ? esc(name) : "anonymous"}`,
    `**Screen:** ${viewport || "?"}, scrolled ${Number(b.scroll) || 0}px`, `**Browser:** ${esc(agent)}`, "",
    shotUrl ? `![Screenshot of where they were](${shotUrl})` : "_No screenshot._",
  ].filter((x) => x !== "").join("\n");

  const gh = await fetch(`https://api.github.com/repos/${REPO}/issues`, {
    method: "POST",
    headers: { Authorization: `Bearer ${Deno.env.get("GITHUB_TOKEN")}`, Accept: "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "abbey-suggest" },
    body: JSON.stringify({ title: `Suggestion: ${first}`, body, labels: ["suggestion"] }),
  });
  if (!gh.ok) { console.error("github", gh.status, await gh.text()); return json({ ok: false, error: "github" }, 502, h); }
  const issue = await gh.json();
  hits.push(now); mine.push(now); perIp.set(ip, mine);
  return json({ ok: true, issue: issue.number }, 200, h);
});
