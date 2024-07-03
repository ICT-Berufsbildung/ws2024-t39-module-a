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
  # Grade only aspect A01_01
  root@fw01:~/ws2024-t39-module-a/grading# ./grading -t a01_01

  _ _ _ ____ ____    _  _ ____ ___  _  _ _    ____    ____
  | | | [__  |       |\/| |  | |  \ |  | |    |___    |__|
  |_|_| ___] |___    |  | |__| |__/ |__| |___ |___    |  |
  
  ____ ____ ____ ____ ____    ____ ____ ___  ____ ____ ___
  [__  |    |  | |__/ |___    |__/ |___ |__] |  | |__/  |
  ___] |___ |__| |  \ |___    |  \ |___ |    |__| |  \  |
  
  ===========================================================================
  => [A01_01] LDAP port tcp/389 is reachable:                              0.1
  ---------------------------------------------------------------------------
  # Grade only aspects A01_01 & A01_03
  (venv) root@fw01:~/ws2024-t39-module-a/grading# ./grading -t A01_01 A01_03
  
  _ _ _ ____ ____    _  _ ____ ___  _  _ _    ____    ____
  | | | [__  |       |\/| |  | |  \ |  | |    |___    |__|
  |_|_| ___] |___    |  | |__| |__/ |__| |___ |___    |  |
  
  ____ ____ ____ ____ ____    ____ ____ ___  ____ ____ ___
  [__  |    |  | |__/ |___    |__/ |___ |__] |  | |__/  |
  ___] |___ |__| |  \ |___    |  \ |___ |    |__| |  \  |
  
  ===========================================================================
  => [A01_01] LDAP port tcp/389 is reachable:                              0.1
  ---------------------------------------------------------------------------
  => [A01_03] User Jamie exists and can login:                             0.3
  ===========================================================================
  (venv) root@fw01:~/ws2024-t39-module-a/grading#
  # Grade all aspects from subcriterion A04
  (venv) root@fw01:~/ws2024-t39-module-a/grading# ./grading -t a04

  _ _ _ ____ ____    _  _ ____ ___  _  _ _    ____    ____
  | | | [__  |       |\/| |  | |  \ |  | |    |___    |__|
  |_|_| ___] |___    |  | |__| |__/ |__| |___ |___    |  |
  
  ____ ____ ____ ____ ____    ____ ____ ___  ____ ____ ___
  [__  |    |  | |__/ |___    |__/ |___ |__] |  | |__/  |
  ___] |___ |__| |  \ |___    |  \ |___ |    |__| |  \  |
  
  ===========================================================================
  => [A04_01] int-srv01 is listening on tcp/53 for IPv4 AND IPv6:          0.1
  ---------------------------------------------------------------------------
  => [A04_02] A & PTR exists for int-srv01.int.worldskills.org.:           0.1
  ===========================================================================
  => [A04_03] AAAA & PTR exists for int-srv01.int.worldskills.org.:        0.1
  ---------------------------------------------------------------------------
  => [A04_04] SRV record for int-srv01.int.worldskills.org exists:         0.2
  ===========================================================================
  => [A04_05] int-srv01 is a recursive name server:                        0.2
  ---------------------------------------------------------------------------
  => [A04_06] int-srv01 is secondary for dmz.worldskills.org.:             0.1
  ===========================================================================
  => [A04_07] int-srv01 is secondary for 20.1.10.in-addr.arpa.:            0.1
  ---------------------------------------------------------------------------
  => [A04_08] int-srv01 is secondary for IPv6 reverse zone in DMZ.:        0.1
  ===========================================================================
  ```
#### Enable verbose mode using `-v` (commands & command output)
Use `-v` to show the command, which will be executed and its output. Use this flag only together with `-t` to limit the scope as it will generate a lot of output!
  ```bash
  $./grading -t A01_02 -v
  => [A01_02] OU Employees exists:                                         0.25
Executed command on int-srv01 =>
$ ldapsearch -H ldap://localhost -b dc=int,dc=worldskills,dc=org -x "(&(objectclass=organizationalunit)(ou=Employees))" -D cn=admin,dc=int,dc=worldskills,dc=org -w Skill39
> # extended LDIF
#
# LDAPv3
# base <dc=int,dc=worldskills,dc=org> with scope subtree
# filter: (&(objectclass=organizationalunit)(ou=Employees))
# requesting: ALL
#

# Employees, int.worldskills.org
dn: ou=Employees,dc=int,dc=worldskills,dc=org
ou: Employees
objectClass: organizationalUnit

# search result
search: 2
result: 0 Success

# numResponses: 2
# numEntries: 1
  ```
