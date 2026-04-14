import streamlit as st
import json
import requests
import base64
import os

st.set_page_config(page_title="Portfolio Generator", page_icon="🎨")

TEMPLATES = {
    "minimal": "Minimal (tmavý)",
    "gradient": "Gradient (glassmorphism)",
    "cards": "Cards (světlý)",
    "terminal": "Terminal (retro)",
    "brutalist": "Brutalist (bold)",
    "neon": "Neon (cyberpunk)",
    "glass": "Glass (moderní)",
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
    "#ffd700": "Gold",
    "#00ffff": "Cyan",
}


def get_social_icon(platform):
    icons = {
        "github": "🐙",
        "linkedin": "💼",
        "twitter": "🐦",
        "website": "🌐",
        "email": "✉️",
        "instagram": "📷",
        "youtube": "🎬",
        "discord": "💬",
    }
    return icons.get(platform, "🔗")


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


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
    color_rgb = hex_to_rgb(color)

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
        "brutalist": f"""<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name}</title>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Space Grotesk', sans-serif; background: #fff; color: #000; min-height: 100vh; padding: 40px; }}
        .container {{ max-width: 900px; margin: 0 auto; }}
        .header {{ border-bottom: 8px solid #000; padding-bottom: 40px; margin-bottom: 40px; }}
        .name {{ font-size: 4rem; font-weight: 700; text-transform: uppercase; letter-spacing: -2px; line-height: 1; margin-bottom: 16px; }}
        .title {{ font-size: 1.5rem; font-weight: 500; background: {color}; display: inline-block; padding: 8px 16px; color: #fff; }}
        .bio {{ font-size: 1.1rem; line-height: 1.6; margin-bottom: 24px; padding: 24px; border: 4px solid #000; }}
        .info {{ display: flex; gap: 24px; font-size: 14px; font-weight: 500; margin-bottom: 24px; }}
        .social {{ display: flex; gap: 16px; margin-bottom: 40px; font-size: 24px; }}
        .social a {{ width: 48px; height: 48px; background: #000; color: #fff; display: flex; align-items: center; justify-content: center; transition: background 0.2s; }}
        .social a:hover {{ background: {color}; }}
        .section-title {{ font-size: 2rem; font-weight: 700; text-transform: uppercase; margin-bottom: 24px; border-bottom: 4px solid #000; padding-bottom: 8px; }}
        .projects-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 0; }}
        .project-card {{ position: relative; border: 4px solid #000; margin: -4px 0 0 -4px; padding: 24px; transition: background 0.2s; }}
        .project-card:hover {{ background: {color}; color: #fff; }}
        .project-card:hover .tech-tags span {{ background: rgba(255,255,255,0.3); color: #fff; }}
        .project-link {{ position: absolute; inset: 0; }}
        .project-card h3 {{ font-size: 1.25rem; font-weight: 700; margin-bottom: 8px; text-transform: uppercase; }}
        .project-card p {{ font-size: 14px; margin-bottom: 12px; }}
        .tech-tags {{ display: flex; gap: 8px; flex-wrap: wrap; }}
        .tech-tags span {{ font-size: 11px; padding: 4px 8px; background: #f0f0f0; border: 2px solid #000; text-transform: uppercase; }}
        footer {{ margin-top: 60px; border-top: 4px solid #000; padding-top: 20px; font-size: 12px; text-transform: uppercase; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="name">{name}</h1>
            <div class="title">{title}</div>
        </div>
        {f'<div class="bio">{bio}</div>' if bio else ""}
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
        "neon": f"""<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name}</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&family=Rajdhani:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Rajdhani', sans-serif; background: #0a0a0f; color: #fff; min-height: 100vh; padding: 40px 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        .name {{ font-family: 'Orbitron', sans-serif; font-size: 3rem; font-weight: 700; text-transform: uppercase; margin-bottom: 8px; text-shadow: 0 0 10px {color}, 0 0 20px {color}, 0 0 40px {color}; }}
        .title {{ font-size: 1.25rem; color: {color}; margin-bottom: 24px; text-transform: uppercase; letter-spacing: 4px; }}
        .bio {{ color: #888; line-height: 1.8; margin-bottom: 24px; padding: 20px; border-left: 3px solid {color}; background: rgba({color_rgb[0]}, {color_rgb[1]}, {color_rgb[2]}, 0.1); }}
        .info {{ display: flex; gap: 24px; margin-bottom: 24px; font-size: 14px; color: #666; }}
        .social {{ display: flex; gap: 16px; margin-bottom: 40px; font-size: 24px; }}
        .social a {{ width: 48px; height: 48px; border: 2px solid {color}; display: flex; align-items: center; justify-content: center; transition: all 0.3s; }}
        .social a:hover {{ background: {color}; box-shadow: 0 0 20px {color}; transform: translateY(-4px); }}
        .section-title {{ font-family: 'Orbitron', sans-serif; font-size: 1.5rem; color: {color}; margin-bottom: 24px; text-transform: uppercase; letter-spacing: 2px; }}
        .projects-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }}
        .project-card {{ position: relative; padding: 24px; background: linear-gradient(135deg, rgba(20,20,30,0.9), rgba(10,10,15,0.9)); border: 1px solid {color}40; transition: all 0.3s; }}
        .project-card:hover {{ border-color: {color}; box-shadow: 0 0 30px {color}30; transform: translateY(-4px); }}
        .project-link {{ position: absolute; inset: 0; }}
        .project-card h3 {{ font-family: 'Orbitron', sans-serif; font-size: 1rem; margin-bottom: 8px; color: {color}; text-transform: uppercase; }}
        .project-card p {{ font-size: 14px; color: #888; margin-bottom: 12px; }}
        .tech-tags {{ display: flex; gap: 8px; flex-wrap: wrap; }}
        .tech-tags span {{ font-size: 10px; padding: 4px 10px; background: {color}20; border: 1px solid {color}; color: {color}; text-transform: uppercase; letter-spacing: 1px; }}
        footer {{ margin-top: 60px; color: #444; font-size: 12px; text-align: center; text-transform: uppercase; letter-spacing: 2px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1 class="name">{name}</h1>
        <div class="title">{title}</div>
        {f'<div class="bio">{bio}</div>' if bio else ""}
        <div class="info">
            {f"<span>📍 {location}</span>" if location else ""}
            {f"<span>✉️ {email}</span>" if email else ""}
        </div>
        {f'<div class="social">{social_html}</div>' if social_html else ""}
        {f'<div class="section-title">// Projekty</div><div class="projects-grid">{projects_html}</div>' if projects_html else ""}
        <footer>Generated with Portfolio Generator</footer>
    </div>
</body>
</html>""",
        "glass": f"""<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name}</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; background: #0f0f23; background-image: radial-gradient(at 100% 0%, hsla(253,16%,7%,1) 0, transparent 50%), radial-gradient(at 0% 100%, hsla(225,39%,30%,1) 0, transparent 50%); min-height: 100vh; color: #fff; padding: 60px 20px; }}
        .container {{ max-width: 900px; margin: 0 auto; }}
        .profile-card {{ background: rgba(255,255,255,0.05); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.1); border-radius: 24px; padding: 48px; margin-bottom: 40px; text-align: center; }}
        .avatar {{ width: 120px; height: 120px; border-radius: 50%; background: linear-gradient(135deg, {color}, {color}80); margin: 0 auto 24px; display: flex; align-items: center; justify-content: center; font-size: 48px; box-shadow: 0 8px 32px {color}40; }}
        .name {{ font-size: 2rem; font-weight: 700; margin-bottom: 8px; background: linear-gradient(135deg, #fff, #aaa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .title {{ font-size: 1rem; color: {color}; margin-bottom: 20px; font-weight: 500; }}
        .bio {{ color: rgba(255,255,255,0.7); line-height: 1.7; max-width: 500px; margin: 0 auto 24px; }}
        .info {{ display: flex; justify-content: center; gap: 24px; font-size: 14px; color: rgba(255,255,255,0.5); margin-bottom: 24px; }}
        .social {{ display: flex; justify-content: center; gap: 12px; }}
        .social a {{ width: 44px; height: 44px; border-radius: 50%; background: rgba(255,255,255,0.1); display: flex; align-items: center; justify-content: center; transition: all 0.3s; backdrop-filter: blur(10px); }}
        .social a:hover {{ background: {color}; transform: translateY(-4px); box-shadow: 0 8px 24px {color}40; }}
        .section-title {{ font-size: 1.5rem; font-weight: 700; margin-bottom: 24px; background: linear-gradient(135deg, #fff, #aaa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .projects-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }}
        .project-card {{ position: relative; background: rgba(255,255,255,0.03); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 28px; transition: all 0.3s; }}
        .project-card:hover {{ background: rgba(255,255,255,0.06); border-color: {color}50; transform: translateY(-4px); }}
        .project-link {{ position: absolute; inset: 0; border-radius: 16px; }}
        .project-icon {{ width: 52px; height: 52px; border-radius: 14px; background: linear-gradient(135deg, {color}40, {color}20); margin-bottom: 20px; display: flex; align-items: center; justify-content: center; font-size: 22px; }}
        .project-card h3 {{ font-size: 1.1rem; font-weight: 600; margin-bottom: 8px; }}
        .project-card p {{ font-size: 14px; color: rgba(255,255,255,0.6); margin-bottom: 16px; line-height: 1.6; }}
        .tech-tags {{ display: flex; gap: 8px; flex-wrap: wrap; }}
        .tech-tags span {{ font-size: 11px; padding: 6px 12px; background: rgba(255,255,255,0.08); border-radius: 20px; color: rgba(255,255,255,0.7); }}
        footer {{ margin-top: 60px; text-align: center; color: rgba(255,255,255,0.3); font-size: 13px; }}
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
    }

    return templates.get(template, templates["minimal"])


def generate_with_ai(prompt, api_key, model="gpt-3.5-turbo"):
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "Jsi expert na psaní bio textů a popisů projektů pro portfolia.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
        }
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30,
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


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
    st.session_state.api_key = ""

st.title("🎨 Portfolio Generator")

with st.sidebar:
    st.header("⚙️ Nastavení")

    st.subheader("💾 Uložení/Načtení")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Uložit", use_container_width=True):
            json_str = json.dumps(st.session_state.data, ensure_ascii=False, indent=2)
            st.download_button(
                "Stáhnout JSON",
                json_str,
                file_name="portfolio-config.json",
                mime="application/json",
                key="download_json",
            )
    with col2:
        uploaded = st.file_uploader("📂 Načíst", type="json", key="upload_json")
        if uploaded:
            try:
                config = json.load(uploaded)
                st.session_state.data.update(config)
                st.success("✅ Načteno!")
                st.rerun()
            except:
                st.error("❌ Chyba při načítání")

    st.divider()

    st.subheader("🤖 AI Generování")
    st.session_state.api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        help="Pro AI generování potřebujete API key z platform.openai.com",
    )

    if st.session_state.api_key:
        with st.expander("✨ AI Akce"):
            if st.button("🧙‍♂️ Generovat Bio", use_container_width=True):
                with st.spinner("Generuji..."):
                    name = st.session_state.data.get("name", "vývojář")
                    title = st.session_state.data.get("title", "")
                    prompt = f"Napiš krátké a poutavé bio (2-3 věty) pro portfolio {name}, {title}. Použij profesionální tón, alebuďtrochu kreativní. V češtině."
                    result = generate_with_ai(prompt, st.session_state.api_key)
                    if not result.startswith("Error"):
                        st.session_state.data["bio"] = result
                        st.rerun()
                    else:
                        st.error(result)

            ai_project = st.selectbox(
                "Projekt pro AI popis",
                ["(vyberte)"]
                + [
                    p.get("name", f"Projekt {i}")
                    for i, p in enumerate(st.session_state.data.get("projects", []))
                ],
            )
            if ai_project != "(vyberte)" and st.button(
                "📝 AI Popis projektu", use_container_width=True
            ):
                with st.spinner("Generuji..."):
                    idx = [
                        p.get("name", f"Projekt {i}")
                        for i, p in enumerate(st.session_state.data.get("projects", []))
                    ].index(ai_project)
                    project = st.session_state.data["projects"][idx]
                    prompt = f"Napiš krátký a výstižný popis projektu '{project.get('name', '')}'.Technologie: {project.get('tech', 'neuvedeny')}. Popis by měl být 1-2 věty, profesionální, v češtině."
                    result = generate_with_ai(prompt, st.session_state.api_key)
                    if not result.startswith("Error"):
                        st.session_state.data["projects"][idx]["description"] = result
                        st.rerun()
                    else:
                        st.error(result)

tab1, tab2, tab3 = st.tabs(["📝 Profil", "🚀 Projekty", "🎭 Design"])

with tab1:
    st.subheader("Základní info")
    st.session_state.data["name"] = st.text_input(
        "Jméno", st.session_state.data["name"]
    )
    st.session_state.data["title"] = st.text_input(
        "Titulek / Profese", st.session_state.data["title"]
    )
    st.session_state.data["bio"] = st.text_area(
        "Bio", st.session_state.data["bio"], height=100
    )
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
            [
                "github",
                "linkedin",
                "twitter",
                "website",
                "email",
                "instagram",
                "youtube",
                "discord",
            ],
            key="social_platform",
        )
    with col2:
        url = st.text_input("Username / URL", key="social_url")

    if st.button("➕ Přidat síť", type="primary"):
        if url:
            st.session_state.data["social"].append({"platform": platform, "url": url})
            st.rerun()

    if st.session_state.data["social"]:
        st.write("---")
        for i, s in enumerate(st.session_state.data["social"]):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.text(f"{get_social_icon(s['platform'])} {s['platform']}: {s['url']}")
            with col2:
                if st.button("✏️", key=f"edit_social_{i}"):
                    st.session_state.data["social"][i]["url"] = st.text_input(
                        "URL", s["url"], key=f"edit_social_url_{i}"
                    )
            with col3:
                if st.button("❌", key=f"del_social_{i}"):
                    st.session_state.data["social"].pop(i)
                    st.rerun()

with tab2:
    st.subheader("GitHub Import")
    col1, col2 = st.columns([2, 1])
    with col1:
        github_user = st.text_input("GitHub username", placeholder="např. klcenka9")
    with col2:
        st.write("")
        if st.button("📥 Importovat", type="primary", use_container_width=True):
            if github_user:
                try:
                    response = requests.get(
                        f"https://api.github.com/users/{github_user}/repos?sort=updated&per_page=20",
                        timeout=10,
                    )
                    if response.status_code == 200:
                        repos = response.json()
                        st.session_state.data["projects"] = []
                        for repo in repos:
                            if not repo.get("fork", False):
                                st.session_state.data["projects"].append(
                                    {
                                        "name": repo.get("name", ""),
                                        "description": repo.get("description", "")
                                        or "",
                                        "url": repo.get("html_url", ""),
                                        "tech": "",
                                    }
                                )
                        st.success(
                            f"✅ Importováno {len(st.session_state.data['projects'])} repozitářů!"
                        )
                        st.rerun()
                    else:
                        st.error("❌ Uživatel nenalezen")
                except Exception as e:
                    st.error(f"❌ Chyba: {e}")

    st.divider()
    st.subheader("Manuální přidání")
    col1, col2 = st.columns(2)
    with col1:
        p_name = st.text_input("Název projektu", key="p_name")
        p_desc = st.text_input("Popis", key="p_desc")
    with col2:
        p_url = st.text_input("URL", key="p_url")
        p_tech = st.text_input("Technologie (oddělené čárkami)", key="p_tech")

    if st.button("➕ Přidat projekt", type="primary"):
        if p_name:
            st.session_state.data["projects"].append(
                {"name": p_name, "description": p_desc, "url": p_url, "tech": p_tech}
            )
            st.rerun()

    if st.session_state.data["projects"]:
        st.divider()
        st.subheader(f"📁 Projekty ({len(st.session_state.data['projects'])})")
        for i, p in enumerate(st.session_state.data["projects"]):
            with st.expander(f"📁 {p['name']}"):
                p["name"] = st.text_input("Název", p["name"], key=f"pn_{i}")
                p["description"] = st.text_area(
                    "Popis", p["description"], key=f"pd_{i}", height=80
                )
                p["url"] = st.text_input("URL", p["url"], key=f"pu_{i}")
                p["tech"] = st.text_input("Technologie", p["tech"], key=f"pt_{i}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("⬆️ Nahoru", key=f"up_proj_{i}"):
                        if i > 0:
                            (
                                st.session_state.data["projects"][i],
                                st.session_state.data["projects"][i - 1],
                            ) = (
                                st.session_state.data["projects"][i - 1],
                                st.session_state.data["projects"][i],
                            )
                            st.rerun()
                with col2:
                    if st.button("🗑️ Smazat", key=f"del_proj_{i}", type="primary"):
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
            is_selected = st.session_state.data["color"] == color
            if st.button(
                "🟨" if not is_selected else "✅",
                key=f"color_{color}",
                help=name,
                type="primary" if is_selected else "secondary",
            ):
                st.session_state.data["color"] = color
                st.rerun()

    st.divider()
    st.subheader("📊 Statistiky")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Projekty", len(st.session_state.data.get("projects", [])))
    with col2:
        st.metric("Sítě", len(st.session_state.data.get("social", [])))
    with col3:
        st.metric(
            "Šablona",
            TEMPLATES.get(st.session_state.data.get("template", "minimal"), ""),
        )

st.divider()

html_output = generate_html(st.session_state.data)
st.subheader("📄 Export")

col1, col2, col3 = st.columns(3)
with col1:
    st.download_button(
        "💾 Stáhnout HTML",
        html_output,
        file_name="portfolio.html",
        mime="text/html",
        type="primary",
        use_container_width=True,
    )
with col2:
    json_str = json.dumps(st.session_state.data, ensure_ascii=False, indent=2)
    st.download_button(
        "💾 Uložit JSON",
        json_str,
        file_name="portfolio-config.json",
        mime="application/json",
        use_container_width=True,
    )
with col3:
    b64 = base64.b64encode(html_output.encode()).decode()
    st.markdown(
        f'<a href="data:text/html;base64,{b64}" download="portfolio.html"><button style="width:100%;padding:0.5rem;border-radius:0.5rem;border:none;background:#0f172a;color:#fff;cursor:pointer;">📥 Přímé stažení</button></a>',
        unsafe_allow_html=True,
    )

st.divider()
st.subheader("🔍 Náhled")

st.components.v1.iframe(
    f"data:text/html;base64,{base64.b64encode(html_output.encode()).decode()}",
    height=600,
    scrolling=True,
)
