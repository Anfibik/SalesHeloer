
//Скрипты модального окна
function openModal() {
    document.getElementById('myModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('myModal').style.display = 'none';
}


function convertInput() {
    const inputValue = document.getElementById('input-field').value;
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/convert_num', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            const outputValue = JSON.parse(xhr.responseText).result;
            document.getElementById('output-field').textContent = outputValue;
        }
    };
    xhr.send(JSON.stringify({ input: inputValue }));
}
//Конец скриптов модального окна




