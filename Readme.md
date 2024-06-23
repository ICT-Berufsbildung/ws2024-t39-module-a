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
2. Create venv called venv in the current folder and enable the venv
```bash
python3 -m venv venv
. venv/bin/activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Run the grading scripts over all subcriterion (full score report)
```bash
./grading
```
### Parameters
#### Limit scope using `-t`
Use the parameter `-t` to limit the scope to a group of tasks. Examples
  ```bash
  # Grade only aspect A02_02
  ./grading -t a01_02
  # Grade only aspects A01_01 & A01_03
  ./grading -t A01_01 A01_03
  # Grade all aspects from subcriterion A04
  ./grading -t a04
  ```
#### Enable verbose mode using `-v` (commands & command output)
Use `-v` to show the command, which will be executed and its output. Use this flag only together with `-t` to limit the scope as it will generate a lot of output!
  ```bash
  ./grading -t A02_02 -v
  
  ```
