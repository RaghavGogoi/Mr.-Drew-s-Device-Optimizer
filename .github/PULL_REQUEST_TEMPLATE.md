## Description
Provide a concise overview of the changes implemented in this pull request and the motivations behind them.

## Type of Change
- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ⚡ Performance optimization (latency reduction, memory compaction, C++ speedup)
- [ ] ✨ New feature (non-breaking addition to functionality)
- [ ] 🛡️ Security hardening (safety whitelist, privilege management, path sanitization)
- [ ] 🎨 UI / UX refinement (themes, shaders, accessibility, design system)
- [ ] 📝 Documentation update

## Verification & Testing
Describe the tests you ran to verify your changes:
- [ ] Automated unit test suite executed (`python -m unittest discover tests -v`)
- [ ] Native C++ engine recompiled and verified (`DeviceOptimizer.exe --help`, `--sys-specs`)
- [ ] Tested on Windows 10 / 11 64-bit workstation
- [ ] Standalone build verified (`dist/DeviceOptimizerGUI`)

## Checklist
- [ ] My code adheres to the style guidelines of this project.
- [ ] I have performed a self-review of my own code.
- [ ] I have commented my code, particularly in complex Win32/NT kernel API sections.
- [ ] New and existing unit tests pass locally with my changes.
- [ ] No personal credentials, API keys, or sensitive telemetry paths are committed.
