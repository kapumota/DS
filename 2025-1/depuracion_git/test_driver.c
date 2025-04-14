/* test_driver.c */

#include <stdio.h>

// Declaración de la función implementada en auth.c.
extern int autenticarUsuario(const char* usuario, const char* password);

int main(void) {
    // Valores de prueba.
    const char* usuario = "admin";
    const char* password = "12345";

    // Se invoca la función.
    if (autenticarUsuario(usuario, password)) {
        printf("Autenticacion exitosa\n");
        return 0;
    } else {
        printf("Fallo en la autenticacion\n");
        return 1;
    }
}
