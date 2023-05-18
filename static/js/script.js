//Открытие и закрытие модального окна
function openModal() {
    var modal = document.getElementById("myModal");
    modal.style.display = "block";
}

function closeModal() {
    var modal = document.getElementById("myModal");
    modal.style.display = "none";
}

function openModalCalc() {
    var modal = document.getElementById("myModalCalc");
    modal.style.display = "block";
}

function closeModalCalc() {
    var modal = document.getElementById("myModalCalc");
    modal.style.display = "none";
}


// Функция для конвертации цифры в словесное представление
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


// Функционал изменения адреса на выбранный продукт
document.getElementById("apply-setting-button").addEventListener("click", function () {
    var product = document.getElementById("product").value;
    var form = document.getElementById("form-setting");
    var action = form.getAttribute("action");
    form.setAttribute("action", action + product);
});

