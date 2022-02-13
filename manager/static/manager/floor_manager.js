function setMoveButtonsEvents() {
    let floorMoveButtons = document.querySelectorAll(".floor-move");
    for(i=0; i<floorMoveButtons.length; i++) {
        const button = floorMoveButtons[i];
        button.onclick = function() {
            fetch("floor_manager/floor_move", {
                method: "POST",
                body: JSON.stringify({
                    floor_id: parseInt(button.dataset.floor),
                    direction: button.dataset.direction
                }),
                headers: {'X-CSRFToken': csrf}
            }).then(response => {
                if (response.ok) {
                    window.location.reload();
                }
            })
        };
    };
}

function setDeleteButtonsEvents() {
    let floorDeleteButtons = document.querySelectorAll(".floor-delete");
    for(i=0; i<floorDeleteButtons.length; i++) {
        const button = floorDeleteButtons[i];
        const url = "floor_manager/delete/" + button.dataset.floor
        button.onclick = function() {
            fetch(url, {
                method: "POST",
                headers: {'X-CSRFToken': csrf}
            }).then(response => {
                if (response.ok) {
                    window.location.reload();
                }
            })
        };
    };
}

const csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;


document.body.addEventListener('htmx:configRequest', (event) => {
    event.detail.headers['X-CSRFToken'] = csrf;
  })


// reload table button events after table content loaded by htmx
document.body.addEventListener('htmx:afterOnLoad', (event) => {
    console.log('response received')
    setMoveButtonsEvents();
    setDeleteButtonsEvents();
  })

setMoveButtonsEvents();
setDeleteButtonsEvents();





