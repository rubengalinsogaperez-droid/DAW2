// Los digitos estan al reves: las unidades van en la posicion 0.
let NumeroLargoA = [8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9];
let NumeroLargoB = [2];

function sumarNumerosLargos(arrayA, arrayB) {
    //declaro resultado y el acarreo
    let resultado = [];
    let acarreo = 0;

    // Mientras quede digitos en alguno de los dos continuamos con el bucle .
    for (let i = 0; i < arrayA.length || i < arrayB.length; i++) {
        let digitoA = 0;
        let digitoB = 0;

       //si alguno de los se acaba se tomara por 0.
        if (i < arrayA.length) {
            digitoA = arrayA[i];
        }
        if (i < arrayB.length) {
            digitoB = arrayB[i];
        }

        let suma = digitoA + digitoB + acarreo;

        resultado.push(suma % 10);
        if (suma >= 10) {
            acarreo = 1;
                    
        } else {
            acarreo = 0;
        }
        
    }

    // Si queda acarreo, se añade al final.
    if (acarreo > 0) {
        resultado.push(acarreo);
    }

    return resultado;
}

console.log(NumeroLargoA);
console.log(NumeroLargoB);
console.log(" ");
console.log(sumarNumerosLargos(NumeroLargoA, NumeroLargoB));
