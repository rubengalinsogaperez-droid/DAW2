// let a = [3, 21, 14, 6, 25]ç
// let sum = 0;
// // console.log(a.includes)


// // every un elemento true or false, si lo cumple true si no false  TODOS

// console.log(a.every(num => num %2 == 0 ));

// //some ALGUNOS


// //forEach() A cada elemtno le pasa ala funcion, for each no devuelve ni modifica ni nada solo pasa la funcion a cada elemento,


// a.fotEach(num => sum += num);





// //map() filter() reduce().

// //reduce empieza desde la posicion 0 a adelatne hail hitler musolini



// let personas = [["leo", 21, "hijoputa"],
//                 ["pablo", 22, "desgraciao"]]


            
// let media = 0;
// //funcion que recibe dos parametros y un valor predetermiando
// media = personas.reduce((personas, edadAcumulada)=>{
//     return edadAcumulada+personas[1]}
//     ,0)/personas.length;

// console.logl(media);

// let masNumeros = [1, 1, 1, 1, 1, 1]


// console.log(masNumeros.reduce((ac, num)=> ac + num * 2, 0));




 //array de pares

let pares = aleatorios.filter(num=>num%2==0);

media = pares.reduce((acumulado, numeros)=>acumulado+num,0)/pares.length;


let diferencias=pares.map(num=>[num,media-num]);

































//nmumeros de 50 a 70 aleatorios
let aleatorios = [];

for (let i = 0; i<100;i++){
    aleatorios[i]=Math.floor(Math.random()*51)+20;
}

console.log(aleatorios);


//AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//
let numeros = [];

for (let i = 0; i < 10; i++) {
    numeros.push(Math.floor(Math.random() * 100) + 1);
}

let pares = numeros.filter(n => n % 2 === 0);

let dobles = pares.map(n => n * 2);

let suma = dobles.reduce((acumulador, n) => acumulador + n, 0);

let media = suma / dobles.length;

console.log("Números aleatorios:", numeros);
console.log("Números pares:", pares);
console.log("Doble de los pares:", dobles);
console.log("Media:", media);










let numeros = [];

for (let i = 0; i < 10; i++) {
    numeros.push(Math.floor(Math.random() * 100) + 1);
}

let pares = numeros.filter(n => n % 2 === 0);

let suma = pares.reduce((acumulador, n) => acumulador + n, 0);

let media = suma / pares.length;

let diferencias = pares.map(n => n - media);

console.log("Números aleatorios:", numeros);
console.log("Números pares:", pares);
console.log("Media:", media);
console.log("Diferencias respecto a la media:", diferencias);