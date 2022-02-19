function hideBedTable() {
    bedTable.style.display = 'none';
}

function showBedTable() {
    bedTable.style.display = 'block';
}

function createRow(bed) {
    var row = bedTable.insertRow(-1);
    row.id = "row"+bed.value;
    row.setAttribute("class", "data-rows");
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
    const row = document.querySelector("#row"+bedId);
    var qty = parseInt(row.cells[1].innerHTML);
    row.cells[1].innerHTML = qty + 1; 
}

function decreaseQty(bedId) {
    const row = document.querySelector("#row"+bedId);
    var qty = parseInt(row.cells[1].innerHTML);
    if (qty == 1) {
        row.remove();
        let rows = document.querySelectorAll(".data-rows");
        if(rows.length === 0) {
            hideBedTable()
        };
    } else {
        row.cells[1].innerHTML = qty - 1; 
    }
}

function showCreateBedForm(){
    createBedForm.style.display = 'block'
}

function hideCreateBedForm(){
    createBedForm.style.display = 'none'
}

const csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;
const bedList = document.querySelector('#bed-list');
const addBedButton = document.querySelector('#add-bed-button');
const createNewBedButton = document.querySelector('#create-new-bed-btn');
const createBedButton = document.querySelector('#create-bed-btn');
const cancelBedButton = document.querySelector('#cancel-bed-btn');
const bedTable = document.querySelector('#bed-table');
const createForm = document.querySelector("#create-form");
const bedInfo = document.querySelector("#bed-info");
const createBedForm = document.querySelector('#create-bed-form');
const plusButtons = document.querySelectorAll('.bed-plus');
const minusButtons = document.querySelectorAll('.bed-minus');

addBedButton.addEventListener("click", function(event) {
    event.preventDefault();
    var bed = bedList.options[bedList.selectedIndex]
    if(document.querySelector(`#row${bed.value}`)) {
        increaseQty(bed.value)
    }
    else if (bed.value) {
        createRow(bed);
        showBedTable();
        let plus = document.querySelector(`#plus${bed.value}`);
        let minus = document.querySelector(`#minus${bed.value}`);
        plus.addEventListener("click", function() {
            increaseQty(bed.value)
        });
        minus.addEventListener("click", function() {
            decreaseQty(bed.value)
        });
    };
});

createForm.addEventListener("submit", function() {
    console.log("in submit event function")
    let rows = document.querySelectorAll(".data-rows");
    if(rows.length === 0) {
        alert("Please add beds.");
        return false;
    }
    // Room bed data
    var data = {}
    rows.forEach(function(row){
        let bedId = row.dataset.bedId;
        let bedQty = row.children[1].innerHTML;
        data[`${bedId}`] = bedQty;
        
    });
    // Set value for hidden input element.
    bedInfo.setAttribute('value', JSON.stringify(data));
    return true
});

createNewBedButton.addEventListener('click', function(event) {
    event.preventDefault();
    showCreateBedForm();
});

cancelBedButton.addEventListener('click', function(event) {
    event.preventDefault();
    hideCreateBedForm();
})

createBedButton.addEventListener('htmx:configRequest', (event) => {
    event.detail.headers['X-CSRFToken'] = csrf;
})

createBedButton.addEventListener('htmx:afterOnLoad', (event) => {
    hideCreateBedForm();
})

plusButtons.forEach(plusButton => {
    plusButton.addEventListener('click', function() {
        increaseQty(plusButton.dataset.bedId);
    });
})

minusButtons.forEach(minusButton => {
    minusButton.addEventListener('click', function() {
        decreaseQty(minusButton.dataset.bedId);
    });
})