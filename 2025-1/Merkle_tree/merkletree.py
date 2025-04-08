import hashlib

class MerkleTree:
    """
    El árbol de Merkle es un árbol binario especial que permite prevenir la manipulación
    de la información y preservar su integridad utilizando funciones de hash criptográficas.
    Cada nivel del árbol se deriva del hash de sus nodos hijos, de modo que un cambio en un
    archivo se propaga a través de la estructura, haciendo evidente cualquier intento de manipulación.
    """

    class __Node:
        def __init__(self, item=None, left=None, right=None):
            """
            Constructor de un nodo del árbol de Merkle.

            Args:
                item (bytes): Objeto de tipo bytes que representa el valor hash del nodo.
                left (__Node): Referencia al nodo izquierdo (puede ser None si es hoja).
                right (__Node): Referencia al nodo derecho (puede ser None si es hoja).
            """
            self.left = left
            self.right = right
            self.__value = item

        @property
        def value(self):
            return self.__value

        @value.setter
        def value(self, value):
            self.__value = value

        def __str__(self):
            return 'Value: {0}'.format(self.value)

        def __repr__(self):
            # Representación recursiva simple (útil para depuración)
            return self.__str__() + '\n\t' + (self.left.__repr__() if self.left else 'None') + \
                   '\n\t' + (self.right.__repr__() if self.right else 'None')

    def __init__(self, iterable, digest_delegate=None):
        """
        Constructor del árbol de Merkle.

        Args:
            iterable (iterable): Colección a partir de la cual se construye el árbol.
            digest_delegate (function): Función que recibe un elemento y devuelve su hash.
                                          Si no se especifica, se usa SHA-1.
        """
        if digest_delegate is None:
            digest_delegate = self.__sha1_digest
        self.digest = digest_delegate
        self.__root = self.build_root(iterable)

    @property
    def root(self):
        return self.__root

    def __sha1_digest(self, element):
        """
        Función digest utilizando SHA-1.

        Args:
            element: Puede ser un entero, cadena o bytes.
        Returns:
            bytes: El valor hash en formato bytes.
        """
        H = hashlib.sha1()
        if isinstance(element, bytes):
            H.update(element)
        elif isinstance(element, str):
            H.update(element.encode('utf-8'))
        elif isinstance(element, int):
            # Se usa un byte mínimo para enteros pequeños
            byte_length = (element.bit_length() + 7) // 8 or 1
            H.update(element.to_bytes(byte_length, byteorder='big'))
        else:
            # Fallback: convertir a cadena y codificar
            H.update(str(element).encode('utf-8'))
        return H.digest()

    def build_root(self, iterable):
        """
        Construye la raíz del árbol de Merkle a partir de la colección.

        Args:
            iterable (iterable): Colección de elementos para el árbol.

        Returns:
            __Node: Raíz del árbol de Merkle.
        """
        collection = list(iterable)
        if len(collection) == 0:
            raise Exception("La colección no puede estar vacía.")

        # Si la cantidad de elementos es impar, se duplica el último para formar un par.
        if len(collection) % 2 != 0:
            collection.extend(collection[-1:])

        # Crear nodos hoja usando el digest aplicado a cada elemento
        collection = [self.__Node(self.digest(x)) for x in collection]
        return self.__build_root(collection)

    def __build_root(self, collection):
        size = len(collection)
        if size == 1:
            return collection[0]

        # Si es impar, se duplica el último nodo para tener pares completos
        if size % 2 != 0:
            collection.append(self.__Node(collection[-1].value, left=collection[-1].left, right=collection[-1].right))

        next_level = []
        i = 0
        while i < size:
            # Concatenar los valores hash de los dos nodos y aplicar la función digest
            digest = self.digest(collection[i].value + collection[i+1].value)
            node = self.__Node(digest, left=collection[i], right=collection[i+1])
            next_level.append(node)
            i += 2
        return self.__build_root(next_level)

    def contains(self, value):
        """
        Comprueba si un valor está contenido en el árbol.

        Args:
            value: El valor a buscar.
        Returns:
            bool: True si se encuentra, False en otro caso.
        """
        if value is None or self.root is None:
            return False

        hashed_value = self.digest(value)
        return self.__find(self.root, hashed_value) is not None

    def __find(self, node, value):
        """
        Búsqueda interna en el árbol.

        Args:
            node (__Node): Nodo actual.
            value: Valor (hash) a buscar.
        Returns:
            __Node o None: El nodo si se encuentra; None en otro caso.
        """
        if node is None:
            return None
        if node.value == value:
            return node
        return self.__find(node.left, value) or self.__find(node.right, value)

    def request_proof(self, value):
        """
        Proporciona la prueba (Merkle branch) para demostrar la integridad de un elemento.

        Args:
            value: El elemento para el cual se solicita la prueba.
        Returns:
            list: Lista de tuplas representando la rama de Merkle.
        Throws:
            Exception: Si el valor no se encuentra en el árbol.
        """
        hashed_value = self.digest(value)
        if self.__find(self.root, hashed_value) is None:
            raise Exception('Este elemento no se encuentra en el árbol.')

        proof = []
        self.__build_valid_proof(self.root, hashed_value, proof)
        if len(proof) != 0:
            # Se inserta la rama final (la raíz) en la prueba
            proof.insert(0, (0 if proof[1][0] else 1, hashed_value))
        return proof

    def __build_valid_proof(self, node, value, proof_list):
        if node is None:
            return False
        if node.value == value:
            return True

        found_left = self.__build_valid_proof(node.left, value, proof_list)
        found_right = self.__build_valid_proof(node.right, value, proof_list)
        if not found_left and not found_right:
            return False

        # Si se encuentra en el subárbol izquierdo, se añade el hash del hijo derecho y viceversa
        n = (0, node.right.value) if found_left else (1, node.left.value)
        proof_list.append(n)
        return True

    def dump(self, indent=0):
        if self.root is None:
            return
        self.__print(self.root, indent)

    def __print(self, node, indent):
        if node is None:
            return
        print('{0}Node: {1}'.format(' ' * indent, node.value))
        self.__print(node.left, indent + 2)
        self.__print(node.right, indent + 2)

    def __contains__(self, value):
        hashed_value = self.digest(value)
        return self.__find(self.root, hashed_value)
