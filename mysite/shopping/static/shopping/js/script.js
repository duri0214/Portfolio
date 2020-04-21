let editing;
let tr_prev;
function addRowHandler() {
    const table = edit_table.tBodies[0];
    const rows = table.rows;
    for (i = 0; i < rows.length; i++) {
        table.rows[i].addEventListener('click', e => {

            if (tr_prev && e.target.parentNode == tr_prev) {
                editing.remove();
                tr_prev = undefined;
            } else {

                // delete if exists editing
                if (editing) {
                    editing.remove();
                }

                // it's clicked tr
                const tr = e.target.parentNode;
                tr_prev = tr;

                // new tr
                let tr_new = tr.parentNode.insertBefore(document.createElement('tr'), tr.nextSibling);
                tr_new.classList.add('edit_record');

                // remember new tr
                editing = tr_new;

                // new td
                let td_new;
                td_new = tr_new.appendChild(document.createElement('td'));
                td_new.setAttribute("colspan", "4");
                for (j = 0; j < 4; j++){
                    input_new = td_new.appendChild(document.createElement('input'));
                    input_new.setAttribute("type", "text"); 
                    input_new.setAttribute("name", "edited");
                    input_new.setAttribute("id", "edit" + (j + 1));
                }
                // code is can't edit
                edit1.setAttribute("disabled", "disabled");
                // submit button
                input_new = td_new.appendChild(document.createElement('input'));
                input_new.setAttribute("type", "submit");
                input_new.onclick = () => { doUpdate() };

                // read db data
                fetch(myurl.base + 'edit/0/', {
                    method: 'POST',
                    headers: {
                        "Content-Type": "application/json; charset=utf-8",
                        "X-CSRFToken": Cookies.get('csrftoken')
                    },
                    body: JSON.stringify({"code": tr.cells[0].textContent})
                })
                .then(response => response.json())
                .then(json => {
                    td_new.children[0].value = json.code;
                    td_new.children[1].value = json.name;
                    td_new.children[2].value = json.price;
                    td_new.children[3].value = json.description;
                })        
            }

        }, false)

    }
}

function doUpdate() {

    const edited = document.querySelectorAll(".edit_data .edit_record input[name='edited']");
    
    fetch(myurl.base + 'edit/1/', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json; charset=utf-8",
            "X-CSRFToken": Cookies.get('csrftoken')
        },
        body: JSON.stringify({
            "code": edited[0].value,
            "name": edited[1].value,
            "price": edited[2].value,
            "description": edited[3].value
        })
    })
    .then(response => response.json())
    .then(json => {
        location.href = myurl.base;
    })        
}