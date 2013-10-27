// wac.launchpad_handler v1.1.0
// Will Crossland

//__________SETUP__________
inlets = 1;
outlets = 3;
setinletassist (0, "MIDI from Ableton / OSC to Launchpad")
setoutletassist (0, "Raw MIDI to Launchpad")
setoutletassist (1, "Raw MIDI to Ableton")
setoutletassist (2, "OSC from Launchpad")
//______________________________



//__________GLOBAL VARIABLES__________

//Current bank for each device (0=AbletonLiveMode)
var currentBank = [0, 0, 0, 0, 0, 0];

// User buttons (both must be pressed together to enter OSC modes)
var user1_state = [0, 0, 0, 0, 0, 0];
var user2_state = [0, 0, 0, 0, 0, 0];

//Flag for setting local loopback off/on
var loopback = false;

//Flag for disable/enable hardware OSC banking
var hardwareBanking = [true, true, true, true, true, true];
//______________________________________

//__________CREATE STORAGE__________
//i = device, j = bank, k = element
var data = new Array(6);
var currentLedDisplay = new Array(6);
for (var i = 0; i < 6; i++) {
    data[i] = new Array (9);
    currentLedDisplay[i] = new Array(9);
    for (var j = 0; j < 9; j++) {
        data[i][j] = new Array (80);
        currentLedDisplay[i][j] = new Array (80);
        for (var k = 0; k < 80; k++) {
            data[i][j][k] = currentLedDisplay[i][j][k] = 12
        }
    }
    createBankDisplayLeds(i);
}
//______________________________________




//__________LP NOTE/ADDRESS LOOKUP__________
//Two elements per grid location: LPmidinote, StorageElement
// Last row is more cc buttons
var yxLookup =
[
[[0,0], [1,1], [2,2], [3,3], [4,4], [5,5], [6,6], [7,7], [8,64]],
[[16,8], [17,9], [18,10], [19,11], [20,12], [21,13], [22,14], [23,15], [24,65]],
[[32,16], [33,17], [34,18], [35,19], [36,20], [37,21], [38,22], [39,23], [40,66]],
[[48,24], [49,25], [50,26], [51,27], [52,28], [53,29], [54,30], [55,31], [56,67]],
[[64,32], [65,33], [66,34], [67,35], [68,36], [69,37], [70,38], [71,39], [72,68]],
[[80,40], [81,41], [82,42], [83,43], [84,44], [85,45], [86,46], [87,47], [88,69]],
[[96,48], [97,49], [98,50], [99,51], [100,52], [101,53], [102,54], [103,55], [104,70]],
[[112,56], [113,57], [114,58], [115,59], [116,60], [117,61], [118,62], [119,63], [120,71]],
[[104,72], [105,73], [106,74], [107,75], [108,76], [109,77], [110,78], [111,79], [112,80]]
]

//Get col/row for MIDI note from LP (xy mode)
var midiNoteXYLookup =
[
[0,0], [1,0], [2,0], [3,0], [4,0], [5,0], [6,0], [7,0], [8,0],,,,,,,,
[0,1], [1,1], [2,1], [3,1], [4,1], [5,1], [6,1], [7,1], [8,1],,,,,,,,
[0,2], [1,2], [2,2], [3,2], [4,2], [5,2], [6,2], [7,2], [8,2],,,,,,,,
[0,3], [1,3], [2,3], [3,3], [4,3], [5,3], [6,3], [7,3], [8,3],,,,,,,,
[0,4], [1,4], [2,4], [3,4], [4,4], [5,4], [6,4], [7,4], [8,4],,,,,,,,
[0,5], [1,5], [2,5], [3,5], [4,5], [5,5], [6,5], [7,5], [8,5],,,,,,,,
[0,6], [1,6], [2,6], [3,6], [4,6], [5,6], [6,6], [7,6], [8,6],,,,,,,,
[0,7], [1,7], [2,7], [3,7], [4,7], [5,7], [6,7], [7,7], [8,7],,,,,,,,
];
//______________________________


