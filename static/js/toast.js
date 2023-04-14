const toastTrigger = document.getElementById('liveToastBtn')
const toastLiveExample = document.getElementById('liveToast')
const toastHeaderDiv = document.querySelector('.toast-header')


if (toastTrigger) {
  const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample)

  toastTrigger.addEventListener('click', () => {
    toastBootstrap.show()
  })
}

const setToast = () => {
    let toastType = errorMsg === 'None' ? 'toast success-toast' : 'toast error-toast'
    let toastHeader = errorMsg === 'None' ? 'toast success-toast-header' : 'toast error-toast-header'
    toastLiveExample.className = toastType
    toastHeaderDiv.className = toastHeader
}