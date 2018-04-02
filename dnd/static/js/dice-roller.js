var diceLog = "";
// Roll a d6
var dice = {
    sides: 6,
    roll: function () {
        console.log("ROLLING D6")
        var randomNumber = Math.floor(Math.random() * this.sides) + 1;
        return randomNumber;
    }
}


// Get the d6 button and tell it to roll on click
var d6 = document.getElementById('d6');
d6.onclick = function() {
    logRoll(dice.roll());
};


// Log all rolls or something


function logRoll(result) {
    console.log("Starting logRoll")
    diceLog += result + "\n";
    console.log("Dice Log Value");
    console.log(diceLog);
    printLog(diceLog);
};


//Prints dice roll to the page
function printLog(number) {
    console.log("PRINTING")
    var output = document.getElementById('output');
    output.value = diceLog;
};