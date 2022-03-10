const form = document.querySelector('#create-form');
const userField = document.querySelector('#user-field');
const hotelInput = document.querySelector('#hotel-id');
const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
form.addEventListener('submit', (event) => {
    event.preventDefault();
    fetch("employee_manager/check_user", {
        method: "POST",
        body: JSON.stringify({
            user: userField.value,
        }),
        headers: {'X-CSRFToken': csrfToken}
    }).then(response => {
        console.log(response);
        if (response.ok) {
            form.submit();
        } else {
            if (confirm("Employee with this username already exists, \nDo you want to proceed?") == true) {
                form.submit();
            } else {return false}
        };
    });
})

// form.addEventListener('submit', myFunc);
// function myFunc(event) {
//     event.preventDefault();
//     console.log(event);
//     return false
// }