

//ejercicio 1 PREPARACIONEXAMEN

let importe = prompt("Dime el importe a pagar");
let entregado = prompt("Dime el dinero entregado");

importecent = importe + "00";
entregadocent = entregado + "00";
importecent = parseInt(importecent.trim());
entregadocent = parseInt(entregadocent.trim());
console.log(cobrar(importecent, entregadocent));

function cobrar(importe, entregado){
    let importemaximo = 20;
    if (importe > entregado) {
        return "No hay dinero suficiente te quedan por pagarme " + (importe - entregado) + " centimos";
    }
    if (importe == entregado) {
            return "Pago exacto no hay cambio";
    }
    if (importe < entregado) {
        let devolverbillete10 = 0;
        let devolverbillete5 = 0;
        let devolvermoneda200 = 0;
        let devolvermoneda100 = 0;
        let devolervermoneda50 = 0;
        let devolvermoneda20 = 0;
        let devolvermoneda10 = 0;
        let devolveremoneda5 = 0;
        let devolvermoneda2 = 0;
        let devolvermoneda1 = 0;

        let billete10 = 1000;
        let billete5 = 500;
        let moneda200 = 200;
        let moneda100 = 100;
        let moneda50 = 50;
        let moneda20 = 20;
        let moneda10 = 10;
        let moneda5 = 5;
        let moneda2 = 2;
        let moneda1 = 1;
        if (entregado - billete10 >= importe) {
            while (entregado >= billete10 && entregado - billete10 >= importe) {
                entregado -= billete10;
                devolverbillete10 +=1;
            }
        }
        if (entregado - billete5 >= importe) {
            while (entregado >= billete5 && entregado - billete5 >= importe) {
                entregado -= billete5;
                devolverbillete5 +=1;
            }
        }
        if (entregado - moneda200 >= importe) {
            while (entregado >= moneda200 && entregado - moneda200 >= importe) {
                entregado -= moneda200;
                devolvermoneda200 +=1;
            }  
        }
        if (entregado - moneda100 >= importe) {
            while (entregado >= moneda100 && entregado - moneda100 >= importe) {
                entregado -= moneda100;
                devolvermoneda100 +=1;
            }
        }
        if (entregado - moneda50 >= importe) {
            while (entregado >= moneda50 && entregado - moneda50 >= importe) {
                entregado -= moneda50;
                devolervermoneda50 +=1;
            }
        }
        if (entregado - moneda20 >= importe) {
            while (entregado >= moneda20 && entregado - moneda20 >= importe) {
                entregado -= moneda20;
                devolvermoneda20 +=1;
            }
        }
        if (entregado - moneda10 >= importe) {
            while (entregado >= moneda10 && entregado - moneda10 >= importe) {
                entregado -= moneda10;
                devolvermoneda10 +=1;
            }
        }
        if (entregado - moneda5 >= importe) {
            while (entregado >= moneda5 && entregado - moneda5 >= importe) {
                entregado -= moneda5;
                devolveremoneda5 +=1;
            }
        }
        if (entregado - moneda2 >= importe) {
            while (entregado >= moneda2 && entregado - moneda2 >= importe) {
                entregado -= moneda2;
                devolvermoneda2 +=1;
            }
        }
        if (entregado - moneda1 >= importe) {
            while (entregado >= moneda1 && entregado - moneda1 >= importe) {
                entregado -= moneda1;
                devolvermoneda1 +=1;
            }
        }
        
        return "Te devuelvo " + (entregado - importe) + " centimos, en billetes y monedas: \n" + devolverbillete10 + " billetes de 10€, \n" + devolverbillete5 + " billetes de 5€,\n" + devolvermoneda200 + " monedas de 2€,\n" + devolvermoneda100 + " monedas de 1€,\n" + devolervermoneda50 + " monedas de 50 centimos,\n" + devolvermoneda20 + " monedas de 20 centimos,\n" + devolvermoneda10 + " monedas de 10 centimos,\n" + devolveremoneda5 + " monedas de 5 centimos,\n" + devolvermoneda2 + " monedas de 2 centimos, y\n" + devolvermoneda1 + " monedas de 1 centimo";
    }
}