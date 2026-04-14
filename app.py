import streamlit as st
import json
import requests
import base64
from io import StringIO

st.set_page_config(page_title="Portfolio Generator", page_icon="🎨")

TEMPLATES = {
    "minimal": "Minimal (tmavý)",
    "gradient": "Gradient (glassmorphism)",
    "cards": "Cards (světlý)",
    "terminal": "Terminal (retro)",
}

COLORS = {
    "#58a6ff": "Blue",
    "#3fb950": "Green",
    "#f0883e": "Orange",
    "#f85149": "Red",
    "#a371f7": "Purple",
    "#f778ba": "Pink",
    "#79c0ff": "Light Blue",
    "#56d364": "Lime",
}


def get_social_icon(platform):
    icons = {
        "github": "🐙",
        "linkedin": "💼",
        "twitter": "🐦",
        "website": "🌐",
        "email": "✉️",
    }
    return icons.get(platform, "🔗")


def generate_html(data):
    name = data.get("name", "Vaše jméno")
    title = data.get("title", "Profese")
    bio = data.get("bio", "")
    location = data.get("location", "")
    email = data.get("email", "")
    social = data.get("social", [])
    projects = data.get("projects", [])
    template = data.get("template", "minimal")
    color = data.get("color", "#58a6ff")

    social_html = ""
    for s in social:
        url = s.get("url", "")
        platform = s.get("platform", "website")
        icon = get_social_icon(platform)

        if platform == "github":
            url = f"https://github.com/{url}"
        elif platform == "linkedin":
            url = f"https://linkedin.com/in/{url}"
        elif platform == "twitter":
            url = f"https://twitter.com/{url}"
        elif platform == "email":
            url = f"mailto:{url}"

        if url:
            social_html += f'<a href="{url}" target="_blank" rel="noopener">{icon}</a>'

    projects_html = ""
    for p in projects:
        p_name = p.get("name", "")
        p_desc = p.get("description", "")
        p_url = p.get("url", "")
        p_tech = p.get("tech", "")

        tech_tags = ""
        if p_tech:
            for t in p_tech.split(","):
                tech_tags += f"<span>{t.strip()}</span>"

        link_tag = (
            f'<a href="{p_url}" target="_blank" rel="noopener" class="project-link"></a>'
            if p_url
            else ""
        )

        projects_html += f"""
        <div class="project-card">
            {link_tag}
            <h3>{p_name}</h3>
            <p>{p_desc}</p>
            {f'<div class="tech-tags">{tech_tags}</div>' if tech_tags else ""}
        </div>
        """

    templates = {
        "minimal": f"""<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #0a0a0a; color: #fff; min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 40px 20px; }}
        .container {{ max-width: 640px; width: 100%; }}
        .name {{ font-size: 2.5rem; font-weight: 700; margin-bottom: 8px; }}
        .title {{ font-size: 1.25rem; color: {color}; margin-bottom: 16px; }}
        .bio {{ color: #888; line-height: 1.7; margin-bottom: 24px; }}
        .location, .email {{ color: #666; font-size: 14px; margin-bottom: 4px; }}
        .social {{ display: flex; gap: 16px; margin: 24px 0; font-size: 24px; }}
        .social a {{ color: #666; transition: color 0.2s; }}
        .social a:hover {{ color: {color}; }}
        .section-title {{ font-size: 12px; text-transform: uppercase; letter-spacing: 1px; color: #444; margin: 40px 0 20px; }}
        .project-card {{ position: relative; padding: 20px; background: #111; border-radius: 8px; margin-bottom: 12px; transition: background 0.2s; }}
        .project-card:hover {{ background: #1a1a1a; }}
        .project-link {{ position: absolute; inset: 0; }}
        .project-card h3 {{ font-size: 1.1rem; margin-bottom: 6px; }}
        .project-card p {{ color: #888; font-size: 14px; }}
        .tech-tags {{ display: flex; gap: 8px; flex-wrap: wrap; margin-top: 12px; }}
        .tech-tags span {{ font-size: 11px; padding: 4px 8px; background: #222; border-radius: 4px; color: #666; }}
        footer {{ margin-top: 60px; color: #444; font-size: 12px; text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <h1 class="name">{name}</h1>
        <div class="title">{title}</div>
        {f'<p class="bio">{bio}</p>' if bio else ""}
        {f'<div class="location">📍 {location}</div>' if location else ""}
        {f'<div class="email">✉️ {email}</div>' if email else ""}
        {f'<div class="social">{social_html}</div>' if social_html else ""}
        {f'<div class="section-title">Projekty</div>{projects_html}' if projects_html else ""}
        <footer>Generated with Portfolio Generator</footer>
    </div>
</body>
</html>""",
        "gradient": f"""<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; color: #fff; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 80px 20px; }}
        .avatar {{ width: 120px; height: 120px; border-radius: 50%; background: rgba(255,255,255,0.2); margin-bottom: 24px; display: flex; align-items: center; justify-content: center; font-size: 48px; backdrop-filter: blur(10px); }}
        .name {{ font-size: 3rem; font-weight: 700; margin-bottom: 8px; }}
        .title {{ font-size: 1.5rem; opacity: 0.9; margin-bottom: 20px; }}
        .bio {{ font-size: 1.1rem; line-height: 1.7; opacity: 0.85; margin-bottom: 32px; }}
        .info {{ display: flex; gap: 24px; margin-bottom: 32px; font-size: 14px; opacity: 0.8; }}
        .social {{ display: flex; gap: 12px; margin-bottom: 60px; font-size: 24px; }}
        .social a {{ width: 44px; height: 44px; border-radius: 50%; background: rgba(255,255,255,0.15); display: flex; align-items: center; justify-content: center; transition: all 0.2s; backdrop-filter: blur(10px); }}
        .social a:hover {{ background: rgba(255,255,255,0.3); transform: translateY(-2px); }}
        .section-title {{ font-size: 14px; text-transform: uppercase; letter-spacing: 2px; opacity: 0.7; margin-bottom: 24px; padding-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.2); }}
        .projects-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }}
        .project-card {{ position: relative; padding: 24px; background: rgba(255,255,255,0.1); border-radius: 16px; backdrop-filter: blur(10px); transition: all 0.3s; }}
        .project-card:hover {{ background: rgba(255,255,255,0.15); transform: translateY(-4px); }}
        .project-link {{ position: absolute; inset: 0; border-radius: 16px; }}
        .project-card h3 {{ font-size: 1.2rem; margin-bottom: 8px; }}
        .project-card p {{ font-size: 14px; opacity: 0.8; margin-bottom: 12px; }}
        .tech-tags {{ display: flex; gap: 8px; flex-wrap: wrap; }}
        .tech-tags span {{ font-size: 12px; padding: 4px 12px; background: rgba(255,255,255,0.2); border-radius: 20px; }}
        footer {{ margin-top: 80px; text-align: center; opacity: 0.5; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="avatar">👤</div>
        <h1 class="name">{name}</h1>
        <div class="title">{title}</div>
        {f'<p class="bio">{bio}</p>' if bio else ""}
        <div class="info">
            {f"<span>📍 {location}</span>" if location else ""}
            {f"<span>✉️ {email}</span>" if email else ""}
        </div>
        {f'<div class="social">{social_html}</div>' if social_html else ""}
        {f'<div class="section-title">Projekty</div><div class="projects-grid">{projects_html}</div>' if projects_html else ""}
        <footer>Generated with Portfolio Generator</footer>
    </div>
</body>
</html>""",
        "cards": f"""<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #f8f9fa; color: #1a1a1a; min-height: 100vh; padding: 60px 20px; }}
        .container {{ max-width: 900px; margin: 0 auto; }}
        .profile-card {{ background: #fff; border-radius: 16px; padding: 40px; margin-bottom: 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); text-align: center; }}
        .avatar {{ width: 100px; height: 100px; border-radius: 50%; background: {color}; margin: 0 auto 20px; display: flex; align-items: center; justify-content: center; font-size: 40px; color: #fff; }}
        .name {{ font-size: 1.75rem; font-weight: 700; margin-bottom: 4px; }}
        .title {{ font-size: 1rem; color: {color}; margin-bottom: 16px; }}
        .bio {{ color: #666; line-height: 1.7; max-width: 500px; margin: 0 auto 20px; }}
        .info {{ display: flex; justify-content: center; gap: 20px; font-size: 14px; color: #888; margin-bottom: 20px; }}
        .social {{ display: flex; justify-content: center; gap: 12px; font-size: 20px; }}
        .social a {{ width: 40px; height: 40px; border-radius: 50%; background: #f0f0f0; display: flex; align-items: center; justify-content: center; transition: all 0.2s; }}
        .social a:hover {{ background: {color}; }}
        .section-title {{ font-size: 1.5rem; font-weight: 700; margin-bottom: 24px; color: #1a1a1a; }}
        .projects-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }}
        .project-card {{ position: relative; background: #fff; border-radius: 12px; padding: 24px; box-shadow: 0 2px 12px rgba(0,0,0,0.05); transition: all 0.2s; }}
        .project-card:hover {{ transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,0.1); }}
        .project-link {{ position: absolute; inset: 0; border-radius: 12px; }}
        .project-icon {{ width: 48px; height: 48px; border-radius: 12px; background: {color}20; margin-bottom: 16px; display: flex; align-items: center; justify-content: center; font-size: 20px; }}
        .project-card h3 {{ font-size: 1.1rem; font-weight: 600; margin-bottom: 8px; }}
        .project-card p {{ font-size: 14px; color: #666; margin-bottom: 12px; }}
        .tech-tags {{ display: flex; gap: 6px; flex-wrap: wrap; }}
        .tech-tags span {{ font-size: 11px; padding: 4px 10px; background: #f0f0f0; border-radius: 4px; color: #666; }}
        footer {{ margin-top: 60px; text-align: center; color: #999; font-size: 13px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="profile-card">
            <div class="avatar">👤</div>
            <h1 class="name">{name}</h1>
            <div class="title">{title}</div>
            {f'<p class="bio">{bio}</p>' if bio else ""}
            <div class="info">
                {f"<span>📍 {location}</span>" if location else ""}
                {f"<span>✉️ {email}</span>" if email else ""}
            </div>
            {f'<div class="social">{social_html}</div>' if social_html else ""}
        </div>
        {f'<h2 class="section-title">Projekty</h2><div class="projects-grid">{projects_html}</div>' if projects_html else ""}
        <footer>Generated with Portfolio Generator</footer>
    </div>
</body>
</html>""",
        "terminal": f"""<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name}</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'JetBrains Mono', monospace; background: #0d1117; color: #c9d1d9; min-height: 100vh; padding: 40px 20px; }}
        .container {{ max-width: 700px; margin: 0 auto; }}
        .prompt {{ color: {color}; margin-bottom: 4px; }}
        .prompt::before {{ content: '$ '; }}
        .name {{ font-size: 2rem; font-weight: 600; color: #fff; margin-bottom: 8px; }}
        .title {{ color: {color}; margin-bottom: 20px; }}
        .bio {{ line-height: 1.8; margin-bottom: 24px; border-left: 2px solid {color}; padding-left: 16px; }}
        .info {{ margin-bottom: 24px; }}
        .info div {{ margin-bottom: 4px; opacity: 0.7; }}
        .social {{ display: flex; gap: 16px; margin-bottom: 40px; font-size: 24px; }}
        .social a {{ color: {color}; opacity: 0.7; transition: opacity 0.2s; }}
        .social a:hover {{ opacity: 1; }}
        .section {{ margin-bottom: 40px; }}
        .section-header {{ display: flex; align-items: center; gap: 8px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 1px solid #21262d; }}
        .section-header span {{ color: {color}; }}
        .project-card {{ position: relative; padding: 16px; background: #161b22; border-radius: 6px; margin-bottom: 12px; transition: background 0.2s; }}
        .project-card:hover {{ background: #1c2128; }}
        .project-link {{ position: absolute; inset: 0; border-radius: 6px; }}
        .project-name {{ color: #58a6ff; margin-bottom: 4px; }}
        .project-name::before {{ content: '> '; color: {color}; }}
        .project-card p {{ font-size: 13px; opacity: 0.7; margin-bottom: 8px; }}
        .tech-tags {{ display: flex; gap: 8px; }}
        .tech-tags span {{ font-size: 11px; padding: 2px 8px; background: #21262d; border-radius: 4px; color: {color}; }}
        footer {{ margin-top: 60px; color: #484f58; font-size: 12px; }}
        footer span {{ color: {color}; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="prompt"></div>
        <div class="name">{name}</div>
        <div class="title">~ {title}</div>
        {f'<div class="bio">{bio}</div>' if bio else ""}
        <div class="info">
            {f"<div>📍 {location}</div>" if location else ""}
            {f"<div>✉️ {email}</div>" if email else ""}
        </div>
        {f'<div class="social">{social_html}</div>' if social_html else ""}
        {f'<div class="section"><div class="section-header"><span>##</span> projects</div>{projects_html}</div>' if projects_html else ""}
        <footer>// <span>Generated with Portfolio Generator</span></footer>
    </div>
</body>
</html>""",
    }

    return templates.get(template, templates["minimal"])