//********************OSC HANDLING********************
function anything()
{
    var a = arrayfromargs(messagename, arguments);

    //make an array by splitting at "/" (OSC seperator) - first element will be null
    a = a[0];
    a = a.split("/");
    var prefix = a[1];
    var dev = a[2] * 1;
    var bank = a[3] * 1;
    var command = a[4];
    
    // validate OSC prefix
    if ("wac.lp" != prefix) { return; }

    //extract data
    var d = arrayfromargs(arguments);
    var x = (d.length >= 1) ? d[0] * 1 : 0;
    var y = (d.length >= 2) ? d[1] * 1 : 0;
    var green = (d.length >= 3) ? d[2] * 1 : 0;
    var red = (d.length >= 4) ? d[3] * 1 : 0;
    var flash = (d.length >= 5) ? d[4] * 1 : 0;


    // validate device input
    if ((dev < 0) || (dev > 5)) {
            post ();
            post ("Device (", dev, ") out of range");
            return;
    }

    // validate bank input
    if ((bank < 0) || (bank > 8)) {
            post ();
            post ("OSC bank (", bank, ") out of range");
            return;
    }

    // validate x/y input
    switch (true) {
        case x < 0:
        case x > 8:
        case y < -1:
        case y > 7:
            post ();
            post ("X/Y coordinates out of range (", x, "/", y, ")");
            return;
    }

    if ("hardwarebank" == a[3]) {
        setHardwareBanking (dev, x);
        return;
    }

    //act based on OSC command
    switch (command) {
        case "led":
            grid_led(dev, bank, x, y, green, red, flash, true, true);
            break;
        case "set":
            grid_led(dev, bank, x, y, green, red, flash, true, false);
            break;
        case "show":
            grid_led(dev, bank, x, y, green, red, flash, false, true);
            break;
        case "recall":
            grid_recall(dev, bank, x, y);
            break;
        case "refresh":
            grid_refresh(dev, bank);
            break;
        case "bank":
            change_bank(dev, bank);
            break;
        case "clear":
            clear_bank(dev, bank);
        }
}
//***********************************************************************

//__________HARDWARE MIDI HANDLING__________
   
function hw_note(dev, note, vel)
{
    if (0 == currentBank[dev]) {
        // output raw MIDI to Ableton (bank 0)
        outlet (1, dev, 144, note, vel);
        return;
    }
    
    //output OSC via lookup for user banks (1-8)
    outlet (2, "/wac.lp/" + dev + "/" + currentBank[dev] + "/press", midiNoteXYLookup[note], vel ? 1 : 0);
    if (loopback) {
        grid_led (
            dev, currentBank[dev],
            midiNoteXYLookup[note][0],
            midiNoteXYLookup[note][1],
            vel ? 1 : 0,
            0, 0, false, true);
    }                     
}


function hw_cc (dev, cc, val)
{
    if (hardwareBanking[dev]) {
        if (cc == 109) {user1_state[dev] = val > 0}
        if (cc == 110) {user2_state[dev] = val > 0}

        if (user1_state[dev] && user2_state[dev]) {
            //toggle between user (1-8)  and ableton (0) banks
            change_bank (dev, currentBank[dev] == 0 ? 1 : 0)
            return;
        }
    }

    if (0 == currentBank[dev]) {
        // send MIDI to Ableton
        outlet (1, dev, 176, cc, val);
        return;
    }

    if (hardwareBanking[dev]) {
        //change to bank 1-8 on button presses (not releases)
        if (val > 0) { change_bank(dev, cc - 103); }
    } else {
        // output presses
        outlet (2, "/wac.lp/" + dev + "/" + currentBank[dev] + "/press", cc - 104, -1, val ? 1 : 0);
    }
}

//always pass sysex messages to Ableton
function hw_sysex(dev, byte)
{
    outlet (1, dev, byte);
}

//______________________________

//********************ABLETON MIDI HANDLING******************** 
function sw_midi (device, byte)
{
    //Pass MIDI from Ableton when in bank 0
    if (currentBank[device] == 0) { outlet (0, device, byte); }
}
//***********************************************************************

//********************LOCAL LOOPBACK FLAG HANDLER******************** 
function local_loop (flag)
{
    loopback = (flag != 0);
}
//***********************************************************************


//__________INTERNAL FUNCTIONS__________


grid_led.local = 1;
function grid_led (dev, bank, x, y, g, r, f, store, show)
{
    //calculate velocity
    var v =  ((g << 4) & 48) + (r & 3) + (12 - (f << 2));
    
    //no top row LED control when hardware banking enabled
    if ((-1 == y) && hardwareBanking[dev]) { return; }

    //re-index top row for data storage
    if (-1 == y ) { y = 8; }

    // output MIDI to LP if in currentBank and new value is different to currently displayed
    if ((show) 
        && (bank == currentBank[dev])
        && (currentLedDisplay[dev][bank][yxLookup[y][x][1]] != v)
    ) {
        outlet(
            0,
            dev,
            y == 8 ? 176 : 144,
            yxLookup[y][x][0],
            v
        );
        currentLedDisplay[dev][bank][yxLookup[y][x][1]] = v;
    }

    if (store) {
        data[dev][bank][yxLookup[y][x][1]] = v;
    }
}


