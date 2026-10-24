//Ruben Galinsoga Perez
// document.write("<H2>Aqui estoy yo</H2>");
// let respuesta=prompt("Elige una opción:\n +"
//                       + "1. Gato 🐱\n"
//                       + "2. Perro 🐶\n"
//                       + "3. Conejo 🐰\n"
//                       + "4. Pájaro 🐦");
// respuesta=parseInt(respuesta);

// if (respuesta == 1) {
//     document.write('<img src="gato.jpg">');
// }
// if (respuesta == 2) {
//     document.write('<img src="perro.jpg">');
// }
// if (respuesta == 3) {
//     document.write('<img src="conejo.jpg">');
// }
// if (respuesta == 4) {
//     document.write('<img src="paloma.jpg">');
// }


let filas = prompt("Dime el numero de filas para hacer tu tabla");
let columnas = prompt("Dime el numero de columnas para hacer tu tabla");

let cualfilaparar = prompt("Dime en que fila paro de hacer la tabla");
let cualcolumnaparar = prompt("Dime en que columna paro de hacer la tabla");


filas = parseInt(filas);
columnas = parseInt(columnas);
cualcolumnaparar = parseInt(cualcolumnaparar);
cualfilaparar = parseInt(cualfilaparar);

let codigotabla = "<table>";
let pararBucle = false; // Bandera (flag) para saber si debemos salir de los bucles


for (let i = 1; i <= filas; i++) {
    codigotabla += "<tr>";
    

    for (let u = 1; u <= columnas; u++) {
        codigotabla += `<td>Celda ${i},${u}</td>`;
        if (i === cualfilaparar && u === cualcolumnaparar) {
            
           
            let hacer = prompt("Has llegado a la celda indicada. Escribe 'Paro' si quieres abandonar la ejecución o cualquier otra cosa para continuar:");
            if (hacer === "Paro") {
                pararBucle = true; 
                break;            
            }
        }
    }
    
    codigotabla += "</tr>"; // Cerramos la fila actual
    
    // Si la bandera está activada, rompemos también el bucle externo de las filas
    if (pararBucle) {
        break;
    }
}


codigotabla += "</table>";


document.getElementById("resultado").innerHTML = codigotabla;