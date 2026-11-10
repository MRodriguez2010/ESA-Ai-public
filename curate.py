"""Propose one evidence-backed topic for analyst review before publishing a narrative."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent


def digest(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def select(data, model=None):
    topics = data["topics"]
    if not topics: raise ValueError("No evidence available")
    if not model:
        return max(topics, key=lambda row: abs(row["gap_pp"]))["topic"]
    choices = [{"topic": t["topic"], "gap_pp": t["gap_pp"]} for t in topics]
    payload = {"model": model, "stream": False, "format": "json",
               "prompt": 'Choose one of these topics for review. Return JSON with only the key "topic".\n'+json.dumps(choices)}
    req = Request("http://127.0.0.1:11434/api/generate", data=json.dumps(payload).encode(),
                  headers={"Content-Type":"application/json"})
    with urlopen(req, timeout=90) as response:
        name = json.loads(json.load(response)["response"])["topic"]
    if name not in {r["topic"] for r in topics}: raise ValueError("Model returned an unknown topic")
    return name


def narrative(data, name):
    t = next(r for r in data["topics"] if r["topic"] == name)
    return (f"{name}: {data['focus']} recorded {t['focus_yes']} favorable answers out of {t['focus_total']}. "
            f"The comparison group recorded {t['peer_yes']} out of {t['peer_total']}. "
            f"The gap was {t['gap_pp']:+.1f} percentage points.")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("action", choices=["propose", "approve"])
    p.add_argument("--evidence", type=Path, default=ROOT/"examples/summary.json")
    p.add_argument("--draft", type=Path, default=Path("draft.json"))
    p.add_argument("--model", help="Optional installed local Ollama model, used only to select a topic")
    p.add_argument("--confirm-topic", help="Exact topic the analyst reviewed")
    a=p.parse_args()
    data=json.loads(a.evidence.read_text())
    if a.action=="propose":
        topic=select(data,a.model)
        draft={"state":"pending","evidence_sha256":digest(data),"topic":topic,"text":narrative(data,topic)}
        a.draft.write_text(json.dumps(draft,indent=2)+"\n")
        print(draft["text"])
    else:
        draft=json.loads(a.draft.read_text())
        if draft["topic"]!=a.confirm_topic or draft["evidence_sha256"]!=digest(data) or draft["text"]!=narrative(data,draft["topic"]):
            p.error("Review the current evidence and confirm the exact proposed topic.")
        draft["state"]="approved"
        a.draft.write_text(json.dumps(draft,indent=2)+"\n")
        print(draft["text"])