def download_html(html_content, filename="portfolio.html"):
    b64 = base64.b64encode(html_content.encode()).decode()
    href = (
        f'<a href="data:text/html;base64,{b64}" download="{filename}">Stáhnout HTML</a>'
    )
    return href


if "data" not in st.session_state:
    st.session_state.data = {
        "name": "",
        "title": "",
        "bio": "",
        "location": "",
        "email": "",
        "social": [],
        "projects": [],
        "template": "minimal",
        "color": "#58a6ff",
    }

st.title("🎨 Portfolio Generator")

tab1, tab2, tab3 = st.tabs(["📝 Profil", "🚀 Projekty", "🎭 Design"])

with tab1:
    st.subheader("Základní info")
    st.session_state.data["name"] = st.text_input(
        "Jméno", st.session_state.data["name"]
    )
    st.session_state.data["title"] = st.text_input(
        "Titulek / Profese", st.session_state.data["title"]
    )
    st.session_state.data["bio"] = st.text_area("Bio", st.session_state.data["bio"])
    st.session_state.data["location"] = st.text_input(
        "Lokace", st.session_state.data["location"]
    )
    st.session_state.data["email"] = st.text_input(
        "E-mail", st.session_state.data["email"]
    )

    st.subheader("Sociální sítě")
    col1, col2 = st.columns([1, 2])
    with col1:
        platform = st.selectbox(
            "Platforma",
            ["github", "linkedin", "twitter", "website", "email"],
            key="social_platform",
        )
    with col2:
        url = st.text_input("Username / URL", key="social_url")

    if st.button("➕ Přidat síť"):
        if url:
            st.session_state.data["social"].append({"platform": platform, "url": url})
            st.rerun()

    if st.session_state.data["social"]:
        st.write("Přidané sítě:")
        for i, s in enumerate(st.session_state.data["social"]):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.text(f"{get_social_icon(s['platform'])} {s['platform']}: {s['url']}")
            with col2:
                if st.button("❌", key=f"del_social_{i}"):
                    st.session_state.data["social"].pop(i)
                    st.rerun()

