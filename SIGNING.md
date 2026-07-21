# Code signing (free, via SignPath Foundation)

The Windows `.exe` is unsigned by default, so Windows SmartScreen / Smart App
Control shows a "publisher not verified" warning. **SignPath Foundation** signs
open-source projects **for free**. The CI is already wired for it — once the
project is approved and configured, every release is signed automatically.

## One-time setup

1. **Apply** for free OSS signing at **https://signpath.io/open-source**
   with this repository (`swayz-editing/swayz-downloader`).
   Eligibility: public repo ✅, OSI license (MIT) ✅, built in CI ✅.

2. Once approved, in the **SignPath** dashboard:
   - Note your **Organization ID**.
   - Create a **Project** (slug e.g. `swayz-downloader`) linked to this GitHub repo.
   - Create a **Signing Policy** (slug e.g. `release-signing`).
   - Create an **API token** (User settings → API tokens).

3. **Install the SignPath GitHub App** on the repo (SignPath will prompt you;
   it lets SignPath read the build artifact from GitHub Actions).

4. In GitHub: **Settings → Secrets and variables → Actions**
   - **Secret** → `SIGNPATH_API_TOKEN` = the API token
   - **Variables** →
     - `SIGNPATH_ORGANIZATION_ID` = your org id
     - `SIGNPATH_PROJECT_SLUG` = `swayz-downloader`
     - `SIGNPATH_POLICY_SLUG` = `release-signing`

5. Cut a new release (`git tag v1.0.2 && git push origin v1.0.2`). The workflow
   now signs the `.exe` automatically. Done ✅

> Notes
> - SignPath signs **Windows** (Authenticode). SmartScreen trust then builds up
>   as more people download the signed app.
> - **macOS** notarization is separate (needs a paid Apple Developer account,
>   $99/yr) — until then, users right-click → Open. **Linux** has no such gate.
