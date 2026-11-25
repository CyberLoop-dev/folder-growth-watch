<p align="center"><img src="https://capsule-render.vercel.app/api?type=waving&color=0:111827,100:0f766e&height=170&section=header&text=Folder%20Growth%20Watch&fontSize=38&fontColor=ffffff" alt="Folder Growth Watch header"/></p>
<p align="center"><img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=19&duration=2800&pause=900&center=true&vCenter=true&width=820&lines=Folder%20Growth%20Watch%20%E2%80%A2%20Track%20how%20a%20folder%20changes%20between%20snapshots%20using%20file%20sizes%20and%20modification%20times%20without%20reading%20file%20contents%20or%20deleting%20anything." alt="Animated project title"/></p>
<p align="center"><img src="https://img.shields.io/github/license/CyberLoop-dev/folder-growth-watch?style=flat-square" alt="License"/> <img src="https://img.shields.io/github/languages/top/CyberLoop-dev/folder-growth-watch?style=flat-square" alt="Language"/> <img src="https://img.shields.io/github/stars/CyberLoop-dev/folder-growth-watch?style=flat-square" alt="Stars"/> <img src="https://img.shields.io/github/last-commit/CyberLoop-dev/folder-growth-watch?style=flat-square" alt="Last commit"/></p>

![Project illustration](assets/mark.svg)

## 🔎 Overview
Track how a folder changes between snapshots using file sizes and modification times without reading file contents or deleting anything.

## ✨ Features
- 📸 Records relative paths, file sizes, and modification times
- 📈 Compares the two most recent snapshots and totals byte growth
- 🆕 Lists new, removed, and size-changed files
- 🔒 Reads metadata only; it never opens file contents or deletes files
- 🧾 Stores history as a portable JSON file

## 🎬 Demo
No hosted demo is published. Run the project locally using the Quick Start command below.

## 🚀 Quick Start
    python -m folder_growth_watch snapshot ./Downloads --store ./growth-history.json
    python -m folder_growth_watch report --store ./growth-history.json

## 🧰 Tech Stack
- Python 3.10+
- pathlib, os, json, argparse
- unittest

## 🗂️ Folder Structure
    folder_growth_watch/cli.py      Snapshot and report commands
    folder_growth_watch/__main__.py Module entry point
    tests/test_cli.py                 Temporary-directory tests
    pyproject.toml                    Package metadata

## 🛣️ Roadmap
- [ ] Add CSV report export
- [ ] Add optional exclusion patterns

## 🤝 Contributing
Issues and pull requests are welcome. Keep changes focused, document behavior, and add a small reproducible example for new features.

## 📄 License
Released under the MIT License. See LICENSE.

<p align="center"><img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f766e,100:111827&height=110&section=footer" alt="Animated footer wave"/></p>
