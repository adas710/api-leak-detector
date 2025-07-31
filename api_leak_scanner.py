import requests
import re

API_PATTERNS = {
    "Twilio SID": r'AC[a-zA-Z0-9]{32}',
    "Twilio Token": r'[a-f0-9]{32}',
    "SendGrid": r'SG\.[a-zA-Z0-9_\-]{22,}\.[a-zA-Z0-9_\-]{22,}',
    "Mailgun": r'key-[a-z0-9]{32}',
    "Firebase": r'AIza[0-9A-Za-z\\-_]{35}',
}

def search_github_code(keyword, page=1):
    url = f"https://api.github.com/search/code?q={keyword}&per_page=10&page={page}"
    headers = {"Accept": "application/vnd.github+json"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get("items", [])
    else:
        print(f"❌ GitHub API Error: {response.status_code}")
        return []

def extract_keys_from_url(raw_url):
    response = requests.get(raw_url)
    found_keys = []
    if response.status_code == 200:
        content = response.text
        for name, pattern in API_PATTERNS.items():
            matches = re.findall(pattern, content)
            for m in matches:
                found_keys.append((name, m))
    return found_keys

def main():
    print("🔍 البحث عن تسريبات API على GitHub...")
    keywords = ["twilio", "sendgrid", "firebase", "mailgun", "apikey", "auth_token"]
    total_found = 0
    for keyword in keywords:
        print(f"\n🔑 يبحث عن: {keyword}")
        results = search_github_code(keyword)
        for item in results:
            raw_url = item['html_url'].replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
            found = extract_keys_from_url(raw_url)
            if found:
                print(f"\n📄 ملف: {raw_url}")
                for name, key in found:
                    print(f"  🔐 {name}: {key}")
                    total_found += 1
    score = 100 if total_found else 0
    print(f"\n✅ Score: {score}/100")
    if total_found:
        print(f"🔎 وجدنا {total_found} مفتاح API.")
    else:
        print("🎉 لا توجد مفاتيح مكشوفة حالياً.")

if __name__ == "__main__":
    main()
