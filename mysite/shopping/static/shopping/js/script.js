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

                // new td *4
                let td_new;
                for (j = 0; j < 4; j++){
                    td_new = tr_new.appendChild(document.createElement('td'));
                    td_new = td_new.appendChild(document.createElement('input'));
                    td_new.setAttribute("type", "text"); 
                }
                tr_new.cells[0].children[0].setAttribute("disabled", "disabled");

                // read db data
                fetch(myurl.base + 'edit/', {
                    method: 'POST',
                    headers: {
                        "Content-Type": "application/json; charset=utf-8",
                        "X-CSRFToken": Cookies.get('csrftoken')
                    },
                    body: JSON.stringify({"code": tr.cells[0].textContent})
                })
                .then(response => response.json())
                .then(json => {
                    tr_new.cells[0].children[0].value = json.code;
                    tr_new.cells[1].children[0].value = json.name;
                    tr_new.cells[2].children[0].value = json.price;
                    tr_new.cells[3].children[0].value = json.description;
                })        
            }

        }, false)

    }
}