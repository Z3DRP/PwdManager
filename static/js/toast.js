const toast = document.getElementById('toast');
const bugSVG = '<svg id="bug" xmlns="http://www.w3.org/2000/svg" width="36" height="36" fill="red" class="bi bi-bug-fill" viewBox="0 0 16 16"><path d="M4.978.855a.5.5 0 1 0-.956.29l.41 1.352A4.985 4.985 0 0 0 3 6h10a4.985 4.985 0 0 0-1.432-3.503l.41-1.352a.5.5 0 1 0-.956-.29l-.291.956A4.978 4.978 0 0 0 8 1a4.979 4.979 0 0 0-2.731.811l-.29-.956z"/><path d="M13 6v1H8.5v8.975A5 5 0 0 0 13 11h.5a.5.5 0 0 1 .5.5v.5a.5.5 0 1 0 1 0v-.5a1.5 1.5 0 0 0-1.5-1.5H13V9h1.5a.5.5 0 0 0 0-1H13V7h.5A1.5 1.5 0 0 0 15 5.5V5a.5.5 0 0 0-1 0v.5a.5.5 0 0 1-.5.5H13zm-5.5 9.975V7H3V6h-.5a.5.5 0 0 1-.5-.5V5a.5.5 0 0 0-1 0v.5A1.5 1.5 0 0 0 2.5 7H3v1H1.5a.5.5 0 0 0 0 1H3v1h-.5A1.5 1.5 0 0 0 1 11.5v.5a.5.5 0 1 0 1 0v-.5a.5.5 0 0 1 .5-.5H3a5 5 0 0 0 4.5 4.975z"/></svg>';
const checkSVG = '<svg id="check" xmlns="http://www.w3.org/2000/svg" width="36" height="36" fill="currentColor" class="bi bi-check-square-fill" viewBox="0 0 16 16"><path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm10.03 4.97a.75.75 0 0 1 .011 1.05l-3.992 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.75.75 0 0 1 1.08-.022z"/></svg>'
const toastIcon = document.getElementById('toast-icon');
const toastTitle = document.getElementById('toast-title');
const toastMsg = document.getElementById('toast-message');
let toastTimeout;
let svgCheck;
let svgBug;

function showToast(toastData) {
    clearTimeout(toastTimeout);
    setupToast(toastData);
    toast.style.transform = 'translateX(0)';
    toastTimeout = setTimeout(() => {
        toast.style.transform = 'translateX(-400px)';
        svgCheck = undefined;
        svgBug = undefined;
    }, 4000);
}

function closeToast() {
    toast.style.transform = 'translateX(-400px)';
}

const setupToast = (toastData) => {
    if (toastData.wasSuccess === 1)  {
        let green = '#47d764';
        removeExistingIcon()
        setupToastIcon(toastIcon, green, 'success');
        toastIcon.appendChild(svgCheck);
        toast.borderLeftColor = green;
        toastTitle.style.color = green;
        toastTitle.textContent = 'Success';
        toastMsg.textContent = toastData.successMessage;
    } else {
        let red = '#ff0000';
        removeExistingIcon();
        setupToastIcon(toastIcon, red, 'error');
        toastIcon.appendChild(svgBug);
        toast.borderLeftColor = red;
        toastTitle.textContent = 'Error';
        toastTitle.style.color = red;
        toastMsg.textContent = toastData.errorMessage;
    }
}

const setupToastIcon = (node, toastColor, toastType) => {
    switch(toastType) {
        case 'success':
            svgCheck = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
            iconPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
            svgCheck.setAttribute('id', 'success-icon');
            svgCheck.setAttribute('fill', 'none');
            svgCheck.setAttribute('viewBox', '0 0 16 16');
            svgCheck.setAttribute('width', 36);
            svgCheck.setAttribute('length', 36);
            svgCheck.classList.add('bi');
            svgCheck.classList.add('bi-check-square-fill')
            iconPath.setAttribute(
            'd',
            'M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm10.03 4.97a.75.75 0 0 1 .011 1.05l-3.992 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.75.75 0 0 1 1.08-.022z'
            );
            iconPath.setAttribute('stroke-linecap', 'round');
            iconPath.setAttribute('stroke-linejoin', 'round');
            iconPath.setAttribute('stroke-width', '2');
            svgCheck.appendChild(iconPath);
            svgCheck.style.color = toastColor;
            break;
        case 'error':
            svgBug = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
            iconPath1 = document.createElementNS('http://www.w3.org/2000/svg', 'path');
            iconPath2 = document.createElementNS('http://www.w3.org/2000/svg', 'path');
            svgBug.setAttribute('id', 'error-icon');
            svgBug.setAttribute('fill', 'none');
            svgBug.setAttribute('viewBox', '0 0 16 16');
            svgBug.setAttribute('width', 36);
            svgBug.setAttribute('length', 36);
            svgBug.classList.add('bi');
            svgBug.classList.add('bi-bug-fill')
            iconPath1.setAttribute(
            'd',
            'M4.978.855a.5.5 0 1 0-.956.29l.41 1.352A4.985 4.985 0 0 0 3 6h10a4.985 4.985 0 0 0-1.432-3.503l.41-1.352a.5.5 0 1 0-.956-.29l-.291.956A4.978 4.978 0 0 0 8 1a4.979 4.979 0 0 0-2.731.811l-.29-.956z'
            );
            iconPath2.setAttribute(
            'd',
            'M13 6v1H8.5v8.975A5 5 0 0 0 13 11h.5a.5.5 0 0 1 .5.5v.5a.5.5 0 1 0 1 0v-.5a1.5 1.5 0 0 0-1.5-1.5H13V9h1.5a.5.5 0 0 0 0-1H13V7h.5A1.5 1.5 0 0 0 15 5.5V5a.5.5 0 0 0-1 0v.5a.5.5 0 0 1-.5.5H13zm-5.5 9.975V7H3V6h-.5a.5.5 0 0 1-.5-.5V5a.5.5 0 0 0-1 0v.5A1.5 1.5 0 0 0 2.5 7H3v1H1.5a.5.5 0 0 0 0 1H3v1h-.5A1.5 1.5 0 0 0 1 11.5v.5a.5.5 0 1 0 1 0v-.5a.5.5 0 0 1 .5-.5H3a5 5 0 0 0 4.5 4.975z'
            );
            iconPath1.setAttribute('stroke-linecap', 'round');
            iconPath1.setAttribute('stroke-linejoin', 'round');
            iconPath1.setAttribute('stroke-width', '2');
            iconPath2.setAttribute('stroke-linecap', 'round');
            iconPath2.setAttribute('stroke-linejoin', 'round');
            iconPath2.setAttribute('stroke-width', '2');

            iconPath1.appendChild(iconPath2);
            svgBug.appendChild(iconPath1);
            svgBug.style.color = toastColor;
            break;
    }
    if (svgCheck !== undefined) {
        return node.appendChild(svgCheck);
    } else {
        return node.appendChild(svgBug);
    }
}

const removeExistingIcon = () => {
    let prevSuccess = document.getElementById('success-icon');
    let prevError = document.getElementById('error-icon');
    if (prevSuccess) {
        toastIcon.removeChild(prevSuccess);
    }
    if (prevError) {
        toastIcon.removeChild(prevError);
    }
}

function main(toastData) {
    if (toastData !== undefined) {
        showToast(toastData);
    }
}

main();