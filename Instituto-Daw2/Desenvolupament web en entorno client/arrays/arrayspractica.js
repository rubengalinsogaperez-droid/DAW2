
// LISTA SENCILLA V

// let listanormal = ["7", "2", "5", "2", "0", "3", "10"]

// function comparar(a,b){
//     return Number(a) > Number(b);
// }


// function ordenar(lista, algoritmo){
//     for (let i = 0; i < lista.length; i ++){
//         let pivote = lista[0];
//         for (let j = 1; j < lista.length; j ++){
//             if (comparar(lista[j - 1], lista[j])){
//                 lista[j - 1] = lista[j];
//                 lista[j] = pivote;
//             }
//             else{
//                 pivote = lista[j];
//             }

//         }
//     }
//     return lista;
// }


// console.log(ordenar(listanormal, comparar));




// let listacomplicada = [
//   ["Adrián", 47, "Profesor"],
//   ["Luisa", 60, "Profesor"],
//   ["Ana", 20, "Estudiante"],
//   ["Blas", 36, "Estudiante"],
//   ["Agustín", 50, "Profesor"],
//   ["Felipe", 25, "Estudiante"],
//   ["Pedro", 19, "Estudiante"],
//   ["Zoraida", 36, "Estudiante"],
//   ["Juan", 36, "Administrativo"],
//   ["Toñi", 48, "Administrativo"],
//   ["Juan", 16, "Estudiante"],
//   ["Miriam", 15, "Estudiante"],
//   ["Rosa", 75, "Estudiante"],
//   ["Pepe", 31, "Estudiante"],
//   ["Fermín", 64, "Estudiante"],
//   ["Jose", 47, "Profesor"]
// ];


// function obtenerNumeroDeRol(rol){
//     if (rol === "Profesor"){
//         return 1;
//     }
//     if (rol === "Administrativo"){
//         return 2;
//     }
//     if (rol === "Estudiante"){
//         return 3;
//     }
// }
// function estanAlReves(personaA, personaB) {
//     let nombreA = personaA[0];
//     let edadA = personaA[1];
//     let rolA = obtenerNumeroDeRol(personaA[2]);

//     let nombreB = personaB[0];
//     let edadB = personaB[1];
//     let rolB = obtenerNumeroDeRol(personaB[2]);



//     if (rolA !== rolB){
//         return rolA > rolB;
//     }

//     if (edadA !== edadB){
//         return edadA > edadB;
//     }
    
//     return nombreA.localeCompare(nombreB) > 0;
    
// }


// function ordenar(lista, criterio){
//     for (let i = 0; i < lista.length; i ++){
//         let pivote = lista[0];
//         for (let j = 1 ; j < lista.length; j ++){
//             if (criterio(pivote, lista[j])){
//                 lista[j - 1] = lista[j]
//                 lista[j] = pivote
                
//             }
//             else{
//                 pivote = lista[j];
//             }
//         }
//     }
//     return lista;
// }


// console.log (ordenar(listacomplicada, estanAlReves));

// Crea una función cobrar(importe, entregado) que reciba un importe a cobrar de hasta 20 € y la cantidad de dinero entregada por el cliente. Debe calcular el cambio y mostrar cómo devolverlo utilizando primero los billetes y monedas de mayor valor.

// La máquina dispone de una cantidad suficiente de billetes de 10 € y 5 €, y de monedas de 2 €, 1 €, 50, 20, 10, 5, 2 y 1 céntimo. No utiliza billetes superiores a 10 € para devolver el cambio.

// Requisitos
// Los dos argumentos se expresan en céntimos enteros: por ejemplo, 635 representa 6,35 € y 2000 representa 20 €. Trabaja con esas cantidades enteras durante todo el cálculo.
// El importe a cobrar debe estar entre 1 y 2000 céntimos, incluidos ambos extremos.
// La cantidad entregada debe ser un número entero de céntimos igual o superior al importe a cobrar. El límite de 20 € se aplica al importe a cobrar, no a la cantidad entregada.
// Si algún argumento no cumple estas condiciones, lanza un error.
// Calcula y muestra el cambio total en céntimos.
// Muestra cuántos billetes o monedas utiliza de cada valor, omitiendo las denominaciones que no necesita.
// Devuelve el número total de billetes y monedas utilizados para dar el cambio.
// Si el pago es exacto, muestra "Pago exacto. No hay cambio", no muestres ningún desglose y devuelve 0.
// No utilices arrays.



// let listanormal = ["7", "2", "5", "2", "0", "3", "10"]


// function espar(numero) {
//     return numero % 2 === 0;
// }


// function listar(lista, par){
//     for (let i = 0; i < lista.length; i ++){
//         if (par(lista[i])){
//             console.log((lista[i]) + "es par")
//         }
//         else {
//             console.log((lista[i]) + "es impar")
//         }
//     }
// }




// console.log(listar(listanormal, espar));







// function comprobar(numero, criterio){
//     if (criterio(numero)){
        
//         console.log("Franco no hizo nada malo");
//     }
//     else{
        
//     }

// }






// console.log(comprobar(4, espar));




function crearControlAforo(capacidad) {

    // Comprobamos que la capacidad sea un entero positivo
    if (!Number.isInteger(capacidad) || capacidad <= 0) {
        throw new Error("La capacidad debe ser un número entero positivo");
    }

    // Variable que guarda la ocupación
    let ocupacion = 0;

    // Devolvemos una función que recuerda ocupacion y capacidad
    return function (movimiento) {

        // Si no recibe argumento, devuelve la ocupación
        if (movimiento === undefined) {
            return ocupacion;
        }

        // Comprobamos que el argumento sea válido
        if (movimiento !== 1 && movimiento !== -1) {
            throw new Error("Movimiento no válido");
        }

        // Intentar entrar
        if (movimiento === 1) {

            if (ocupacion >= capacidad) {
                console.log("Aforo completo");
                return ocupacion;
            }

            ocupacion++;
        }

        // Intentar salir
        if (movimiento === -1) {

            if (ocupacion <= 0) {
                console.log("No queda nadie dentro");
                return ocupacion;
            }

            ocupacion--;
        }

        console.log("Ocupación: " + ocupacion);

        return ocupacion;
    };
}


// Ejemplo de uso
const puerta = crearControlAforo(2);

console.log(puerta()); // 0

puerta(+1); // Ocupación: 1
puerta(+1); // Ocupación: 2
puerta(+1); // Aforo completo

console.log(puerta()); // 2

puerta(-1); // Ocupación: 1
puerta(-1); // Ocupación: 0
puerta(-1); // No queda nadie dentro

console.log(puerta()); // 0
