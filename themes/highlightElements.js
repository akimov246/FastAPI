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
        top: 0;
        right: 0;
        height: 2.5rem;
        width: 2.5rem;
        border: none;
        cursor: pointer;
        opacity: 0.7;
        border-radius: 0.5rem;
        box-sizing: border-box;
    `;

    button.addEventListener('click', function () {
        (async function() {
            await navigator.clipboard.writeText(button.parentElement.innerText);
        })();
    });

    elem.append(button);

    elem.addEventListener('scroll', function() {
        button.style.left = elem.offsetWidth + elem.scrollLeft - button.offsetWidth + 'px';
    });
}

document.querySelectorAll('pre').forEach((elem) => {
    addCopyButton(elem);
});

document.addEventListener('keydown', function(event) {
    if (event.code === 'Enter' && document.activeElement.tagName !== 'TEXTAREA') {
        let form  = document.activeElement.assignedSlot?.closest('form');
        if (form) {
            form.querySelector('slot[name="buttons"]').assignedElements({flatten: true}).at(0).click();
        }
    }
    if (event.code === 'Tab') {
        if (document.activeElement.tagName === 'TEXTAREA') {
            event.preventDefault();
            const textarea = document.activeElement;
            const start = textarea.selectionStart;
            const end = textarea.selectionEnd;
            textarea.value = textarea.value.substring(0, start) + '\t' + textarea.value.substring(end);
            textarea.selectionStart = textarea.selectionEnd = start + 1;
        }
    }
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
                    gap: 0;
                }
              
                form {
                    display: grid;
                    grid-template-columns: max-content 1fr;
                    border: 0.1rem solid var(--code-background-color);
                    border-radius: 0.5rem;
                    box-sizing: border-box;
                    gap: 0.5rem;
                    padding: 1rem 0.5rem 0.5rem 1rem;
                    width: 100%;
                    align-items: start;
                    height: max-content;
                    transition: width 1s;
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
                ::slotted(textarea:hover),
                ::slotted(input:focus) {
                    outline: none;
                    box-shadow: 0 0 1rem rgba(0, 0, 0, 0.2);
                }
                
                div.response {
                    opacity: 0;
                    width: 0;
                    box-sizing: border-box;
                    transition: width 1s, opacity 1s;
                }
                
                ::slotted(pre) {
                    margin: 0 !important;
                    min-height: 100%;
                }
                
                ::slotted(textarea) {
                    display: block;
                    width: 100%;
                    border: 0.1rem solid var(--code-background-color);
                    border-radius: 0.5rem;
                    padding-left: 0.5rem;
                    font-family: 'Roboto', sans-serif;
                    transition: box-shadow 0.5s;
                    min-height: 15rem;
                    resize: none;
                    margin-top: 0.3rem;
                    font-size: 1.1rem;
                    outline: none;
                    overflow-x: auto;
                    overflow-y: hidden;
                    line-height: 1.5rem;
                    tab-size: 4;
                    letter-spacing: 0.05ch;
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
        let textarea  = inputs.find(element => {
            return element.tagName === 'TEXTAREA'
        });
        
        if (textarea) {
            textarea.style.height = textarea.scrollHeight + 'px';
            textarea.addEventListener('input', function() {
                textarea.style.height = textarea.scrollHeight + 'px';
            });
        }
        
        button.addEventListener('click', function() {
            this.assignedSlot.parentElement.style.width = '50%';
            this.assignedSlot.parentElement.nextElementSibling.style.opacity = '1';
            this.assignedSlot.parentElement.nextElementSibling.style.width = '50%';
            this.assignedSlot.parentElement.getRootNode().host.style.gap = '0.5rem';

            pre.innerHTML = '';
            let url = inputs.at(0).value;
            let method = inputs.at(1).value;
            let data = {};
            for (let input of inputs.slice(2)) {
                if (input.value) {
                    let value = input.value;
                    if (input.tagName === 'TEXTAREA') {
                        data = JSON.parse(value);
                        continue;
                    }
                    if (/^\[.*]$/.test(value)) {
                        value = JSON.parse(value);
                    }
                    if (input.dataset.body) {
                        if (!data[input.dataset.body]) {
                            data[input.dataset.body] = {};
                        }
                        data[input.dataset.body][input.name] = value;
                    } else {
                        data[input.name] = value;
                    }
                }
            }
            let requestInit = {
                    method: method
            }
            if (method.toLowerCase() !== 'get' && Object.keys(data).length) {
                requestInit.headers = {
                        'Content-type': 'application/json'
                }
                requestInit.body = JSON.stringify(data)
            }
            fetch(url, requestInit)
            .then(response => {
                return response.json();
            })
            .then(json => {
                pre.innerHTML = JSON.stringify(json, undefined, 4);
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
