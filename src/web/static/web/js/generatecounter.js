var matrika = document.getElementById("text");
const data = document.currentScript.dataset;
const idCounter = data.idCounter
// TODO вставлять хост на основе request из Django
// TODO переписать на vue, раз вы его используете
function innerTextScript(idCounter) {
    var domain = window.location.hostname;
    var script = `
  <!-- / counter -->
  <div id="counter_id" style="transform: translateX(9999px);">${idCounter}</div>
  <script src="https://${domain}/src/src/assets/collectdata.js"></script>
  <noscript><div><img src="https://${domain}/api/getmetadata/${idCounter}"/></div></noscript>`;

    matrika.innerText = script;

}
innerTextScript(idCounter);

// Создание кнопки копирования
    var copyButton = document.createElement("button");
    copyButton.id = "copy";
    copyButton.innerText = "Копировать";

// Применение стилей к кнопке
    copyButton.style.position = "absolute";
    copyButton.style.background = "#a7f736";
    copyButton.style.marginTop = "-23.5%";
    copyButton.style.marginLeft = "38%";
    copyButton.style.border = "none";
    copyButton.style.borderRadius = "12px";
    copyButton.style.padding = "8px 16px";
    copyButton.style.fontSize = "14px";
    copyButton.style.cursor = "pointer";

// Добавление обработчика события при клике на кнопку
    copyButton.addEventListener("click", function () {
        var scriptText = matrika.innerText; // Получение текста скрипта
        navigator.clipboard.writeText(scriptText) // Копирование текста в буфер обмена
            .then(function () {
            })
            .catch(function () {
                alert("Не удалось скопировать текст.");
            });
    });

// Добавление кнопки на страницу
    document.body.appendChild(copyButton);
