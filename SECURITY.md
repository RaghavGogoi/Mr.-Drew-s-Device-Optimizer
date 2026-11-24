# Security Policy

## Overview

Mr. Drew's Device & FPS Optimizer is designed with the highest standards of safety, system stability, and data privacy. Because the application interacts directly with Windows NT kernel APIs, system memory management (`EmptyWorkingSet`, `NtSetSystemInformation`), process priorities, and file caches, security is a paramount concern.

---

## Supported Versions

| Version | Supported | Status |
| :--- | :--- | :--- |
| **2.5.x** | :white_check_mark: | Currently Supported (Active Maintenance) |
| **2.0.x - 2.4.x** | :x: | Deprecated |
| **< 2.0.x** | :x: | Unsupported |

---

## Architecture & System Safety Principles

### 1. Zero Telemetry & 100% Local Execution
* Mr. Drew's Device Optimizer operates **entirely offline** on your local workstation.
* No personal data, hardware telemetry, process names, or diagnostic reports are ever transmitted to any remote cloud server or external third-party service without your explicit manual action.

### 2. Immutable System Process Whitelist
* The application enforces an immutable, non-bypassable whitelist of critical operating system services:
  * `csrss.exe`, `smss.exe`, `wininit.exe`, `services.exe`, `lsass.exe`, `svchost.exe`, `explorer.exe`, `dwm.exe`, `securityhealthservice.exe`, `smartscreen.exe`, and kernel tasks.
* Under no circumstances can these processes be terminated, trimmed unsafely, or suspended through the interface or API.

### 3. Strict Directory Traversal Guards
* File cleaning operations (Temporary file purging, GPU shader cache sweep) strictly enforce path sanitization:
  * Only predefined system directories (`%TEMP%`, `%SystemRoot%\Temp`, official NVIDIA, AMD, DirectX, Intel cache directories) are cleaned.
  * Relative directory traversal tokens (`..`, symlink junctions) are strictly rejected to prevent accidental file deletion outside designated cache folders.

### 4. Privilege Elevation Safety
* Administrative privilege elevation is handled strictly via the documented Windows `ShellExecuteW(..., "runas", ...)` protocol prompting standard Windows User Account Control (UAC).
* Process token adjustments are limited strictly to required performance privileges (`SeProfileSingleProcessPrivilege`, `SeIncreaseQuotaPrivilege`, `SeIncreaseBasePriorityPrivilege`).

---

## Reporting a Security Vulnerability

If you discover a security vulnerability or potential privilege escalation vector in Mr. Drew's Device Optimizer, please report it responsibly:

1. **Do NOT report security vulnerabilities via public GitHub issues.**
2. Send an email with technical details, steps to reproduce, and environment specs to:
   * **Security Contact:** `raghavgogoigamerz@gmail.com`
   * **Subject Line:** `[SECURITY] Vulnerability Report - Mr. Drew's Device Optimizer`
3. Please include:
   * Operating system version and architecture (e.g. Windows 11 x64 build 26100)
   * Detailed explanation of the vulnerability
   * Proof of Concept (PoC) code or exact steps to reproduce
   * Potential impact assessment

### Response Timeline
* **Initial Response:** Within 48 hours.
* **Triage & Reproduction:** Within 5 business days.
* **Patch Release & Disclosure Coordination:** As soon as verified and remediated.

We thank the security research community for their contributions to keeping system optimization tools safe and reliable.
