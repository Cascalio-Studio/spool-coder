---
name: Build Issue
about: Report problems with building or CI/CD
title: '[BUILD] '
labels: 'build, ci/cd'
assignees: ''

---

## Build Issue Description
**Describe the build problem**
A clear and concise description of what the build issue is.

## Build Environment
**Local build or CI/CD?**
- [ ] Local build on my machine
- [ ] GitHub Actions CI/CD
- [ ] Other CI system

**Operating System:**
- [ ] Windows 10/11
- [ ] macOS
- [ ] Linux (specify distro): _______________
- [ ] Other: _______________

**Python Version:**
```
python --version
# Output here
```

## Steps to Reproduce
1. Go to '...'
2. Run command '....'
3. See error

## Build Command Used
```bash
# Paste the exact command you ran
```

## Error Output
**Full error message/log:**
```
# Paste the complete error output here
```

## Expected Behavior
**What should have happened?**
A clear and concise description of what you expected to happen.

## Build Artifacts
**Did any files get created?**
- [ ] Partial build files in `build/` directory
- [ ] Executable created but won't run
- [ ] No output files at all

**File sizes and locations:**
```
# If any files were created, list them:
# ls -la dist/
# or
# dir dist\
```

## Environment Details
**Dependencies installed:**
```
pip freeze
# Output here (or just the relevant packages)
```

**System specs:**
- RAM: _____ GB
- Available disk space: _____ GB
- Architecture: _____ (x64, arm64, etc.)

## Additional Context
**Anything else that might be relevant:**
- Antivirus software running?
- Corporate firewall/proxy?
- Previous successful builds?
- Recent system updates?

## Checklist
- [ ] I have read the [CI/CD Build Guide](../docs/CI_CD_Build_Guide.md)
- [ ] I have tried the basic troubleshooting steps
- [ ] I have checked existing issues for similar problems
- [ ] I have included the complete error output
- [ ] I have specified my exact environment details
