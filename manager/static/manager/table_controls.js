function setMoveButtonsEvents() {
    let objectMoveButtons = document.querySelectorAll(".object-move");
    for(i=0; i<objectMoveButtons.length; i++) {
        const button = objectMoveButtons[i];
        button.onclick = function() {
            fetch(button.dataset.target, {
                method: "POST",
                body: JSON.stringify({
                    object: button.dataset.object,
                    object_id: parseInt(button.dataset.id),
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

const csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;


document.body.addEventListener('htmx:configRequest', (event) => {
    event.detail.headers['X-CSRFToken'] = csrf;
  });


// reload table button events after table content loaded by htmx
document.body.addEventListener('htmx:afterSwap', (event) => {
    setMoveButtonsEvents();
  });

setMoveButtonsEvents();
