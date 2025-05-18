#!/usr/bin/env bash
# Hook de pre-push para Git
#
# Este hook se ejecuta antes de un `git push`.
# 1. Ejecuta las pruebas del proyecto usando `make test`.
# 2. Valida que los mensajes de los commits sigan el formato de conventional commits.
#
# Si alguna de estas comprobaciones falla, el push se aborta.

# Salir inmediatamente si un comando falla (-e), si se usa una variable no definida (-u),
# o si un comando en un pipeline falla (-o pipefail). (opcional)
set -euo pipefail

# Configuración
# Expresión regular para Conventional Commits (ajustar si es necesario)
# Tipos permitidos: feat, fix, chore, docs, style, refactor, test, perf, ci, build, revert
CONVENTIONAL_COMMIT_REGEX='^(feat|fix|chore|docs|style|refactor|test|perf|ci|build|revert)(\(.+\))?: .{1,100}'
# Directorio raíz del proyecto (donde está el Makefile)
PROJECT_ROOT=$(git rev-parse --show-toplevel)

#  Funciones auxiliares 
print_error() {
    echo -e "\033[0;31mERROR: $1\033[0m" >&2
}

print_success() {
    echo -e "\033[0;32mSUCCESS: $1\033[0m"
}

print_info() {
    echo -e "\033[0;34mINFO: $1\033[0m"
}

# 1. Ejecutar Pruebas ---
print_info "Ejecutando pruebas ('make test')..."
if ! (cd "$PROJECT_ROOT" && make test); then
    print_error "Las pruebas fallaron. Revisa los errores antes de hacer push."
    print_error "Puedes ejecutar 'make test' manualmente para más detalles."
    exit 1
fi
print_success "Todas las pruebas pasaron."

#  2. Validar Mensajes de Commit ---
print_info "Validando mensajes de commit..."

# Leer las referencias local y remota que se están empujando
# Formato de entrada: <local_ref> <local_sha1> <remote_ref> <remote_sha1>
while read -r local_ref local_sha remote_ref remote_sha; do
    # Si remote_sha es todo ceros, es una rama nueva. Validar desde el primer commit.
    # Si no, es una actualización de rama. Validar el rango de commits.
    if [[ "$remote_sha" == "0000000000000000000000000000000000000000" ]]; then
        # Rama nueva: obtener todos los commits hasta local_sha que no están en otras ramas remotas
        # Esto es complejo; una aproximación simple es desde el ancestro común con la rama por defecto (main/master)
        # O, si es más simple, desde el "divergence point" con origin/<default_branch>
        # Para simplificar, podemos usar `git rev-list $local_sha --not --remotes`
        # O simplemente tomar los commits que no están en el remote_ref si éste existiera antes (no es el caso aquí)
        # Una forma más común para ramas nuevas:
        main_branch=$(git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@' || echo "main") # o master
        range_to_check=$(git rev-list "origin/${main_branch}..${local_sha}" --abbrev-commit || git rev-list "${local_sha}" --abbrev-commit)
        if [ -z "$range_to_check" ]; then # Si no hay ancestro común o es el primer commit
             range_to_check=$(git rev-list "${local_sha}" --abbrev-commit)
        fi

        print_info "Validando commits para la nueva rama: $local_ref (commits: $local_sha)"
    else
        range_to_check=$(git rev-list "${remote_sha}..${local_sha}" --abbrev-commit)
        print_info "Validando commits para la rama existente: $local_ref (rango: $remote_sha..$local_sha)"
    fi

    if [ -z "$range_to_check" ]; then
        print_info "No hay nuevos commits para validar en $local_ref."
        continue
    fi

    print_info "Commits a validar:"
    echo "$range_to_check" | sed 's/^/  /' # Imprimir lista de commits

    # Iterar sobre cada commit en el rango
    invalid_commits_found=0
    for commit_hash in $range_to_check; do
        commit_subject=$(git log --format=%s -n 1 "$commit_hash")
        if [[ ! "$commit_subject" =~ $CONVENTIONAL_COMMIT_REGEX ]]; then
            print_error "Commit $commit_hash tiene un mensaje NO CONVENCIONAL: '$commit_subject'"
            invalid_commits_found=$((invalid_commits_found + 1))
        fi
    done

    if [ "$invalid_commits_found" -gt 0 ]; then
        print_error "Se encontraron $invalid_commits_found commits con mensajes no convencionales."
        echo "Por favor, sigue el formato Conventional Commits:" >&2
        echo "  Ej: 'feat: añadir nueva funcionalidad'" >&2
        echo "  Tipos permitidos: feat, fix, chore, docs, style, refactor, test, perf, ci, build, revert." >&2
        echo "  Puedes usar 'git commit --amend' o 'git rebase -i' para corregir los mensajes." >&2
        exit 1
    fi
done

print_success "Todos los mensajes de commit son válidos."
print_info "Pre-push hook finalizado exitosamente. Permitiendo push."
exit 0
