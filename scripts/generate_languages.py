import os, sys, requests, math
import matplotlib.pyplot as plt

TOKEN = os.environ.get("GH_TOKEN")
if not TOKEN:
    print("Missing GH_TOKEN env var", file=sys.stderr)
    sys.exit(1)

API = "https://api.github.com/graphql"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

ignored = {"HTML", "CSS", "Jupyter Notebook"}

lang_sizes = {}

# Paginate repositories
after = None
while True:
    q = {
        "query": """
        query($after: String) {
          viewer {
            repositories(first: 100, after: $after, affiliations: [OWNER, ORGANIZATION_MEMBER, COLLABORATOR], isFork: false, orderBy: {field: UPDATED_AT, direction: DESC}) {
              pageInfo { hasNextPage endCursor }
              nodes {
                languages(first: 100, orderBy: {field: SIZE, direction: DESC}) {
                  edges { size node { name } }
                }
              }
            }
          }
        }
        """,
        "variables": {"after": after}
    }
    r = requests.post(API, json=q, headers=HEADERS, timeout=60)
    r.raise_for_status()
    data = r.json()
    repos = data["data"]["viewer"]["repositories"]
    for repo in repos["nodes"]:
        for e in repo["languages"]["edges"]:
            name = e["node"]["name"]
            if name in ignored:
                continue
            lang_sizes[name] = lang_sizes.get(name, 0) + int(e["size"])
    if not repos["pageInfo"]["hasNextPage"]:
        break
    after = repos["pageInfo"]["endCursor"]

if not lang_sizes:
    # Create a tiny placeholder to avoid failing the workflow
    with open("languages.svg", "w") as f:
        f.write("<svg xmlns='http://www.w3.org/2000/svg' width='600' height='60'><text x='10' y='35' font-family='sans-serif' font-size='16'>No language data yet</text></svg>")
    sys.exit(0)

# Sort and aggregate small slices to 'Other'
items = sorted(lang_sizes.items(), key=lambda x: x[1], reverse=True)
 total = sum(v for _, v in items)
percent = [(k, v/total*100.0) for k, v in items]
major = [(k, p) for k, p in percent if p >= 3.0]
other = sum(p for _, p in percent if p < 3.0)
if other > 0:
    major.append(("Other", other))
labels = [k for k, _ in major]
sizes = [p for _, p in major]

# Donut chart
fig = plt.figure(figsize=(8, 5), dpi=160)
ax = fig.add_subplot(111)
wedges, texts = ax.pie(sizes, startangle=180, wedgeprops=dict(width=0.45))
ax.axis('equal')

# Only label slices >=6%
label_texts = [f"{l} {p:.1f}%" if p >= 6 else "" for l, p in zip(labels, sizes)]
kw = dict(ha='center', va='center', fontsize=9)
# Annotate around the donut
angle = 180
for w, t, lbl, p in zip(wedges, texts, labels, sizes):
    ang = (w.theta2 + w.theta1) / 2.0
    x = 1.05 * math.cos(math.radians(ang))
    y = 1.05 * math.sin(math.radians(ang))
    if p >= 6:
        ax.text(x, y, f"{lbl}
{p:.1f}%", **kw)

plt.title("Languages (public + private)", fontsize=12)
plt.tight_layout()
fig.savefig("languages.svg", format="svg", bbox_inches='tight')
