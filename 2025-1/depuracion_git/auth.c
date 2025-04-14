/* auth.c */

#include <stdio.h>
#include <string.h>

/**
 * Función: autenticarUsuario
 * ---------------------------
 * Verifica si el usuario y contraseña proporcionados son correctos.
 *
 * usuario: cadena con el nombre de usuario.
 * password: cadena con la contraseña.
 *
 * Retorna:
 *   1 si la autenticación es exitosa,
 *   0 en caso contrario.
 */
int autenticarUsuario(const char* usuario, const char* password) {
    // En este ejemplo, la autenticación es exitosa únicamente para el usuario "admin" y password "12345".
    if (strcmp(usuario, "admin") == 0 && strcmp(password, "12345") == 0) {
        return 1;  // Autenticación exitosa.
    }
    return 0;      // Fallo en la autenticación.
}