with tab2:
    st.subheader("GitHub Import")
    github_user = st.text_input("GitHub username")
    if st.button("📥 Importovat z GitHub"):
        if github_user:
            try:
                response = requests.get(
                    f"https://api.github.com/users/{github_user}/repos?sort=updated&per_page=20"
                )
                if response.status_code == 200:
                    repos = response.json()
                    st.session_state.data["projects"] = []
                    for repo in repos:
                        if not repo.get("fork", False):
                            st.session_state.data["projects"].append(
                                {
                                    "name": repo.get("name", ""),
                                    "description": repo.get("description", "") or "",
                                    "url": repo.get("html_url", ""),
                                    "tech": "",
                                }
                            )
                    st.success(
                        f"Importováno {len(st.session_state.data['projects'])} repozitářů!"
                    )
                    st.rerun()
                else:
                    st.error("Uživatel nenalezen")
            except Exception as e:
                st.error(f"Chyba: {e}")

    st.subheader("Manuální přidání")
    col1, col2 = st.columns(2)
    with col1:
        p_name = st.text_input("Název projektu", key="p_name")
        p_desc = st.text_input("Popis", key="p_desc")
    with col2:
        p_url = st.text_input("URL", key="p_url")
        p_tech = st.text_input("Technologie", key="p_tech")

    if st.button("➕ Přidat projekt"):
        if p_name:
            st.session_state.data["projects"].append(
                {"name": p_name, "description": p_desc, "url": p_url, "tech": p_tech}
            )
            st.rerun()

    if st.session_state.data["projects"]:
        st.write("---")
        st.write("Vaše projekty:")
        for i, p in enumerate(st.session_state.data["projects"]):
            with st.expander(f"📁 {p['name']}"):
                p["name"] = st.text_input("Název", p["name"], key=f"pn_{i}")
                p["description"] = st.text_input(
                    "Popis", p["description"], key=f"pd_{i}"
                )
                p["url"] = st.text_input("URL", p["url"], key=f"pu_{i}")
                p["tech"] = st.text_input("Technologie", p["tech"], key=f"pt_{i}")
                if st.button("🗑️ Smazat", key=f"del_proj_{i}"):
                    st.session_state.data["projects"].pop(i)
                    st.rerun()

