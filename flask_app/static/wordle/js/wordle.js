var wordOfTheDay="";
var number_of_letters = 1;
var currentWord="";
var currentWordSpelling = 0;
var currentCell;
var startTime=-1;
var endTime;
var timeElapsed;
const keyboardButtons = document.querySelectorAll('.kb-button');

//initialize the Wordle game board
document.addEventListener('DOMContentLoaded', function() {
    fetch('/get_word_of_day')
        .then(response => response.json())
        .then(data => {
            wordOfTheDay = data.hidden_word;
            number_of_letters = wordOfTheDay.length;
            initializeWordle();
        });
});

// Function to handle virtual keyboard button click
function handleButtonClick(key) {
    const virtualEvent = new KeyboardEvent('keydown', { key: key });
    document.dispatchEvent(virtualEvent);
}

// Event listener for virtual keyboard button click
keyboardButtons.forEach(button => {
    button.addEventListener('click', function () {
        const key = this.innerHTML;
        handleButtonClick(key);
    });
});

function initializeWordle() {
    var wordleGame = document.getElementById('wordleGame');

    //create n x n grid
    for (var i = 0; i < number_of_letters; i++) {
        var row = document.createElement('div');
        row.classList.add('row');

        for (var j = 0; j < number_of_letters; j++) {
            var cell = document.createElement('div');
            cell.classList.add('cell');
            cell.id = 'cell_' + i + '_' + j;

            row.appendChild(cell);
        }

        wordleGame.appendChild(row);
    }
    currentCell = document.getElementById('cell_0_0');
}

// Add event listener for keydown events
document.addEventListener('keydown', function (event) {

    var wordleGameElement = document.getElementById("wordleGame");
    var wordleGameStyle = window.getComputedStyle(wordleGameElement);

    //if game is initialized and game is being displayed
    //keyboard doesnt need to be active during leaderboard display
    if (currentCell && wordleGameStyle.display !== "none") {
        guessLetter(event);
    }
});

// Function to handle user's letter guesses
async function guessLetter(event) {

    // Check if the pressed key is a letter (A-Z)
    if (event.key.match(/^[a-zA-Z]$/)) {

        //if time not started yet
        if(startTime===-1){
            //as soon as user types their first letter, time is started
            startTime= new Date();
        }
        // Update the content of the current cell
        currentCell.innerHTML = event.key.toUpperCase();

        // Move to the next cell
        var nextCell = getNextCell(currentCell);
        if (nextCell) {
            currentCell = nextCell;
        }
    } 
    else if (event.key === 'Backspace' || event.key === 'Delete') {
        if (currentCell.innerHTML != ''){
            // Delete the letter in the current cell
            currentCell.innerHTML = '';
        }
        else{
            // Move to the previous cell
            var previousCell = getPreviousCell(currentCell);
            if (previousCell) {
                previousCell.innerHTML = '';
                currentCell=previousCell;
            }
        }
    }
    else if (event.key === 'Enter') {
        // If the current row is valid, move to the first cell in the next row
        if (await checkCurrentRowValid(currentCell)) {

            var cellColors = compareWithWordOfDay(currentWord);
            updateCellColors(currentCell, cellColors);
            
            var gameStatusElement = document.getElementById("gameStatus");
            //if all cell colors green i.e. or used all guesses
            if (currentWord===wordOfTheDay){
                gameStatusElement.textContent = "You Won! Worlde's word of the day is...";
                processGameOver("Won");
            }
            else if (goToNextRow(currentCell)===null){
                gameStatusElement.textContent = "You lost! Worlde's word of the day is...";
                processGameOver("Lost");
            }
            var nextRowCell = goToNextRow(currentCell);
            if (nextRowCell) {
                currentCell = nextRowCell;
            }
        }
    }
}

// Function to get the next cell
function getNextCell(currentCell) {
    var nextCell = currentCell.nextElementSibling;
    // If next cell exists in the same row, return it
    if (nextCell) {
        return nextCell;
    }
    else{
        return null;
    }
}
// Function to get the previous cell
function getPreviousCell(currentCell) {
    var previousCell = currentCell.previousElementSibling;

    // If previous cell exists in the same row, return it
    if (previousCell) {
        return previousCell;
    }
    return null;
}
// Function to go to the first cell in the next row
function goToNextRow(currentCell) {
    var nextRow = currentCell.parentElement.nextElementSibling;

    // If next row exists, return the first cell in that row
    return nextRow ? nextRow.querySelector('.cell') : null;
}

