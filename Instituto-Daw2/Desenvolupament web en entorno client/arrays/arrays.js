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

// let a = ["1", "2", "3", "3"];
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


// let numeros1 = [1,2,3,3,5,1,2,3,32,2,1];

// for (let i = 0; i < numeros1.length ; i++) {
//     for(let j = 0; j < numeros1.length ; j++) {

//         if (numeros1[j] > numeros1[j+1]) {

//             let varauxiliar = numeros1[j];
//             numeros1[j] = numeros1[+1];
//             numeros1[j+1] = varauxiliar;
//         }
//     }
// }
// console.log(numeros1);

//diferencia entre sort y ordenare

// let b = [1, 4, 2, 5, 2, 7, 7, 8, 54, 2, 11];

// function mayorquemenorque(a, b) {
//     return a > b;
// }

// function miSort(miArray, comparar) {
//     // 1. Cambiado '>' por '<'
//     for (let i = 0; i < miArray.length; i++) {
//         let pivote = miArray[0];
        
//         // 2. Cambiado '>' por '<' y corregido '.length'
//         for (let j = 1; j < miArray.length - i; j++) {
//             if (comparar(pivote, miArray[j])) {
//                 // intercambio
//                 miArray[j - 1] = miArray[j];
//                 miArray[j] = pivote;
//             } else {
//                 pivote = miArray[j];
//             }
//         }
//     }
//     // 3. Añadido return para devolver el array ordenado
//     return miArray;
// }

// console.log(miSort(b, mayorquemenorque));





//     let personas = [
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

// function mayorquemenorque(a, b) {
//   return a > b;
// }

// function miSort(miArray, comparar) {
//   for (let i = 0; i < miArray.length; i++) {
//     // 1. Guardamos la FICHA ENTERA de la primera persona, no solo su edad
//     let pivote = miArray[0];

//     for (let j = 1; j < miArray.length - i; j++) {
//       // 2. Comparamos las EDADES ([1]) de la ficha pivote y la ficha actual
//       if (comparar(pivote[1], miArray[j][1])) {
//         // 3. Intercambiamos las FICHAS ENTERAS
//         miArray[j - 1] = miArray[j];
//         miArray[j] = pivote;
//       } else {
//         // 4. Actualizamos el pivote con la FICHA ENTERA
//         pivote = miArray[j];
//       }
//     }
//   }

//   return miArray;
// }

// console.table(miSort(personas, mayorquemenorque));









//REPASAR ESTO 

// let personas = [
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

// function obtenerNumeroDeRol(rol) {
//   if (rol === "Profesor") {
//     return 1;
//   } else if (rol === "Administrativo") {
//     return 2;
//   } else {
//     return 3;
//   }  
// }

// function estanAlReves(personaA, personaB) {
//   let nombreA = personaA[0];
//   let edadA   = personaA[1];
//   let rolA    = obtenerNumeroDeRol(personaA[2]);

//   let nombreB = personaB[0];
//   let edadB   = personaB[1];
//   let rolB    = obtenerNumeroDeRol(personaB[2]);

//   if (rolA !== rolB) {
//     return rolA > rolB;
//   }

//   if (edadA !== edadB) {
//     return edadA > edadB;
//   }

//   return nombreA.localeCompare(nombreB) > 0;
// }

// function ordenar(lista, funcionComparadora) {
//   for (let ronda = 0; ronda < lista.length; ronda++) {
//     let pivote = lista[0];

//     for (let pos = 1; pos < lista.length - ronda; pos++) {
//       if (funcionComparadora(pivote, lista[pos])) {
//         lista[pos - 1] = lista[pos];
//         lista[pos] = pivote;
//       } else {
//         pivote = lista[pos];
//       }
//     }
//   }

//   return lista;
// }

// let personasOrdenadas = ordenar(personas, estanAlReves);
// console.table(personasOrdenadas);

// ESTO 


//para el examen de interfisis fuentes tamaño estilo y variantes, uso tipoco dar formato basico al texto 
//listas list-style-type list style asignar posiciones separadas por comas a la vez 
// margin 
//leere primer tma parte de css hasta punto 8  












