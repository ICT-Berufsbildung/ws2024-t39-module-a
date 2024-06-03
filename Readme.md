# WorldSkills Competition 2024 - Module A Linux
This repository contains all the necessary artifacts to build the module A Linux test project for the WorldSkills competition 2024 in Lyon.

## Build VM image
### Prequisites
* Packer
* ESXi server

### Build

## Grading
The grading script is using nornir to schedule tasks. A custom output plugin has been developed to customize the output, which prints a score report.

1. Change to the grading folder: `cd grading`
2. Create venv called venv in the current folder
```bash
python3 -m venv venv
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Run grading scripts
```bash
python3 grading.py
```