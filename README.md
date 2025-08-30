<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:4158D0,100:C850C0&height=160&section=header&text=Abdul%20Aziz&fontSize=48&fontColor=ffffff&animation=twinkling&fontAlignY=35&desc=Senior%20Full%20Stack%20Engineer%20%7C%20AI%20Innovator%20%7C%20Team%20Lead&descAlignY=55&descSize=18" />
</div>

<div align="center">

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code\&size=22\&duration=3000\&pause=1000\&color=4158D0\&center=true\&vCenter=true\&width=700\&lines=Building+Scalable+Full+Stack+Apps;AI+%26+LangChain+Integration+Specialist;ICPC+Top+10%20%7C%20LeetCode%20Top%205%25;Passionate%20Leader%20%26%20Mentor;Innovation%20Through%20Code)](https://git.io/typing-svg)

</div>

<h2 align="center">Senior Full‑Stack Engineer · AI Innovator · Team Lead @ <strong>Developer Tag</strong></h2>

<p align="center">
  <a href="https://connect2abdulaziz-psi.vercel.app">Portfolio</a> ·
  <a href="https://linkedin.com/in/connect2abdulaziz">LinkedIn</a> ·
  <a href="https://leetcode.com/connect2abdulaziz">LeetCode</a> ·
  <a href="mailto:connect2abdulaziz@gmail.com">Email</a>
</p>

---

### At a glance

* **3+ years** shipping scalable products (SaaS, dashboards, microservices)
* **ICPC Asia 2023 — Top 10** · **LeetCode Top 5%**
* Lead teams building **MERN/Next.js** platforms on **AWS** with solid DevOps
* Production **AI/RAG** with LangChain/LangGraph

---

### What I do

* Architect & deliver **full‑stack systems** (Next.js/React · Node.js/Express · PostgreSQL/MongoDB)
* Design **event‑driven microservices** with Docker, queues, and observability
* Build **AI assistants** (retrieval‑augmented generation, tools/agents) for real use‑cases
* Lead teams: code reviews, roadmaps, hiring, mentoring

---

### Tech

<p align="center">
  <img src="https://skillicons.dev/icons?i=react,nextjs,typescript,javascript,nodejs,express,python,langchain,mongodb,postgresql,aws,docker,git,graphql" />
</p>

---

### Selected work

> Private client repositories are intentionally not linked. Public case‑study write‑ups will live on the portfolio. For repo access, please reach out privately.

<div align="center">

| Project                        | What it does                                           | Stack                                         | Access                           |
| ------------------------------ | ------------------------------------------------------ | --------------------------------------------- | -------------------------------- |
| **LangGraph RAG Starter**      | Production‑grade RAG with evaluations & feedback loops | Python, LangChain/LangGraph, OpenAI, PgVector | 🔒 Internal (request case study) |
| **Next.js SaaS Boilerplate**   | Auth, billing, dashboards, CRUD, testing               | Next.js 14, tRPC, Prisma, PostgreSQL, Stripe  | 🔒 Internal (request case study) |
| **Event‑Driven Microservices** | Services with Kafka/NATS, SAGA/Outbox patterns         | Node.js, Docker, PostgreSQL, Kafka            | 🔒 Internal (request case study) |
| **AI Support Bot**             | Multilingual support agent with tools & memory         | Python, FastAPI, LangChain, Redis             | 🔒 Internal (request case study) |

</div>

---

### Impact & activity

<p align="center">
  <img src="./metrics.svg" alt="GitHub Metrics" />
</p>

<p align="center">
  <img width="49%" src="https://github-readme-stats-weld-iota-73.vercel.app/api?username=connect2abdulaziz&show_icons=true&count_private=true&theme=tokyonight&hide_border=true&bg_color=0D1117&title_color=4158D0&icon_color=4158D0&text_color=FFFFFF&border_radius=10" />
  <img width="49%" src="https://github-readme-streak-stats.herokuapp.com/?user=connect2abdulaziz&theme=tokyonight&hide_border=true&background=0D1117&stroke=4158D0&ring=4158D0&fire=C850C0&currStreakLabel=C850C0&border_radius=10" />
</p>

<p align="center">
  <img width="49%" src="https://github-readme-stats-weld-iota-73.vercel.app/api/top-langs/?username=connect2abdulaziz&layout=compact&count_private=true&theme=tokyonight&hide_border=true&bg_color=0D1117&title_color=4158D0&text_color=FFFFFF&border_radius=10&hide=jupyter%20notebook,css,html" />
</p>

<p align="center">
  <img src="https://github-readme-activity-graph.vercel.app/graph?username=connect2abdulaziz&bg_color=0D1117&color=4158D0&line=4158D0&point=C850C0&area=true&hide_border=true&theme=tokyo-night" />
</p>

> **Private contributions:** Enable **Profile → Settings → Contributions → Include private contributions on my profile**. For the stats cards above, you’re already using a self‑hosted deployment with `count_private=true`. Ensure that deployment has a PAT with scopes `repo` and `read:user` so private activity is included.

---

### Leadership & practices

* Write architecture decisions (ADRs) and run blameless post‑mortems
* Prefer automated quality gates: CI, coverage, lint, type‑safety
* Design for operability: logs, traces, dashboards, SLOs
* Communicate with RFCs and small, frequent releases

---

### Achievements

* **ICPC Asia Online Preliminary 2023 – Top 10**
* **LeetCode Top 5%** problem solver
* Delivered **50+ projects** for global clients
* Awarded **Student of the Year** (Akhuwat College)

---

### Get in touch

I build reliable software and mentor engineers. If you have a challenging platform problem or want to talk AI + product, reach out.

---

<details>
<summary><strong>Profile settings & automation (click to expand)</strong></summary>

#### 1) Show private org contributions (optional)

* Settings → **Profile → Contributions** → check **Include private contributions on my profile**

#### 2) Keep your metrics SVG fresh (GitHub Actions)

Create `.github/workflows/metrics.yml` in your **username/username** profile repo:

```yaml
name: Metrics
on:
  schedule:
    - cron: "22 3 * * *"   # daily at 03:22 UTC
  workflow_dispatch:

jobs:
  github-metrics:
    runs-on: ubuntu-latest
    steps:
      - name: Generate metrics
        uses: lowlighter/metrics@latest
        with:
          token: ${{ secrets.METRICS_TOKEN }}
          user: connect2abdulaziz
          template: classic
          base: header, activity, community, repositories
          config_timezone: Asia/Karachi
          plugin_followup: yes
          plugin_isocalendar: yes
          plugin_isocalendar_duration: half-year
          plugin_languages: yes
          plugin_languages_ignored: html, css, jupyter notebook
          plugin_achievements: yes
          plugin_achievements_threshold: C
          plugin_lines: yes
          plugin_repositories: yes
          plugin_topics: yes
          plugin_topics_limit: 12
      - name: Save SVG to repo
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git init
          git remote add origin https://github.com/${GITHUB_REPOSITORY}.git
          git fetch --depth=1 origin
          git checkout -B main || git checkout -B master || true
          echo "Generated on $(date -u)" > .metrics_timestamp
          mv metrics.svg metrics.svg || true
          git add metrics.svg .metrics_timestamp
          git commit -m "chore(metrics): update metrics.svg"
          git push origin HEAD
```

> **Setup:** Create a classic PAT named `METRICS_TOKEN` with `public_repo` (and `repo` if you want private stats) and add it to **Settings → Secrets and variables → Actions**.

#### 3) Professional repo hygiene (copy into your projects)

* **License:** MIT or Apache‑2.0
* **Topics & description:** add 5–10 relevant topics for SEO
* **CI:** minimal CI with install, test, lint
* **Docs:** short README with architecture diagram + screenshots

`CONTRIBUTING.md`

```md
# Contributing

Thanks for your interest! Use conventional commits (feat, fix, chore, docs), write tests for changes, and run lint before pushing.

## Development
- Install: pnpm|npm install
- Test: pnpm|npm test
- Lint: pnpm|npm run lint

## Pull Requests
- Small, focused PRs
- Include screenshots for UI changes
- Link related issues
```

`.github/PULL_REQUEST_TEMPLATE.md`

```md
## What

## Why

## How to test

- [ ] Tests added/updated
- [ ] Docs updated (if needed)
```

`.github/ISSUE_TEMPLATE/bug_report.yml`

```yaml
name: Bug report
description: File a bug
labels: [bug]
body:
  - type: textarea
    id: what-happened
    attributes:
      label: What happened?
      description: What did you expect to happen?
    validations:
      required: true
```

`.github/ISSUE_TEMPLATE/feature_request.yml`

```yaml
name: Feature request
description: Suggest an idea
labels: [enhancement]
body:
  - type: textarea
    id: problem
    attributes:
      label: Problem
  - type: textarea
    id: proposal
    attributes:
      label: Proposal
```

#### 4) Pins that signal impact

Pin 6 repos that show: (1) **business impact**, (2) **AI expertise**, (3) **architecture depth**, (4) **tests/CI quality**, (5) **clean docs**, (6) **community value** (templates/starters).

#### 5) Include private repo contributions in status cards (self‑hosted)

* Using your own `github-readme-stats` deployment. In hosting (e.g., Vercel), set an env var `GH_TOKEN` or `PAT_1` with a Classic PAT that has `repo` + `read:user` scopes.
* Keep `count_private=true` in the image URLs (already set above).
* Private contributions must also be enabled in your profile settings to appear in streak/activity graphs.

</details>

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:4158D0,100:C850C0&height=120&section=footer&animation=twinkling" />

<strong>"Passion + Precision = Innovation"</strong>

</div>
