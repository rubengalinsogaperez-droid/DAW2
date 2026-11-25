let NumeroLargoA = [8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9];
let NumeroLargoB = [2];

function sumarNumerosLargos(arrayA,arrayB){
    let acarreo = 0
    let resultado = [];
    //si en alguno de los dos siguen habiendo numeros se continua con las iteraciones
    for (let i = 0; i < arrayA.length || i < arrayB.length; i++){
        
        let digitoA=0
        let digitoB=0
        //a cada iteracion sobrescribimos encaso de que exista el numero
        if (i < arrayA.length){
            digitoA = arrayA[i];
        }
        if (i < arrayB.length){
            digitoB = arrayB[i]
        }

        let suma = digitoA + digitoB + acarreo;
        resultado.push(suma % 10)
        //maximo puedo acarrear 19
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
