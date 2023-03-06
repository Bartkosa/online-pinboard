var intervalId = setInterval(function () {
    var taskDivs = document.getElementsByClassName("taskdiv");

    if (taskDivs.length > 0) {
        for (var i = 0; i < taskDivs.length; i++) {
            dragElement(taskDivs[i]);

        }
        clearInterval(intervalId);
    }
}, 150);

function dragElement(elmnt) {
    elmnt.onmousedown = dragMouseDown;

    function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();

        elmnt.style.position = "absolute";
        document.onmouseup = closeDragElement;
        // call a function whenever the cursor moves:
        document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();

        elmnt.style.top = (e.clientY - 30) + "px";
        elmnt.style.left = (e.clientX - 30) + "px";

    }

    function closeDragElement() {
        // stop moving when mouse button is released:
        document.onmouseup = null;
        document.onmousemove = null;
    }
}