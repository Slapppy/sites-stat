export default function generateCounterScript(counterId) {
    console.log('скрипт')
    return `
    &lt;!-- /Auf.Metrika counter --&gt;
                    &lt;script&gt;&lt;img src="${window.location.origin}/api/getmetadata/${counterId}" style="position:absolute; left:-9999px;" alt="" /&gt;&lt;/script&gt;
                    &lt;noscript&gt;&lt;div&gt;&lt;img src="${window.location.origin}/api/getmetadata/${counterId}" style="position:absolute; left:-9999px;" alt="" /&gt;
                    &lt;/div&gt;&lt;/noscript&gt;
  `;
}


export function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}