async function checkCurrentRowValid(currentCell){
    //1: Check if the current row is valid (all cells have letters)
    var currentRow = currentCell.parentElement;
    var allCellsFilled = Array.from(currentRow.children).every(function (cell) {
        return cell.innerHTML.trim() !== '';
    });

    //2: check if the entered word exists in English lang
    if (allCellsFilled) {
        currentWord = Array.from(currentRow.children).map(function (cell) {
            return cell.innerHTML;
        }).join('').toLowerCase(); // Concatenate cell content and convert to lowercase

        await spellCheckWord();
        if(currentWordSpelling===0){
            showSpellingAlert("Invalid word! Please check your spelling.");
        }
        return currentWordSpelling===1;
        
    }else {
        // If not all cells are filled, resolve with false
        return Promise.resolve(false);
    }
}


async function spellCheckWord() {
    try {
        const response = await fetch('/spell_check', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "word": currentWord })
        });

        if (response.ok) {
            console.log("Backend spell check request worked");
            const data = await response.json();
            currentWordSpelling = data.spelling_correct; //1 means correct else 0
        } else {
            console.error('Spell check request failed:', response.statusText);
        }
    } catch (error) {
        console.error('Error during spell check:', error);
    }
}


// Function to compare the user's guess with the hidden word
function compareWithWordOfDay(word) {
    var cellColorResult = [];

    for (var i = 0; i < wordOfTheDay.length; i++) {
        var guessedChar = word[i];
        var actualChar = wordOfTheDay[i];

        if (guessedChar === actualChar) {
            // Correct character in correct location (green)
            cellColorResult.push('green');
        } else if (wordOfTheDay.includes(guessedChar)) {
            // Correct character in incorrect location (yellow)
            cellColorResult.push('yellow');
        } else {
            // Character does not show up anywhere in the hidden word (grey)
            cellColorResult.push('grey');
        }
    }
    return cellColorResult;
}

// Update the cell colors in the current row based on the result array
function updateCellColors(currentCell, colors) {
    var cells = currentCell.parentElement.querySelectorAll('.cell');

    for (var i = 0; i < cells.length; i++) {
        cells[i].style.backgroundColor = colors[i];
    }
}

async function processGameOver(gameStatus) {
    // Hide the wordleGame
    var wordleGame = document.getElementById('wordleGame');
    wordleGame.style.display = 'none';

    //only update current users time if they beat the game
    if (gameStatus === "Won"){
        endTime = new Date();

        timeElapsed = endTime - startTime;

        timeElapsed /= 1000;
        // get seconds 
        var timeElapsed = Math.round(timeElapsed);

        await updateCurrentUsersTime(timeElapsed);
    }
    // Display the leaderboard
    await updateLeaderboard();
}

async function updateCurrentUsersTime(timeElapsed) {

    await fetch('/update_time_taken', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'time_elapsed': timeElapsed })
    })
    .then(response => response.json())
    .then(data => {
        console.log("updated user's time_elapsed");
    })
    };

async function updateLeaderboard() {
    // Fetch leaderboard data
    await fetch('/leaderboard')
        .then(response => response.json())
        .then(data => {
            updateTable(data);
        });
}

function updateTable(leaderboardData) {
    var wordOfDataElement = document.getElementById("wordOfDay");
    wordOfDataElement.textContent = wordOfTheDay;
    var leaderboardBody = document.getElementById('leaderboardBody');

    // Clear existing table content
    leaderboardBody.innerHTML = '';

    // Iterate through the leaderboard data and update the table
    leaderboardData.leaderboard.forEach(function(user) {

            var row = document.createElement('tr');
            var usernameCell = document.createElement('td');
            var timeCell = document.createElement('td');

            usernameCell.textContent = user.email;
            timeCell.textContent = user.time_taken;

            row.appendChild(usernameCell);
            row.appendChild(timeCell);

            leaderboardBody.appendChild(row);
    });
    // Display the leaderboard table
    var leaderboard = document.getElementById('leaderboard');
    leaderboard.style.display = 'block';
}

function showSpellingAlert(message) {
    var spellingAlert = document.getElementById('spelling-alert');
    spellingAlert.innerHTML = message;

    // Show the notification
    spellingAlert.style.display = 'block';
    setTimeout(function() {
        spellingAlert.style.display = 'none';
    }, 2000);
}
