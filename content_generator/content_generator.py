# ============================================
# Script  : content_generator.py
# Purpose : Generate TikTok & YouTube scripts
#           for each portfolio project
# Author  : Anel Graph
# ============================================

import os
import sys
import datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from groq import Groq

api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    print("ERROR: Set GROQ_API_KEY first")
    sys.exit(1)

client = Groq(api_key=api_key)

# -----------------------------------------------
# Your portfolio projects
# -----------------------------------------------
PROJECTS = [
    {
        "title": "Python Security Toolkit",
        "description": (
            "A unified menu-driven toolkit with 7 tools: "
            "log writer, threat detector, real-time monitor, "
            "port scanner, password checker, and SOC dashboard. "
            "Built entirely in Python from scratch."
        ),
        "skills": "Python, regex, sockets, file I/O, Git, GitHub",
        "wow_factor": (
            "I built a mini SIEM from scratch in Python that "
            "detects brute force attacks and port scans in real time"
        ),
        "github": "https://github.com/Aceknight4/security-toolkit"
    },
    {
        "title": "AI-Powered Intrusion Detection System",
        "description": (
            "Real-time log analyser using Groq API and Llama 3.3. "
            "Detects behavioural threats that rule-based systems miss "
            "including data exfiltration hidden in INFO-level logs."
        ),
        "skills": "Python, Groq API, Llama 3.3, prompt engineering",
        "wow_factor": (
            "The AI caught a data exfiltration attack that said INFO "
            "in the log — a rule-based system would have completely "
            "ignored it"
        ),
        "github": "https://github.com/Aceknight4/security-toolkit"
    }
]

# -----------------------------------------------
# Generate content for one platform
# -----------------------------------------------
def generate_script(project, platform):
    """
    Sends project details to AI and gets back
    a ready-to-record content script.
    """

    if platform == "tiktok":
        instructions = """
        Write a TikTok script for a cybersecurity developer
        showing their project. Rules:
        - Maximum 60 seconds when spoken aloud
        - Hook in the first 3 seconds — make it shocking or curious
        - Show the demo moment clearly
        - End with a call to action (follow, link in bio)
        - Casual, energetic tone — not corporate
        - Use short punchy sentences
        - Include suggested on-screen text overlays in [brackets]
        Format:
        HOOK: (first 3 seconds)
        DEMO: (show the tool working)
        PAYOFF: (the impressive result)
        CTA: (call to action)
        HASHTAGS: (10 relevant hashtags)
        """
    else:  # youtube
        instructions = """
        Write a YouTube short script (60 seconds) for a
        cybersecurity developer showing their project. Rules:
        - Hook in first 5 seconds
        - Explain what problem this solves
        - Show the impressive demo moment
        - Explain what skills this demonstrates
        - End with subscribe CTA and GitHub link mention
        - Professional but approachable tone
        Format:
        TITLE: (YouTube title, SEO optimised)
        HOOK: (first 5 seconds)
        PROBLEM: (what problem does this solve)
        DEMO: (the impressive moment)
        SKILLS: (what this proves to employers)
        CTA: (subscribe + GitHub)
        TAGS: (10 SEO tags)
        """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a social media strategist specialising in "
                    "tech and cybersecurity content. You help developers "
                    "build personal brands and attract remote job offers "
                    "through short-form video content. "
                    "The creator is Anel Graph, a self-taught security "
                    "automation engineer based in Cameroon building "
                    "toward remote work. They are authentic, technical, "
                    "and ambitious. Write scripts that sound like a real "
                    "person, not a corporate presenter."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Project: {project['title']}\n"
                    f"Description: {project['description']}\n"
                    f"Skills shown: {project['skills']}\n"
                    f"The wow moment: {project['wow_factor']}\n"
                    f"GitHub: {project['github']}\n\n"
                    f"Platform: {platform.upper()}\n\n"
                    f"{instructions}"
                )
            }
        ],
        temperature=0.7,   # Higher temperature = more creative writing
        max_tokens=800
    )

    return response.choices[0].message.content

# -----------------------------------------------
# Save script to file
# -----------------------------------------------
def save_script(project_title, platform, content):
    """Saves generated script to a text file."""
    safe_title = project_title.lower().replace(" ", "_")
    filename = f"{safe_title}_{platform}_script.txt"

    with open(filename, "w") as f:
        f.write(f"PROJECT: {project_title}\n")
        f.write(f"PLATFORM: {platform.upper()}\n")
        f.write(f"GENERATED: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write("=" * 60 + "\n\n")
        f.write(content)
        f.write("\n\n" + "=" * 60)

    print(f"  Saved → {filename}")
    return filename

# -----------------------------------------------
# Main — generate all scripts
# -----------------------------------------------
print("\n" + "=" * 60)
print("  CONTENT GENERATOR — Portfolio to Social Media")
print("  by Anel Graph")
print("=" * 60)
print(f"\n  Projects loaded  : {len(PROJECTS)}")
print(f"  Platforms        : TikTok, YouTube")
print(f"  Scripts to create: {len(PROJECTS) * 2}\n")

generated_files = []

for project in PROJECTS:
    print(f"\n  Processing: {project['title']}")
    print("  " + "-" * 40)

    for platform in ["tiktok", "youtube"]:
        print(f"  Generating {platform.upper()} script...", end=" ", flush=True)

        try:
            script = generate_script(project, platform)
            filename = save_script(project["title"], platform, script)
            generated_files.append(filename)
            print("Done ✅")

        except Exception as e:
            print(f"Error: {e}")

# --- Final summary ---
print("\n" + "=" * 60)
print("  ALL SCRIPTS GENERATED")
print("=" * 60)
print(f"\n  Files created:")
for f in generated_files:
    print(f"    → {f}")

print(f"\n  Next steps:")
print(f"  1. Read each script and personalise it")
print(f"  2. Record your screen showing the tool running")
print(f"  3. Record your voiceover using the script")
print(f"  4. Post TikTok first — fastest feedback loop")
print(f"  5. Repurpose same video for YouTube Shorts")
print(f"  6. Pin GitHub link in every bio\n")
