import { createServer } from "node:http";
import { readFile, mkdir } from "node:fs/promises";
import { extname, join, normalize } from "node:path";
import { chromium } from "playwright";

const root = join(process.cwd(), ".pages");
const types = { ".css": "text/css", ".html": "text/html" };
const server = createServer(async (request, response) => {
  const pathname = request.url === "/" ? "/index.html" : request.url;
  const file = normalize(join(root, pathname));
  if (!file.startsWith(`${root}/`)) {
    response.writeHead(403).end();
    return;
  }
  try {
    const body = await readFile(file);
    response.writeHead(200, { "content-type": types[extname(file)] || "application/octet-stream" });
    response.end(body);
  } catch {
    response.writeHead(404).end();
  }
});

await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
const { port } = server.address();
const browser = await chromium.launch({ headless: true });

try {
  for (const viewport of [
    { name: "desktop", width: 1440, height: 1000 },
    { name: "mobile", width: 390, height: 844 },
  ]) {
    const page = await browser.newPage({ viewport });
    const errors = [];
    page.on("pageerror", (error) => errors.push(error.message));
    page.on("console", (message) => {
      if (message.type() === "error") errors.push(message.text());
    });
    await page.goto(`http://127.0.0.1:${port}`, { waitUntil: "networkidle" });
    await page.locator("h1").waitFor();
    if ((await page.locator("section.learner").count()) !== 3) {
      throw new Error(`${viewport.name}: expected three learner review sections`);
    }
    if (errors.length) throw new Error(`${viewport.name}: ${errors.join("; ")}`);
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
    if (overflow) throw new Error(`${viewport.name}: page has horizontal overflow`);
    if (process.env.CAPTURE === "1" && viewport.name === "desktop") {
      await mkdir(join(process.cwd(), "docs", "images"), { recursive: true });
      await page.screenshot({
        path: join(process.cwd(), "docs", "images", "workflow-demo.png"),
        fullPage: true,
      });
    }
    await page.close();
  }
  console.log("visual smoke passed at desktop and mobile viewports");
} finally {
  await browser.close();
  server.close();
}
