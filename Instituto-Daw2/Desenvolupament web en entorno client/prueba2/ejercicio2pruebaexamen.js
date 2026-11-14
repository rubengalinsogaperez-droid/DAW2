function evaluarIntervalo(inicio, fin, criterio) {
    let resultado = [];
    for (let i = inicio; i <= fin; i++) {
        if (criterio(i)) {
            resultado.push(i);
        }
    }
    return resultado;
}

function criterioPar(numero) {
    return numero % 2 === 0;
}
function criterioImpar(numero) {
    return numero % 2 !== 0;
}

console.log(evaluarIntervalo(1, 10, criterioPar)); // Devuelve [2, 4, 6, 8, 10]
console.log(evaluarIntervalo(1, 10, criterioImpar)); // Devuelve [1, 3, 5, 7, 9]