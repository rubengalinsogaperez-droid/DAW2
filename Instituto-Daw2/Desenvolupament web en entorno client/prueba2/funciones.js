// 'use strict'

// function prueba(nombre){
//     console.log(`estoy vivo y m llamo ${nombre}`);
// }
// prueba("pepe");
// prueba("tu_madre");
// prueba("luisa");


// crearfuncion
// PRUEBA IDENTIFICADOR DE FUNCION

// esto es una funcion anonima no tiene nombre 

// Se puede hacer una funcion recursiva

//funcion nombre valor por defecto 

// /**
//  * @param {number} numero de veces
//  * @return {undefined} no devuelve nada
//  * */
 

// function prueba(valor=10){
//     if(!valor){
//         return
//     } 
//     console.log("Hola, desde funcion prueba, VALOR VALE: "+valor);
//     // Sin el return seria undefined
//     prueba(valor--)
// }
// let a=prueba;

// //primero pasa el valor y luego decremento valor post decremento valor-- pre decremento --valor
// // a es igual a prueba literalmente

// console.log(a);

// esto si que tira el resultado de la variable

// a();

// // lo normal es usar const

// prueba()


// //funcion fecha


// let suma(a b){
//     let resultado;
//     resultado = a + b;
//     return resultado;

// }

// console.log(suma(7,4));

// let suma2 = (a ,b) => a + b;


// let mayorque = (a, b) =>{
//     let resultado;
//     if (a > b)
//         return console.log("a es mayor que b");
//     if (b > a)
//         return console.log("b es mayor que a");

// }

//let comarar = (a, b) => a > b ? `${a} > ${b}` :b > a ? `${a} < ${b}` : `${a} = ${b}`; 

// function suma(a, b){
//     let resultado;
//     resultado = a + b;
//     return resultado;
// }


// console.log(suma(7,4));

// let doblar = a => a + a;

//valor valor funcion
// function operar(j ,k, f){
//     if (k != null){
//         return f(j,k);
//     }
//     else{
//         return "No hay valor";  
//     }
// }

// console.log(operar(7,4,suma));

// function devolver(){
//     return function ejecutar(){
//         console.log("Hola, soy una funcion que devuelve otra funcion");
//     }
//     return ejecutar;
// }
// let ni_idea = devolver();

// console.log(ni_idea);

// function factorial(n){
//     if(n<0) return;
    
//     if (n){
//         return n*factorial(n-1);
//     }
//     else return 1;
// }

// console.log(factorial(10));

// console.log(parseInt("101011", 2));
// console.log(Number.isSafeInteger(10));


//ejercicio 1 PREPARACIONEXAMEN

// let importe = prompt("Dime el importe a pagar");
// let entregado = prompt("Dime el dinero entregado");

// importecent = importe + "00";
// entregadocent = entregado + "00";
// importecent = parseInt(importecent.trim());
// entregadocent = parseInt(entregadocent.trim());
// console.log(cobrar(importecent, entregadocent));

// function cobrar(importe, entregado){
//     let importemaximo = 20;
//     if (importe > entregado) {
//         return "No hay dinero suficiente te quedan por pagarme " + (importe - entregado) + " centimos";
//     }
//     if (importe == entregado) {
//             return "Pago exacto no hay cambio";
//     }
//     if (importe < entregado) {
//         let devolverbillete10 = 0;
//         let devolverbillete5 = 0;
//         let devolvermoneda200 = 0;
//         let devolvermoneda100 = 0;
//         let devolervermoneda50 = 0;
//         let devolvermoneda20 = 0;
//         let devolvermoneda10 = 0;
//         let devolveremoneda5 = 0;
//         let devolvermoneda2 = 0;
//         let devolvermoneda1 = 0;

//         let billete10 = 1000;
//         let billete5 = 500;
//         let moneda200 = 200;
//         let moneda100 = 100;
//         let moneda50 = 50;
//         let moneda20 = 20;
//         let moneda10 = 10;
//         let moneda5 = 5;
//         let moneda2 = 2;
//         let moneda1 = 1;
//         if (entregado - billete10 >= importe) {
//             while (entregado >= billete10 && entregado - billete10 >= importe) {
//                 entregado -= billete10;
//                 devolverbillete10 +=1;
//             }
//         }
//         if (entregado - billete5 >= importe) {
//             while (entregado >= billete5 && entregado - billete5 >= importe) {
//                 entregado -= billete5;
//                 devolverbillete5 +=1;
//             }
//         }
//         if (entregado - moneda200 >= importe) {
//             while (entregado >= moneda200 && entregado - moneda200 >= importe) {
//                 entregado -= moneda200;
//                 devolvermoneda200 +=1;
//             }  
//         }
//         if (entregado - moneda100 >= importe) {
//             while (entregado >= moneda100 && entregado - moneda100 >= importe) {
//                 entregado -= moneda100;
//                 devolvermoneda100 +=1;
//             }
//         }
//         if (entregado - moneda50 >= importe) {
//             while (entregado >= moneda50 && entregado - moneda50 >= importe) {
//                 entregado -= moneda50;
//                 devolervermoneda50 +=1;
//             }
//         }
//         if (entregado - moneda20 >= importe) {
//             while (entregado >= moneda20 && entregado - moneda20 >= importe) {
//                 entregado -= moneda20;
//                 devolvermoneda20 +=1;
//             }
//         }
//         if (entregado - moneda10 >= importe) {
//             while (entregado >= moneda10 && entregado - moneda10 >= importe) {
//                 entregado -= moneda10;
//                 devolvermoneda10 +=1;
//             }
//         }
//         if (entregado - moneda5 >= importe) {
//             while (entregado >= moneda5 && entregado - moneda5 >= importe) {
//                 entregado -= moneda5;
//                 devolveremoneda5 +=1;
//             }
//         }
//         if (entregado - moneda2 >= importe) {
//             while (entregado >= moneda2 && entregado - moneda2 >= importe) {
//                 entregado -= moneda2;
//                 devolvermoneda2 +=1;
//             }
//         }
//         if (entregado - moneda1 >= importe) {
//             while (entregado >= moneda1 && entregado - moneda1 >= importe) {
//                 entregado -= moneda1;
//                 devolvermoneda1 +=1;
//             }
//         }
        
//         return "Te devuelvo " + (entregado - importe) + " centimos, en billetes y monedas: \n" + devolverbillete10 + " billetes de 10€, \n" + devolverbillete5 + " billetes de 5€,\n" + devolvermoneda200 + " monedas de 2€,\n" + devolvermoneda100 + " monedas de 1€,\n" + devolervermoneda50 + " monedas de 50 centimos,\n" + devolvermoneda20 + " monedas de 20 centimos,\n" + devolvermoneda10 + " monedas de 10 centimos,\n" + devolveremoneda5 + " monedas de 5 centimos,\n" + devolvermoneda2 + " monedas de 2 centimos, y\n" + devolvermoneda1 + " monedas de 1 centimo";
//     }
// }


// function evaluarIntervalo(inicio, fin, criterio) {
//     let resultado = [];
//     for (let i = inicio; i <= fin; i++) {
//         if (criterio(i)) {
//             resultado.push(i);
//         }
//     }
//     return resultado;
// }

// function criterioPar(numero) {
//     return numero % 2 === 0;
// }
// function criterioImpar(numero) {
//     return numero % 2 !== 0;
// }

// console.log(evaluarIntervalo(1, 10, criterioPar)); // Devuelve [2, 4, 6, 8, 10]
// console.log(evaluarIntervalo(1, 10, criterioImpar)); // Devuelve [1, 3, 5, 7, 9]