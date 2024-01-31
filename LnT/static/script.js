const container = document.getElementById('question-container');
const feedbackMessageEl = document.getElementById('feedback-message');
let currentQuestionIndex = 0;
let questions = [];

// Function to preload all questions
function preloadQuestions() {
    fetch('http://localhost:5000/ask-question')  // Replace with the appropriate endpoint
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(allQuestions => {
            questions = allQuestions;
            if (questions.length > 0) {
                displayQuestion();
            } else {
                container.innerHTML = '<p>No questions available.</p>';
            }
        })
        .catch(error => {
            feedbackMessageEl.textContent = 'Error fetching questions: ' + error;
        });
}

// Function to display the current question
function displayQuestion() {
    const currentQuestion = questions[currentQuestionIndex];

    if (currentQuestion) {
        console.log('Current question:', currentQuestion);

        const questionDiv = document.createElement('div');

        const questionTextEl = document.createElement('div');
        questionTextEl.textContent = currentQuestion.text;
        questionTextEl.id = 'question-text';  // Add an ID for question text

        const responseArea = document.createElement('div'); // Create the response area
        responseArea.id = 'response-area'; // Add an ID for the response area

        const responseForm = document.createElement('form');
        responseForm.addEventListener('submit', function (event) {
            event.preventDefault();
            handleResponseSubmit(currentQuestion.id, responseForm);
        });

        let responseInput;
        if (currentQuestion.type === 'descriptive') {
            responseInput = createDescriptiveInput();
            // Append the descriptive input to the response area
            responseForm.appendChild(responseInput);
        } else if (currentQuestion.type === 'yes_no') {
            responseInput = createTrueFalseOptions();
            responseForm.appendChild(responseInput); // Append true/false options directly
        } else if (currentQuestion.type === 'mcq') {
            responseInput = createMcqOptions(currentQuestion.options);
            responseForm.appendChild(responseInput); // Append MCQ options to the form
        }

        const submitButton = document.createElement('button');
        submitButton.type = 'submit';
        submitButton.textContent = 'Submit';
        submitButton.id = 'submit-button';

        responseForm.appendChild(submitButton);

        questionDiv.appendChild(questionTextEl);
        questionDiv.appendChild(responseForm);

        // Ensure that questionDiv is a valid DOM element
        if (questionDiv instanceof Node) {
            // Append the new questionDiv directly without clearing the container
            container.innerHTML = ''; // Clear the container before appending the new question
            container.appendChild(questionDiv);
        } else {
            console.error('Error creating questionDiv:', questionDiv);
        }
    } else {
        container.innerHTML = '<p>No more questions available.</p>';
    }
}

// Function to create a descriptive input
function createDescriptiveInput() {
    const input = document.createElement('textarea');
    input.name = 'answer';
    input.placeholder = 'Your answer...';
    input.style.width = '100%'; // Set the text area to 100% width
    input.style.height = '100%'; // Set the text area to 100% height
    input.style.resize = 'none'; // Prevent resizing
    input.style.border = 'none';
    return input;
}

// Function to create true/false options
function createTrueFalseOptions() {
    const trueOption = document.createElement('input');
    trueOption.type = 'radio';
    trueOption.name = 'answer';
    trueOption.value = 'true';
    trueOption.id = 'true-option';

    const falseOption = document.createElement('input');
    falseOption.type = 'radio';
    falseOption.name = 'answer';
    falseOption.value = 'false';
    falseOption.id = 'false-option';

    const trueLabel = document.createElement('label');
    trueLabel.htmlFor = 'true-option';
    trueLabel.textContent = 'True';

    const falseLabel = document.createElement('label');
    falseLabel.htmlFor = 'false-option';
    falseLabel.textContent = 'False';

    const optionsContainer = document.createElement('div');
    optionsContainer.appendChild(trueOption);
    optionsContainer.appendChild(trueLabel);
    optionsContainer.appendChild(falseOption);
    optionsContainer.appendChild(falseLabel);

    return optionsContainer;
}

// Function to create multiple-choice options
function createMcqOptions(options) {
    const ul = document.createElement('ul');
    ul.classList.add('options-list'); // Add a class for styling

    options.forEach((option, index) => {
        const li = document.createElement('li');
        li.style.listStyleType = 'none'; // Remove bullet points

        const radio = document.createElement('input');
        radio.type = 'radio';
        radio.name = 'answer';
        radio.value = index; // Assuming the index is the correct answer
        
        // Create a label for the radio button and place it after the radio button
        const label = document.createElement('label');
        label.textContent = option;
        label.style.fontWeight = 'bold'; // Make the text bold
        label.style.textAlign = 'left'; // Align the text to the left

        li.appendChild(radio);
        li.appendChild(label);
        
        ul.appendChild(li);
    });
    return ul;
}



let startTime = null; // Initialize startTime to null

function startTimer() {
    startTime = new Date().getTime(); // Capture the start time
}

function handleResponseSubmit(questionId, form) {
    const formData = new FormData(form);
    const userResponse = formData.get('answer');

    // If startTime is null, initialize the timer
    if (startTime === null) {
        startTimer();
    } else {
        // Capture the time before submitting the form in milliseconds
        const currentTime = new Date().getTime();

        // Calculate elapsed time in seconds
        const elapsedTime = (currentTime - startTime) / 1000;

        // Extract the email from the hidden div element
        const emailElement = document.getElementById('user-email');
        const email = emailElement.textContent;

        // Create an object to send as JSON
        const postData = {
            questionId,
            userResponse,
            elapsedTime,
            email, // Include the email from the hidden div
        };

        // Send the JSON data to the backend
        fetch('http://localhost:5000/submit-answers', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(postData),
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response from the server if needed
            console.log(data);

            // Move to the next question
            currentQuestionIndex += 1;

            // Reset the timer
            startTimer();

            // Display the next question
            displayQuestion();
        })
        .catch(error => {
            console.error('Error submitting response:', error);
        });
    }
}


// Example: Start the timer when fetching questions
startTimer();

// Load all questions initially
preloadQuestions();
