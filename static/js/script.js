let verificados = document.getElementById('btn_token')
let verificadosCheck = verificados.value

Token = () => {
    if(verificadosCheck == 'on'){
        verificadosCheck = 'off'
        verificados.value = verificadosCheck

    } else {
        verificadosCheck = 'on'
        verificados.value = verificadosCheck
    }
}
