# Wordle Game
[![HTML](https://img.shields.io/badge/HTML-5E5E5E?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS](https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/doc/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/en/2.1.x/)
[![SQL](https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.w3schools.com/sql/)
[![Cryptography](https://img.shields.io/badge/Cryptography-8C88A0?style=for-the-badge&logo=cryptography&logoColor=white)](https://cryptography.io/en/latest/)
[![Beautiful Soup](https://img.shields.io/badge/Beautiful%20Soup-32B16C?style=for-the-badge&logo=beautifulsoup&logoColor=white)](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docs.docker.com/)
[![Requests](https://img.shields.io/badge/Requests-006D8E?style=for-the-badge&logo=requests&logoColor=white)](https://docs.python-requests.org/en/latest/)


Welcome to the Wordle Game project! This project is a twist on the popular word guessing game, [Wordle](https://www.nytimes.com/games/wordle/index.html). The implementation follows the similar visual and functional structure as the standard game with additional features and modifications.

## Project Overview

### 1. Reactive Front-end Design
The front-end of the Wordle Game is designed to be highly reactive, providing an engaging and responsive user experience..

### 2. Design of a Data-Driven Backend
The backend of the Wordle Game is built on a robust data-driven architecture. It efficiently manages user data, game states, and leaderboard information. The design ensures scalability and performance, providing a smooth gameplay experience.

### 3. Session Management
User sessions are managed securely to ensure a personalized experience for each player. Users are required to sign up and log in before playing the game, enhancing security and providing a tailored experience.

### 4. Asynchronous Communication
The Wordle Game utilizes asynchronous communication for real-time updates and interactions. This enhances the multiplayer experience and ensures that players receive timely feedback during the game.

### 5. Web APIs
The project incorporates Web APIs to facilitate communication between the frontend and backend components. These APIs enable data exchange, allowing the game to retrieve and update information dynamically.

## Some features


1. **User Authentication:** Players must sign up and log in before being able to play the game, adding a layer of security.

2. **Word Length Variation:** The hidden word is not limited to 5 characters. Players have a specific number of tries to guess a word of the same length (e.g., 3 tries to guess a word of length 3).

3. **Leaderboard Display:** At the end of each game (win or loss), a leaderboard is displayed, showcasing the top 5 users based on how quickly they beat that day's game.

## Run project locally 

Make sure you have docker installed. Then you can use docker-compose to host the web application locally by executing the following command from you terminal:

```bash
docker-compose -f docker-compose.yml -p wordle-container up
```

**Deploy your web application to Google Cloud**

If you have access and credits to a google cloud account, you can deploy your Dockerized App to Google Cloud by running the commands below from current directory.

```bash
gcloud builds submit --tag gcr.io/project/wordle
gcloud run deploy --image gcr.io/project/wordle --platform managed
```

Feel free to explore and enjoy the Wordle Game! 
