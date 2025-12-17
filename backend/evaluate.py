import pandas as pd
import requests
import time

API_URL = "http://127.0.0.1:8000/recommend"
TEST_FILE = "test_set.csv"          # must contain column: Query
OUT_FILE = "surabhi_bhor.csv"       # FINAL submission file


def safe_read_csv(path):
    """Handle encoding issues safely"""
    try:
        return pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin1")


def main():
    df = safe_read_csv(TEST_FILE)

    if "Query" not in df.columns:
        raise ValueError("❌ test_set.csv must contain a column named 'Query'")

    rows = []

    print(f"📄 Total queries: {len(df)}")

    for idx, row in df.iterrows():
        query = str(row["Query"]).strip()

        if not query:
            rows.append({"Query": "", "Assessment_url": ""})
            continue

        try:
            resp = requests.post(
                API_URL,
                json={"query": query, "max_results": 10},
                timeout=30
            )

            if resp.status_code != 200:
                print(f"❌ API error on row {idx+1}")
                rows.append({"Query": query, "Assessment_url": ""})
                continue

            data = resp.json()

            # 🔑 backend returns "recommendations"
            recs = data.get("recommendations", [])

            urls = [
                r.get("url") or r.get("assessment_url")
                for r in recs
                if r.get("url") or r.get("assessment_url")
            ]

            # ONE ROW PER QUERY (SHL EXPECTATION)
            rows.append({
                "Query": query,
                "Assessment_url": "|".join(urls[:10])
            })

            print(f"✅ {idx+1}/{len(df)} processed")

            time.sleep(0.3)  # be polite to API

        except Exception as e:
            print(f"⚠️ Error on row {idx+1}: {e}")
            rows.append({"Query": query, "Assessment_url": ""})

    out_df = pd.DataFrame(rows)
    out_df.to_csv(OUT_FILE, index=False, encoding="utf-8")

    print("\n🎯 DONE")
    print(f"✅ Saved: {OUT_FILE}")
    print(f"📊 Rows: {len(out_df)} (should match test queries)")


if __name__ == "__main__":
    main()
