// ajax: myurl.edit
function addRowsHandler() {
    const table = edit_table.tBodies[0];
    const rows = table.rows;
    for (i = 0; i < rows.length; i++) {
        table.rows[i].addEventListener('click', e => {
            let retValue = [];
            const tr = e.target.parentNode;
            for (j = 0; j < tr.cells.length; j++) {
                retValue.push(tr.cells[j].textContent)
            }
            console.log(retValue.join(', '));
            let ele = document.createElement('div');
            ele.classList.add('row_detail');
            let div = tr.parentNode.insertBefore(ele, tr.nextSibling); 
            
        }, false)
    }
}