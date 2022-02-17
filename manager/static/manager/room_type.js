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

function hideBedTable() {
    bedTable.style.display = 'none';
}

function showBedTable() {
    bedTable.style.display = 'block';
}

function createRow(bed) {
    var row = bedTable.insertRow(-1);
    row.id = "row"+bed.value;
    row.setAttribute('data-bed-id', bed.value);
    var bedName = row.insertCell(0);
    var bedQty = row.insertCell(1);
    var minus = row.insertCell(2);
    var plus = row.insertCell(3)
    bedName.innerHTML = bed.innerHTML;
    bedQty.innerHTML = 1;
    minus.innerHTML = `<i id="minus${bed.value}" data-bed-id="${bed.value}" class="bi bi-dash-circle bed-minus"></i>`;
    plus.innerHTML = `<i id="plus${bed.value}" data-bed-id="${bed.value}" class="bi bi-plus-circle bed-plus"></i>`;
}

function increaseQty(bedId) {
    console.log(bedId)
    const row = document.querySelector("#row"+bedId);
    var qty = parseInt(row.cells[1].innerHTML);
    row.cells[1].innerHTML = qty + 1; 
}

function decreaseQty(bedId) {
    const row = document.querySelector("#row"+bedId);
    var qty = parseInt(row.cells[1].innerHTML);
    if (qty == 1) {
        row.remove()
    } else {
        row.cells[1].innerHTML = qty - 1; 
    }
    
}

const csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;
const bedList = document.querySelector('#bed-list');
const addBedButton = document.querySelector('#add-bed-button');
const bedTable = document.querySelector('#bed-table');

addBedButton.addEventListener("click", function(event) {
    event.preventDefault();
    var bed = bedList.options[bedList.selectedIndex]
    
    if (bed.value) {
        createRow(bed);
        showBedTable();
        var plusList = document.querySelectorAll(".bed-plus");
        var minusList = document.querySelectorAll(".bed-minus");
        for (let i=0; i<plusList.length; i++) {
            plusList[i].addEventListener("click", function() {
                increaseQty(bed.value)
            });
        }
        for (let i=0; i<minusList.length; i++) {
            minusList[i].addEventListener("click", function() {
                decreaseQty(bed.value)
            });
        }
    };
});

document.body.addEventListener('htmx:configRequest', (event) => {
    event.detail.headers['X-CSRFToken'] = csrf;
  })


// reload table button events after table content loaded by htmx
document.body.addEventListener('htmx:afterSwap', (event) => {
    setMoveButtonsEvents();
    setDeleteButtonsEvents();
  })

setMoveButtonsEvents();
setDeleteButtonsEvents();





