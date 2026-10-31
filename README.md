# How to Scrape US and Canadian Job Postings: 6 Boards, One Schema

> **Run it now, no code: [north-america-jobs-scraper on the Apify Store](https://apify.com/bibian/north-america-jobs-scraper)** &nbsp;|&nbsp; $1.20 per 1,000 postings &nbsp;|&nbsp; no browser, no login

Buying and maintaining a separate scraper per board is slow. This Actor reads 6 major US and Canadian job boards — [Job Bank](https://www.jobbank.gc.ca) (the Government of Canada's official board), [The Muse](https://www.themuse.com), [Built In](https://builtin.com), [Dice](https://www.dice.com), [Wellfound](https://wellfound.com) and [Hacker News "Who is Hiring"](https://news.ycombinator.com) — in a single run, deduplicated and mapped to one unified schema.

Searches this page answers: north america jobs scraper, usa jobs scraper, canada job board api, job bank scraper, us tech jobs dataset.

## What you can do with it

- **Search US and Canadian jobs across tech, startups and government postings in one run**, instead of buying and maintaining 6 separate scrapers.
- **Filter once, everywhere**: `keywords`, `location` and `countries` apply the same way across all 6 sources.
- **Compare pay across boards**: every record shares the same `salaryMin`/`salaryMax` and `employmentType` fields, whichever site it came from.
- **Monitor new postings daily**: schedule it with `onlyNew` checked and `publishedWithinDays: 1` to get, and pay for, only what is new since the last run.

A real sample (five results across five different sources, personal data removed) is in [`sample-output.json`](sample-output.json).

## Output fields

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Stable identifier (`<source>:<native id>`), used to deduplicate between runs. |
| `url` | string | Public page of the posting. |
| `title` | string | Job title as published. |
| `companyName` | string or null | Employer name; `null` when hidden (then `confidentialCompany: true`). |
| `locationLabel`, `city`, `region`, `postalCode` | string or null | Finer location breakdown, when the site publishes one. |
| `country` | string or null | `US` or `CA`. Job Bank is always `CA`; the other sources are matched against the location they publish, defaulting to `US` when nothing points elsewhere. Hacker News listings are free text with no reliable location convention, so an unresolved one stays `null` rather than being guessed. |
| `remote` | string | `remote`, `hybrid`, `onsite` or `unknown`. |
| `employmentType` | string | `full_time`, `part_time`, `contract`, `freelance`, `internship`, `apprenticeship`, `temporary` or `unknown`. |
| `salaryMin` / `salaryMax` / `salaryCurrency` / `salaryPeriod` | — | Salary range as numbers, ISO 4217 currency, and `hour`/`day`/`month`/`year`. |
| `datePosted`, `validThrough` | string or null | Publication and expiry date, ISO 8601. |
| `description` | string or null | Plain-text description, only when `includeDescriptions` is on. No personal data. |
| `skills` | string[] | Skills listed by the site, if any. |
| `source`, `sourceId`, `scrapedAt` | — | Host name of the source site, its native id, and when this Actor read it. |

Site-specific fields are kept in addition to these (never in place of them) — for example Wellfound's `compensation` free text, Dice's `remoteOnly` flag, or Hacker News's `threadId` and `headline`.

## Input

| Field | What it does |
|---|---|
| `keywords` | Job title, skill or trade, for example `backend engineer`. Empty means every posting. |
| `location` | City, province or state, used only by the sources that support it; ignored by the others. |
| `remote` | Keep only postings matching this work mode: `any`, `remote`, `hybrid` or `onsite`. Best effort, based on whatever the source itself publishes. |
| `countries` | Keep only postings in these countries: `US`, `CA`, or both (default). Best effort, based on whatever location the source itself publishes. |
| `sources` | Which of the 6 job boards to query in this run: `jobbank`, `themuse`, `builtin`, `dice`, `wellfound`, `hackernews`. Defaults to all 6. |
| `publishedWithinDays` | Keep only postings published in the last N days. Use `1` for a daily monitoring run. |
| `maxItems` | The run stops once this many postings are saved, across all sources combined (default 50). |
| `includeDescriptions` | Add the job description as plain text (off by default, for a fast run). |
| `onlyNew` | For scheduled runs: skip postings an earlier run of this same search already delivered. |

Example input:

```json
{
  "keywords": "engineer",
  "countries": ["US", "CA"],
  "maxItems": 50,
  "includeDescriptions": false
}
```

## Three ways to use it

### 1. Apify console, no code

1. Open [the Actor page](https://apify.com/bibian/north-america-jobs-scraper) and click **Try for free** (a free Apify account is enough).
2. Fill in the input form (keywords, filters and the maximum number of results) and click **Start**.
3. When the run finishes, open the **Output** tab, check the table, then **Export** as CSV, Excel or JSON.
4. For a daily alert, open **Schedules**, create a daily schedule for the Actor and, optionally, add an integration that sends new results to Slack, e-mail or Google Sheets.

### 2. Apify API with JavaScript

```bash
npm install apify-client
export APIFY_TOKEN="your token from Apify console, Settings, Integrations"
node examples/run.js
```

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('bibian/north-america-jobs-scraper').call({
  keywords: 'engineer',
  maxItems: 50,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
```

The complete file is [`examples/run.js`](examples/run.js) (ES module, Node 18 or later).

### 3. Apify API with Python

```bash
pip install apify-client
export APIFY_TOKEN="your token from Apify console, Settings, Integrations"
python examples/run.py
```

```python
from apify_client import ApifyClient

client = ApifyClient(token="<APIFY_TOKEN>")
run = client.actor("bibian/north-america-jobs-scraper").call(run_input={
    "keywords": "engineer",
    "maxItems": 50
})
items = client.dataset(run["defaultDatasetId"]).list_items().items
```

The complete file is [`examples/run.py`](examples/run.py). Never put your token in the code: read it from the `APIFY_TOKEN` environment variable as above.

## Pricing

Pay per result: **$1.20 per 1,000 postings**, plus $0.01 per run start with the default memory. For example, 100 postings cost about $0.13. You only pay for the postings you receive, and platform usage is included in that price. Store discounts apply automatically on paid Apify plans: up to 20% off every event on the higher tiers.

## Monitor new postings daily and connect your tools

1. **Schedule it.** Save a task, set its publication date filter to the shortest window, and schedule it daily with Apify Schedules. Tick **Only new results** in the input and each run returns, and charges, only the postings that earlier runs of the same search did not deliver.
2. **Push the results where you work.** Add an Apify integration or a webhook to the task: Google Sheets, Slack, Make, Zapier, n8n or your own endpoint, triggered at the end of every run.
3. **Call it from your stack.** The API and the JavaScript and Python clients return the dataset as JSON, CSV or Excel.
4. **Let an AI agent use it.** Through the [Apify MCP server](https://docs.apify.com/platform/integrations/mcp), assistants such as Claude or ChatGPT can search the Store, read this page and run the actor as a tool.

## Why this one

The only Apify actor that puts Canada's official Job Bank in the same schema as US tech boards (The Muse, Built In, Dice, Wellfound) and Hacker News's "Who is hiring?" threads — one run, one schema, deduplicated between sources. `country` on every row to split US from Canada without guessing. No connection, no login, no browser to configure, no recruiter e-mail ever included.

## Limits and honest notes

- `country` is a best-effort filter for the 5 sources that are not single-country by construction: an unclear location is kept rather than dropped, only a clear signal (a Canadian province, city, or a place clearly outside North America) decides.
- `employmentType` is read from each site's own field when it has one; when a source carries none, it is inferred from the title and description, and left `unknown` rather than guessed when nothing matches.
- Hacker News "Who is hiring?" postings are free text with no enforced format: `companyName` and fine-grained location are left `null` rather than force-split from a headline that was never meant to be parsed. The `author` field is the public Hacker News username that posted the thread comment, not a recruiter's real name or contact detail.
- Every result is deduplicated across all 6 sources before it is counted or charged.
- No personal data: contact details of individuals are stripped from descriptions; only companies are named.
- This is an unofficial tool, not affiliated with any of the boards listed above. Check each site's terms and the laws that apply to your use, for example the GDPR.

## FAQ

**Do I need an account, cookies or a proxy?** No. The actor reads publicly visible pages only.

**Which formats can I export?** JSON, CSV, Excel, XML, HTML table or RSS, from the dataset page or through the API.

**Is it legal to scrape?** The actor collects publicly visible postings and respects the robots.txt rules of each site. How you use the data is your responsibility: check the site's terms and the laws that apply to you, for example the GDPR.

**Something does not work?** Open an issue in the Issues tab. Every public actor is test-run daily and the broken ones are repaired.

## More job scrapers by the same author

- [Remote Jobs Worldwide Scraper (8 boards)](https://apify.com/bibian/remote-jobs-worldwide-scraper)
- [Europe Jobs Scraper (12 boards, 7 countries)](https://apify.com/bibian/europe-jobs-scraper)
- [Latin America Jobs Scraper (4 networks, 18 countries)](https://apify.com/bibian/latin-america-jobs-scraper)
- [Dice Jobs Scraper](https://apify.com/bibian/dice-jobs-scraper)
- [Wellfound Jobs Scraper](https://apify.com/bibian/wellfound-jobs-scraper)
- [Built In Jobs Scraper](https://apify.com/bibian/builtin-jobs-scraper)

## Try it

**[Open north-america-jobs-scraper on the Apify Store](https://apify.com/bibian/north-america-jobs-scraper)**

The code in `examples/` is released under the MIT license (see [LICENSE](LICENSE)). The data belongs to its original publishers.