grid_recall.local = 1;
function grid_recall (dev, bank, x, y)
{
    if (bank != currentBank[dev]) { return; }     
    if (-1 == y) { y = 8; }
    if (currentLedDisplay[dev][bank][yxLookup[y][x][1]] != data[dev][bank][yxLookup[y][x][1]]) {
        outlet(
            0,
            dev,
            y == 8 ? 176 : 144,
            yxLookup[y][x][0],
            data[dev][bank][yxLookup[y][x][1]]
        );
        currentLedDisplay[dev][bank][yxLookup[y][x][1]] = data[dev][bank][yxLookup[y][x][1]];
    }
}


grid_refresh.local =1;
function grid_refresh (dev, bank)
{
    if (currentBank[dev] != bank) { return; }

    //set LP grid mode to xy and enable flashing
    outlet (0, dev, 176, 0, 1, 176, 0, 40);

    // output stored data for new bank (using rapid led update messages)
    for (var i = 0; i < 40; i++) {
        outlet (0, dev, 146, data[dev][bank][2 * i], data[dev][bank][2 * i + 1]);
        currentLedDisplay[dev][bank][2 * i] = data[dev][bank][2 * i];
        currentLedDisplay[dev][bank][2 * i + 1] = data[dev][bank][2 * i + 1];
    }
}

setHardwareBanking.local = 1;
function setHardwareBanking (dev, state)
{
    // make boolean
    state = state != 0;
    if (state == hardwareBanking[dev]) { return; }

    hardwareBanking[dev] = state;
    createBankDisplayLeds (dev);
    outputBankLedDisplay(dev, currentBank[dev]);

    // output change via OSC
    outlet (2, "/wac.lp/" + dev + "/hardwarebank", state ? 1 : 0);
}

createBankDisplayLeds.local = 1;
function createBankDisplayLeds (dev)
{
    for (var j = 1; j <= 8; j++) {
        for (var k = 72; k <= 79; k++) {
            data[dev][j][k] = 12
        }
        // create colours for displaying bank
        if (hardwareBanking[dev]) {
            data[dev][j][77] =  63;
            data[dev][j][78] =  63;
            data[dev][j][71 + j] =  15;
        }
    }
}

outputBankLedDisplay.local = 1;
function outputBankLedDisplay (dev, bank)
{
    if ((bank != currentBank[dev]) || bank == 0) { return; }
    for (var x = 0; x <= 7; x++) {
        grid_recall(dev, bank, x, -1);
    }
}

change_bank.local = 1;
function change_bank (dev, bank)
{
    if ((currentBank[dev] == bank)
        || (bank < 0)
        || (bank > 8)
    ) {
        return;
    }
    if (bank > 0) {
        //set LP grid mode to xy and enable flashing
        outlet (0, dev, 176, 0, 1, 176, 0, 40);

        // emulate pressing "user1" button to Ableton (so last mode is NOT "session")
        // Ableton replies ignored as current bank is not 0)
        outlet (1, dev, 176, 109, 127, 176, 109, 0);

        // output stored data for new bank (using rapid led update messages)
        for (var i = 0; i < 40; i++) {
            outlet (0, dev, 146, data[dev][bank][2 * i], data[dev][bank][2 * i + 1]);
            currentLedDisplay[dev][bank][2 * i] = data[dev][bank][2 * i];
            currentLedDisplay[dev][bank][2 * i + 1] = data[dev][bank][2 * i + 1];
        }
    } else {                    
        //reset Launchpad
        outlet (0, dev, 176, 0, 0);

        //emulate pressing "session" button to Ableton
        outlet (1, dev, 176, 108, 127, 176, 108, 0);
    }
    currentBank[dev] = bank;
    outlet (2, "/wac.lp/" + dev + "/" + bank + "/bank")
}


clear_bank.local =1;
function clear_bank (dev, bank)
{
    //clear storage
    for (var i = 0; i < 80; i++) {
        data[dev][bank][i] = 12;
        currentLedDisplay[dev][bank][i] = 12;
    }
    createBankDisplayLeds (dev);

    if (bank != currentBank[dev]) { return; } 

    //clear message to LP
    outlet (0, dev, 176, 0, 0);

    //set LP grid mode to xy and enable flashing
    outlet (0, dev, 176, 0, 1, 176, 0, 40);
    
    outputBankLedDisplay (dev, bank)
}
//______________________________