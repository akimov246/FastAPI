'use strict';

// const prismStyle = document.createElement('link');
// prismStyle.href = 'https://cdnjs.cloudflare.com/ajax/libs/prism/1.30.0/themes/prism.min.css';
// prismStyle.rel = 'stylesheet';
// document.head.append(prismStyle);
//
// const prismScript = document.createElement('script');
// prismScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/prism/1.30.0/prism.min.js';
// document.head.append(prismScript);
//
// const prismJSONScript = document.createElement('script');
// prismJSONScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/prism/1.30.0/components/prism-json.min.js';
//
// const prismPythonScript = document.createElement('script');
// prismPythonScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/prism/1.30.0/components/prism-python.min.js';
//
// prismScript.addEventListener('load', function () {
//     document.head.append(prismJSONScript);
//     document.head.append(prismPythonScript);
// });
//
// prismPythonScript.addEventListener('load', function () {
//     document.querySelectorAll('code').forEach((elem) => {
//         Prism.highlightElement(elem);
//     });
// });

const prismStyle = document.createElement('link');
prismStyle.href = '../../themes/prism.css';
prismStyle.rel = 'stylesheet';
document.head.append(prismStyle);

const prismScript = document.createElement('script');
prismScript.src = '../../themes/prism.js';
document.head.append(prismScript);


// Шрифт
const fontRoboto = document.createElement('link');
fontRoboto.href = 'https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap';
fontRoboto.rel = 'stylesheet';
document.head.append(fontRoboto);

document.querySelectorAll('pre').forEach((elem) => {
    let button = document.createElement('button');
    button.innerHTML = '<svg style="vertical-align: middle" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19 21H8V7h11m0-2H8a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2m-3-4H4a2 2 0 0 0-2 2v14h2V3h12V1Z"/></svg>';
    button.style.cssText = `
        position: absolute;
        right: 0;
        top: 0;
        height: 2.5rem;
        width: 2.5rem;
        border: none;
        cursor: pointer;
        opacity: 0.7;
        border-radius: 0.5rem;
        transition: filter 0.5s;
    `;

    button.addEventListener('click', function () {
        button.style.filter = 'brightness(0.9)';
        (async function test() {
            await navigator.clipboard.writeText(button.parentElement.innerText);
        })();
        setTimeout(() => button.style.filter = '', 500);
    });

    elem.append(button);

    elem.dispatchEvent(new CustomEvent('buttonAdded'));
});
