const form = document.querySelector('#create-form');
const userField = document.querySelector('#user-field');
const hotelInput = document.querySelector('#hotel-id');
const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
const formType = document.querySelector('#form-type');
console.log(formType.value)

if (formType.value == 'update') {
    console.log('update');
    userField.setAttribute('readonly', true);
};
if (form) {
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
                Swal.fire({  
                    title: 'Employee with this username already exists. \nDo you want to proceed?',  
                    showCancelButton: true,  
                    confirmButtonText: `Submit`,  
                  }).then((result) => {  
                      if (result.isConfirmed) {    
                        form.submit();  
                      } else if (result.isDenied) {    
                          return false
                       }
                  });
            };
        });
    })
}
