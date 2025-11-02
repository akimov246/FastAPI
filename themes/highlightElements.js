'use strict';

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

function addCopyButton(elem) {
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
    `;

    button.addEventListener('click', function () {
        (async function() {
            await navigator.clipboard.writeText(button.parentElement.innerText);
        })();
    });

    elem.append(button);
}

document.querySelectorAll('pre').forEach((elem) => {
    addCopyButton(elem);
});

customElements.define('request-response-container', class extends HTMLElement {
    connectedCallback() {
        this.attachShadow({mode: 'open'})
        this.shadowRoot.innerHTML = `
            <style>
                :host {
                    display: flex;
                    border: 0.1rem solid var(--code-background-color);
                    border-radius: 0.5rem;
                    padding: 0.5rem;
                    gap: 0.5rem;
                }
              
                form {
                    display: grid;
                    grid-template-columns: max-content 1fr;
                    border: 0.1rem solid var(--code-background-color);
                    border-radius: 0.5rem;
                    box-sizing: border-box;
                    gap: 0.5rem;
                    padding: 1rem 1rem 0.5rem 1rem;
                    width: 50%;
                    align-items: start;
                    height: max-content;
                }
                
                ::slotted(*) {
                    box-sizing: border-box;
                }
                
                form div.labels {
                    max-height: max-content;
                }
                
                ::slotted(input),
                ::slotted(label) {
                    display: block;
                    margin-top: 0.3rem;
                    height: 1.5rem;
                }
                
                ::slotted(input) {
                    width: 100%;
                    border: 0.1rem solid var(--code-background-color);
                    border-radius: 0.5rem;
                    padding-left: 0.5rem;
                    font-family: 'Roboto', sans-serif;
                    transition: box-shadow 0.5s;
                }
                
                ::slotted(button) {
                    grid-column: span 2;
                    border: 0.1rem solid var(--code-background-color);
                    border-radius: 0.5rem;
                    cursor: pointer;
                    height: 2rem;
                    transition: box-shadow 0.5s;
                }
                
                ::slotted(button:hover),
                ::slotted(input:hover),
                ::slotted(input:focus) {
                    outline: none;
                    box-shadow: 0 0 1rem rgba(0, 0, 0, 0.2);
                }
                
                div.response {
                    width: 50%;
                    box-sizing: border-box;
                }
                
                ::slotted(pre) {
                    margin: 0 !important;
                    min-height: 100%;
                }
            </style>
            
            <form>
                <div class="labels">
                    <slot name="labels"></slot>
                </div>
                <div class="inputs">
                    <slot name="inputs"></slot>
                </div>
                <slot name="buttons"></slot>
            </form>
            <div class="response">
                <slot name="response"></slot>
            </div>
        `
        
        let button = this.shadowRoot.querySelector('slot[name="buttons"]').assignedElements({flatten: true}).at(0);
        let inputs = this.shadowRoot.querySelector('slot[name="inputs"]').assignedElements({flatten: true});
        let pre = this.shadowRoot.querySelector('slot[name="response"]').assignedElements({flatten: true}).at(0);
        button.addEventListener('click', function() {
            pre.innerHTML = '';
            let url = inputs.at(0).value;
            let method = inputs.at(1).value;
            let formData = new FormData();
            for (let input of inputs) {
                if (input.name.toLowerCase() === 'url' || input.name.toLowerCase() === 'method') {
                    continue;
                }
                if (input.value) {
                    formData.append(input.name, input.value);
                }
            }
            let data = Object.fromEntries(formData);
            let requestInit = {
                    method: method,
                    headers: {
                        'Content-type': 'application/json'
                    }
            }
            if (method.toLowerCase() !== 'get') {
                requestInit.body = JSON.stringify(data)
            }
            fetch(url, requestInit)
            .then(response => {
                return response.json();
            })
            .then(json => {
                pre.innerHTML = JSON.stringify(json, undefined, 2);
                Prism.highlightElement(pre);
                addCopyButton(pre);
            })
            .catch(reason => {
                pre.innerHTML = reason;
                addCopyButton(pre);
            });
        });
    }
});
