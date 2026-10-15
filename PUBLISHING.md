# Publish this demonstration

The public repository is intended to be named `antiscalant-dosage-ml-project`.
This guide describes the publication procedure; it does not report the current remote publication status.

1. Review the README, notebook outputs and every file to be published. Include only the synthetic demonstration; never copy private internship files into this folder.
2. Create an empty public repository on your GitHub account, without adding a README or license remotely.
3. From this folder, stage the explicit public artifact list and review the diff:

```bash
git add .gitignore README.md PUBLISHING.md requirements.txt src tests notebooks data/synthetic reports
git diff --cached --stat
git diff --cached
```

4. After review, commit using your own Git identity and push:

```bash
git commit -m "Add reproducible synthetic antiscalant regression demonstration"
git remote add origin https://github.com/ImaneTayf/antiscalant-dosage-ml-project.git
git push -u origin main
```

Authentication and permission to write to the account are required. If Git requests a name or email, configure your own identity; a GitHub private commit email can be used. No license has been selected on your behalf.

Only after a successful push and checking the repository while signed out should you use its URL in an application.
