let splashScreen = document.querySelector('.splash');
// opacity might need moved inside timeout
splashScreen.style.opacity = 0;
setTimeout(() => {
    splashScreen.clasList.add('hidden')
    }, 610);