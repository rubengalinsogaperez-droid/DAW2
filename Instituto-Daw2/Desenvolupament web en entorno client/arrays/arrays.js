// let a= new Array(12);

// a[20] = "Hello";

// console.log(a.length);

// console.log(a[20]);

// // length se usa tambien para coratar listas
// //un array es una lista solo que a la lista si que se le puede cambiar el tamañano

// let o={
//     nombre:"Roberto",
//     edad:"mucha",
//     modulos:["Economia", "Ciencias"]

// }

// let a = ["1", "2", "3", "4"];
// let b = a.length; // b es 4
// let c = []
// for (let i = 0; i < b; i++) {
//     c[i]= a.length-i
// };
// console.log(c);

// .unshift mete cosas al su contraparte es push que lo mete al final shof y pop borran :) Animooo9 ruben lockea >:o

//.splice te devuelve lo que ha borrado 
//.splice(2,1,"f")  de la posicion dos 
//invertir elementos .reverse()

// let a = ["a", "b", "c", "d", "e", "f"];

// console.log(a);

// a.sort();
// //si a sort ordena por alfabetico, no nos vale para ordenar numeros
// console.log(a);

// let b = [4, 7, 1, 0, 10 , 500, 5, 91];

// console.log(b);
// b.sort((a,b) => a - b);
// //si quiero ordenar de mayor a menor tengo que poner "b - a" en vez de a - b
// console.log(b);

// let numeros=[
//     [1,4,7],
//     [5,0,-3],
//     [50,-47,8],
//     [31,0,0,1,1,-20]
// ]

// for (let i = 0; i < numeros.length ; i++) {
//     console.log("Hola maricon " + i);
// }



// let numeros=[
//     [1,4,7],
//     [5,0,-3],
//     [50,-47,8],
//     [31,0,0,1,1,-20]
// ];



// numeros.sort((a,b) => { //sort por dentro hace un bucle
//     let sumaA = 0, sumaB = 0;

//     for (let x of a) {
//         sumaA += x;
//     }

//     for (let x of b) {
//         sumaA += x;
//     }

//     return sumaB - sumaA;
// })

// console.log(numeros)


//ordenacion burbuja

// let numeros = [5, 2, 8, 1, 3];

// // Bucle externo: controla cuántas pasadas hacemos
// for (let i = 0; i < numeros.length; i++) {
    
//     // Bucle interno: compara elementos de dos en dos
//     for (let j = 0; j < numeros.length - 1; j++) {
        
//         // Si el número actual es mayor que el que tiene a la derecha...
//         if (numeros[j] > numeros[j + 1]) {
            
//             // ...los intercambiamos usando una variable auxiliar (aux)
//             let aux = numeros[j];
//             numeros[j] = numeros[j + 1];
//             numeros[j + 1] = aux;
            
//         }
//     }
// }

// console.log(numeros); // Resultado: [1, 2, 3, 5, 8]


let numeros1 = [1,2,3,3,5,1,2,3,32,2,1];

for (let i = 0; i < numeros1.length ; i++) {
    for(let j = 0; j < numeros1.length ; j++) {

        if (numeros1[j] > numeros1[j+1]) {

            let varauxiliar = numeros1[j];
            numeros1[j] = numeros1[+1];
            numeros1[j+1] = varauxiliar;
        }
    }
}
console.log(numeros1);