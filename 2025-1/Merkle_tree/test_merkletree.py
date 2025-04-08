import hashlib
import unittest
# Se asume que la clase MerkleTree se encuentra en un módulo llamado merkletree.
import merkletree

def H(element):
    """
    Función auxiliar para computar el hash SHA-1.
    Soporta tipos: str, int, bytes.
    """
    H_obj = hashlib.sha1()
    if isinstance(element, bytes):
        H_obj.update(element)
    elif isinstance(element, str):
        H_obj.update(element.encode('utf-8'))
    elif isinstance(element, int):
        byte_length = (element.bit_length() + 7) // 8 or 1
        H_obj.update(element.to_bytes(byte_length, byteorder='big'))
    else:
        H_obj.update(str(element).encode('utf-8'))
    return H_obj.digest()

class MerkleTest(unittest.TestCase):

    def test_unable_to_build_from_empty_collection(self):
        # Se espera que se lance una excepción al pasar una colección vacía.
        with self.assertRaises(Exception):
            merkletree.MerkleTree([])

    def test_merkle_no_digest(self):
        # Se crean árboles sin pasar una función digest explícita; se usará el SHA-1 por defecto.
        tree_even = merkletree.MerkleTree([1, 2, 3, 4, 5, 6])
        tree_odd = merkletree.MerkleTree([1, 2, 3, 4, 5])
        
        # Calcular el valor esperado para la colección par:
        even_digest = [H(x) for x in [1, 2, 3, 4, 5, 6]]
        d12 = H(even_digest[0] + even_digest[1])
        d34 = H(even_digest[2] + even_digest[3])
        d56 = H(even_digest[4] + even_digest[5])
        d1234 = H(d12 + d34)
        d5656 = H(d56 + d56)
        expected_even = H(d1234 + d5656)
        
        # Calcular el valor esperado para la colección impar:
        odd_digest = [H(x) for x in [1, 2, 3, 4, 5]]
        # Duplicar el último elemento para formar el par.
        odd_digest.append(odd_digest[-1])
        d12 = H(odd_digest[0] + odd_digest[1])
        d34 = H(odd_digest[2] + odd_digest[3])
        d55 = H(odd_digest[4] + odd_digest[5])
        d1234 = H(d12 + d34)
        d5555 = H(d55 + d55)
        expected_odd = H(d1234 + d5555)

        even_error_feedback = 'Incorrecta raíz para el árbol par.'
        odd_error_feedback = 'Incorrecta raíz para el árbol impar.'
        
        self.assertEqual(tree_even.root.value, expected_even, even_error_feedback)
        self.assertEqual(tree_odd.root.value, expected_odd, odd_error_feedback)

    def test_merkle_with_cryptographic_digest(self):
        # Secuencias de ejemplo para transacciones y números
        even_sequence = ['tx1', 'tx2', 'tx3', 'tx4']
        odd_sequence = [1, 2, 3, 8, 9, 9, 9, 9]

        # Usar la función H (SHA-1) para calcular cada hash.
        tree_even = merkletree.MerkleTree(even_sequence, digest_delegate=H)
        tree_odd = merkletree.MerkleTree(odd_sequence, digest_delegate=H)

        even_digest = [H(x) for x in even_sequence]
        odd_digest = [H(x) for x in odd_sequence]

        # Para el árbol par, se toma como:
        # raíz = H( H(even_digest[0] + even_digest[1]) + H(even_digest[2] + even_digest[3]) )
        d12 = H(even_digest[0] + even_digest[1])
        d34 = H(even_digest[2] + even_digest[3])
        root_even = H(d12 + d34)

        # Para el árbol impar, se separa en dos mitades:
        # Se supone que el número de elementos es par (ya que se duplicará el último en caso de ser impar)
        d_left = H(H(odd_digest[0] + odd_digest[1]) + H(odd_digest[2] + odd_digest[3]))
        d_right = H(H(odd_digest[4] + odd_digest[5]) + H(odd_digest[6] + odd_digest[7]))
        root_odd = H(d_left + d_right)
        
        even_error_feedback = 'Incorrecta raíz para el árbol par con digest SHA-1.'
        odd_error_feedback = 'Incorrecta raíz para el árbol impar con digest SHA-1.'

        self.assertEqual(tree_even.root.value, root_even, even_error_feedback)
        self.assertEqual(tree_odd.root.value, root_odd, odd_error_feedback)

if __name__ == '__main__':
    unittest.main(verbosity=2)