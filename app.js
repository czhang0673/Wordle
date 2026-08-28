const board = document.getElementById("board"); /* const prevents reassignment. note that if you assign a const to an array, you can still change that array */
const rows = 6;
const columns = 5;

let currentRow = 0; /* let = a variable that changes */
let currentCol = 0;

function initializeBoard() {
	for (let r = 0; r < rows; r++) {
		for (let c = 0; c < columns; c++) {
			let tile = document.createElement("div")
			tile.id = r.toString() + "-" + c.toString(); /* ex. id = 0-0, 4-2*/
			tile.classList.add("tile");
			board.appendChild(tile);
		}
	}
} 

document.addEventListener("keyup", (e) => {
	if (e.code >= "KeyA" && e.code <= "KeyZ") {
		if (currentCol < columns) {
			let currTile = document.getElementById(`${currentRow}-${currentCol}`);
			currTile.innerText = e.key;
			currentCol += 1;
		}
	}
		else if (e.code === "Backspace") {
			if (currentCol > 0) {
				currentCol -= 1;
				let currTile = document.getElementById(`${currentRow}-${currentCol}`);
				currTile.innerText = "";
			}
		}
		else if (e.code === "Enter") {
			if (currentCol === columns) {
				sendGuess();
			}
		}
	}
)

//js is "single-threaded". async - mandatory warning label to use keyword await
async function sendGuess() {

	// const userInput = document.getElementById("guessInput").value;
	// console.log("User input: " + userInput);
	// const resultDisplay = document.getElementById("resultText");

	// const solutionDisplay = document.getElementById("solutionDisplay");

	// document.getElementById("guessInput").value = "";
	// resultDisplay.innerText = "Checking...";

	let guess = "";
	for (let c = 0; c < columns; c++) {
		let tile = document.getElementById(`${currentRow}-${c}`);
		guess += tile.innerText;
	}

	//packages front end keystrokes into the right format to send to backend
	const dataToSend = {
	"user_input": guess,
		"key1": "test"
	 };

	let body_content = JSON.stringify(dataToSend)
	console.log("body content:", body_content);
	
	try {
		//await tells js to pause this function and wait for backend, but run the rest of the webpage as normal
		let response = await fetch("https://nntpan6521.execute-api.us-east-2.amazonaws.com/default/testFunction0673/", {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: body_content
		});

		let resultData = await response.json();
		// console.log("Result DATA:", resultData);
		let resultArray = resultData.colors.colors;
		// console.log(resultArray);

		const classMap = ["incorrect", "contains", "correct"];
		//this is a map:

		for (let c = 0; c < columns; c++) {
			let tile = document.getElementById(`${currentRow}-${c}`);
			
			let statusNumber = resultArray[c];
			let cssClass = classMap[statusNumber]; //because it's an actual number, can just use it as the index of the array
			
			let animationDelay = c * 200;

			setTimeout(() => {
				tile.classList.add(cssClass); //this reaches into tile element and adds a class = "tile correct" if correct
			}, animationDelay); //javascript function that alllows you to delay a block of code
			
			
		}

		currentRow += 1;
		currentCol = 0;
		// if (!resultData.success) {
		// 	resultDisplay.innerText = "Error: " + resultData.message;
		// 	solutionDisplay.innerText = "Displaying random solution from database:" + JSON.stringify(resultData.solution);
		// } else {
		// 	resultDisplay.innerText = "Result: " + JSON.stringify(resultData.colors);
		// 	solutionDisplay.innerText = "Displaying random solution from database:" + JSON.stringify(resultData.solution);
		// }

	} catch (error) {
		// resultDisplay.innerText = "Error connecting to server.";
		console.error("Backend error:", error);
	}

	
}

initializeBoard();



