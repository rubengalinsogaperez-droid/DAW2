//Ruben Galinsoga Perez
document.write("<H2>Aqui estoy yo</H2>");
let respuesta=prompt("Elige una opción:\n +"
                      + "1. Gato 🐱\n"
                      + "2. Perro 🐶\n"
                      + "3. Conejo 🐰\n"
                      + "4. Pájaro 🐦");
respuesta=parseInt(respuesta);

if (respuesta == 1) {
    document.write('<img src="gato.jpg">');
}
if (respuesta == 2) {
    document.write('<img src="perro.jpg">');
}
if (respuesta == 3) {
    document.write('<img src="conejo.jpg">');
}
if (respuesta == 4) {
    document.write('<img src="paloma.jpg">');
}

