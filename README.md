## Database
1. Start the docker container with the MongoDB server
```
docker-compose up -d
```

## Backend Setup

1. Navigate to the `backend` directory:
   ```bash
   cd server
   ```

2. Create a Python virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
    ```bash
    source venv/bin/activate
    ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the Flask application:
   ```bash
   python app.py
   ```

## Frontend Setup

1. Navigate to the `frontend` directory:
   ```bash
   cd web
   ```

2. Install the required dependencies:
   ```bash
   npm i
   ```

3. Run the Vue.js application:
   ```bash
   npm run dev
   ```
