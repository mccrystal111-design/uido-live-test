# UiDo Beta Environment

This is the temporary, no-production-cost beta path for UiDo course delivery.

## Purpose

Prove the complete flow with real course data before choosing production cloud infrastructure:

1. acquire source data automatically;
2. build a provider-neutral UiDo course package;
3. publish an approved beta package to a temporary static cloud host;
4. download the package from the phone;
5. run the round flow offline.

## Beta storage

The first beta delivery target is GitHub Pages. It is deliberately disposable and keeps the runtime contract identical to a future object-storage/CDN deployment.

GitHub Actions remains the build system. Actions artifacts are temporary build evidence; the Pages site is the beta delivery layer.

## Courses

- Overstone Park — reference course and first end-to-end target.
- Second course — deliberately independent course used to prove the factory is not Overstone-specific.

## Production boundary

Nothing in this beta is treated as production infrastructure or a production SLA.

The stable contract is the UiDo Course Package:

Course Factory -> UiDo package -> beta delivery -> UiDo runtime

The eventual storage provider can change without changing the runtime package contract.
