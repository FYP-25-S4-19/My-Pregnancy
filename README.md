# My-Pregnancy

A mobile application designed to support women throughout their pregnancy

---

## Quick start

You will need two terminals - one for the frontend and one for the backend

### Prerequisites

- [Node.js _(via nvm)_](https://nodejs.org/en/download)
  - Install the LTS: `nvm install --lts && nvm use --lts`
- [Python](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/)
- [Android Studio](https://developer.android.com/studio)

### Frontend

1. `cd frontend`
2. **[First time]** Install dependencies: `npm i`
3. Start:
   - Android emulator: `npm run android`
   - iOS _(macOS only)_: `npm run ios`
   - Web: `npm run web`
4. Stop: `Ctrl-C`

### Backend

1. `cd backend`
2. `docker compose up -d --build`
3. To stop, just `docker compose down`

---

## Building, Deployment, and You

#### Managing Python Dependencies

If you ever need to install or uninstall a new Python package during development, make sure that you first activate a virtual environment _(venv)_, and then update the `requirements.txt` after

1. **[First time]** Create venv: `python -m venv venv`
2. _(Once per run)_ Activate venv - do this BEFORE installing new libraries:
   - Linux/MacOS: `source venv/bin/activate`
   - Windows CMD: `venv\Scripts\Activate.bat`
3. Modify installed packages/libraries as necessary...
   - Install: `pip install <package_name>`
   - Uninstall: `pip uninstall <package_name>`
4. Update requirement list: `pip freeze > requirements.txt`
5. Deactivate venv: `deactivate`

#### Creating Docker image for deployment

- Build image: `docker build -t my-image-name:tag`
- Verify: `docker images` _("my-image-name" should be listed)_
- Push to registry: `docker push <registry_url>/my-image-name:tag`
