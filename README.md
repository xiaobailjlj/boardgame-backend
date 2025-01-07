# Co-Creative Board Game Generator

This project implements a co-creative system for board game design, allowing users to generate new game rules based on existing game structures and rules. The system includes a backend API for processing game data and a frontend for displaying and interacting with the generated board games.

## Requirements

To run this project, you'll need to install the necessary dependencies. These are listed in the `requirements.txt` file.

### 1. Install Dependencies

First, clone this repository and navigate into the project directory:

```bash
git clone https://github.com/VictorYiS/cc_final.git
cd cc_final
pip install -r requirements.txt
```

### 2. Running the Backend
The backend is implemented in api_boardgame.py. You can run the backend server using Python.
```bash
python api_boardgame.py
```
This will start a local server (usually at http://127.0.0.1:5000/) where the backend API will be running. The API will handle requests from the frontend and interact with the game generation logic.

### 3. Running the Frontend
The backend is implemented in api_boardgame.py. You can run the backend server using Python.
```bash
open play.html
```
Then navigate to http://localhost:8000/play.html to access the frontend interface.

### Security Notice
Do not expose the key.py file publicly. It contains your GPT API key, and sharing it could lead to unauthorized access to your OpenAI account. Please handle it securely and store it in a private location.

### Thank you for using the Co-Creative Board Game Generator!




