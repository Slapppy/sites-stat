var matrika = document.getElementById("text");
const data = document.currentScript.dataset;
const idCounter = data.idCounter

function innerTextScript(idCounter) {
  matrika.innerText = `
  <noscript><img src="http://127.0.0.1:8000/api/getmetadata/${idCounter}"/></noscript>
    <script src="http://127.0.0.1:8000/api/getmetadata/${idCounter}"></script>`;
};



innerTextScript(idCounter);