with tab3:
    st.subheader("Šablona")
    template = st.selectbox(
        "Vyberte šablonu",
        list(TEMPLATES.keys()),
        format_func=lambda x: TEMPLATES[x],
        index=list(TEMPLATES.keys()).index(st.session_state.data["template"]),
    )
    st.session_state.data["template"] = template

    st.subheader("Accent barva")
    cols = st.columns(len(COLORS))
    for i, (color, name) in enumerate(COLORS.items()):
        with cols[i]:
            if st.button(
                "🟨",
                key=f"color_{color}",
                help=name,
                type="primary"
                if st.session_state.data["color"] == color
                else "secondary",
            ):
                st.session_state.data["color"] = color
                st.rerun()

st.write("---")

html_output = generate_html(st.session_state.data)
st.subheader("📄 Vygenerovaný HTML")

col1, col2 = st.columns(2)
with col1:
    st.download_button(
        "💾 Stáhnout HTML", html_output, file_name="portfolio.html", mime="text/html"
    )
with col2:
    b64 = base64.b64encode(html_output.encode()).decode()
    st.markdown(
        f'<a href="data:text/html;base64,{b64}" download="portfolio.html">📥 Alternativní stažení</a>',
        unsafe_allow_html=True,
    )

st.write("---")
st.subheader("🔍 Náhled")

st.components.v1.iframe(
    f"data:text/html;base64,{base64.b64encode(html_output.encode()).decode()}",
    height=600,
    scrolling=True,
)
