#!/usr/bin/env python3
"""
Testes unitários para o módulo utils
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """
    Casos de teste para a função access_nested_map
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Testa que access_nested_map retorna o resultado esperado
        """
        resultado = access_nested_map(nested_map, path)
        self.assertEqual(resultado, expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, missing_key):
        """
        Testa que access_nested_map levanta KeyError para caminhos inválidos
        """
        with self.assertRaises(KeyError) as contexto:
            access_nested_map(nested_map, path)
        
        # Verifica se a mensagem de erro contém a chave que faltou
        self.assertIn(missing_key, str(contexto.exception))


if __name__ == '__main__':
    unittest.main()