import unittest
import os
import sys
import json
import shutil
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules import file_manager as fm
import config

class TestFormatSave(unittest.TestCase):
    """Tests unitaires pour vérifier la sauvegarde des différents formats de fichiers."""
    
    @classmethod
    def setUpClass(cls):
        """Initialisation avant tous les tests."""
        config.OUTPUT_DIR = str(Path(__file__).parent / "fixtures")
        config.TMP_DIR = str(Path(__file__).parent / "tmp")
        os.makedirs(config.OUTPUT_DIR, exist_ok=True)
        os.makedirs(config.TMP_DIR, exist_ok=True)
    
    @classmethod
    def tearDownClass(cls):
        """Nettoyage après tous les tests."""
        shutil.rmtree(config.OUTPUT_DIR, ignore_errors=True)
        shutil.rmtree(config.TMP_DIR, ignore_errors=True)
        
    def setUp(self):
        """Initialisation avant chaque test."""
        self.test_data = [
            {
                "id": 1,
                "name": "Alice",
                "age": 25,
                "score": 98.5,
                "active": True,
                "tags": ["python", "data"],
                "metadata": {"level": "senior", "years": 5}
            },
            {
                "id": 2,
                "name": "Bob",
                "age": 30,
                "score": 87.3,
                "active": False,
                "tags": ["java"],
                "metadata": {"level": "junior", "years": 2}
            }
        ]
    
    # ========== Tests JSON - Sauvegarde ==========
    
    def test_json_save_and_reload_types(self):
        """Test que les types de données sont préservés lors de la sauvegarde et du rechargement JSON."""
        output_path = fm.save_data(self.test_data, "test_types.json")
        
        # Recharger les données
        loaded_data = fm.load_data(output_path)
        
        # Vérifier que les types sont préservés
        self.assertIsInstance(loaded_data[0]['id'], int, "L'ID doit rester un entier")
        self.assertIsInstance(loaded_data[0]['age'], int, "L'âge doit rester un entier")
        self.assertIsInstance(loaded_data[0]['score'], float, "Le score doit rester un float")
        self.assertIsInstance(loaded_data[0]['active'], bool, "Active doit rester un booléen")
        self.assertIsInstance(loaded_data[0]['tags'], list, "Tags doit rester une liste")
        self.assertIsInstance(loaded_data[0]['metadata'], dict, "Metadata doit rester un dictionnaire")
        
        # Vérifier les valeurs exactes
        self.assertEqual(loaded_data[0]['id'], 1)
        self.assertEqual(loaded_data[0]['age'], 25)
        self.assertEqual(loaded_data[0]['score'], 98.5)
        self.assertTrue(loaded_data[0]['active'])
        self.assertFalse(loaded_data[1]['active'])
    
    def test_json_save_complex_nested_structures(self):
        """Test de la sauvegarde de structures imbriquées complexes en JSON."""
        complex_data = [
            {
                "id": 1,
                "nested": {
                    "level1": {
                        "level2": {
                            "value": 42,
                            "list": [1, 2, 3]
                        }
                    }
                }
            }
        ]
        
        output_path = fm.save_data(complex_data, "test_nested.json")
        loaded_data = fm.load_data(output_path)
        
        self.assertEqual(loaded_data[0]['nested']['level1']['level2']['value'], 42)
        self.assertIsInstance(loaded_data[0]['nested']['level1']['level2']['list'], list)
    
    # ========== Tests CSV - Sauvegarde ==========
    
    def test_csv_save_and_reload_types(self):
        """Test que les types de données sont préservés lors de la sauvegarde et du rechargement CSV."""
        output_path = fm.save_data(self.test_data, "test_types.csv")
        
        # Recharger les données
        loaded_data = fm.load_data(output_path)
        
        # Vérifier que les types sont préservés
        self.assertIsInstance(loaded_data[0]['id'], int, "L'ID doit rester un entier")
        self.assertIsInstance(loaded_data[0]['age'], int, "L'âge doit rester un entier")
        self.assertIsInstance(loaded_data[0]['score'], float, "Le score doit rester un float")
        self.assertIsInstance(loaded_data[0]['active'], bool, "Active doit rester un booléen")
        self.assertIsInstance(loaded_data[0]['tags'], list, "Tags doit rester une liste")
        self.assertIsInstance(loaded_data[0]['metadata'], dict, "Metadata doit rester un dictionnaire")
        
        # Vérifier les valeurs
        self.assertEqual(loaded_data[0]['id'], 1)
        self.assertEqual(loaded_data[0]['score'], 98.5)
        self.assertTrue(loaded_data[0]['active'])
    
    def test_csv_save_list_and_dict_conversion(self):
        """Test que les listes et dictionnaires sont correctement convertis en CSV."""
        output_path = fm.save_data(self.test_data, "test_complex.csv")
        loaded_data = fm.load_data(output_path)
        
        # Vérifier que les listes sont correctement sérialisées et désérialisées
        self.assertEqual(loaded_data[0]['tags'], ["python", "data"])
        self.assertEqual(loaded_data[1]['tags'], ["java"])
        
        # Vérifier que les dictionnaires sont correctement sérialisés et désérialisés
        self.assertEqual(loaded_data[0]['metadata']['level'], "senior")
        self.assertEqual(loaded_data[0]['metadata']['years'], 5)
    
    # ========== Tests d'erreurs de sauvegarde ==========
    
    def test_save_empty_data(self):
        """Test de la sauvegarde de données vides."""
        with self.assertRaises(ValueError):
            fm.save_data([], "test_empty.json")
    
    def test_save_invalid_data_format(self):
        """Test de la sauvegarde avec un format de données invalide."""
        with self.assertRaises(ValueError):
            fm.save_data("not a list", "test_invalid.json")
    
    def test_save_invalid_file_format(self):
        """Test de la sauvegarde avec une extension non supportée."""
        with self.assertRaises(ValueError):
            fm.save_data(self.test_data, "test_invalid.txt")
    
    def test_save_empty_path(self):
        """Test de la sauvegarde avec un chemin vide."""
        with self.assertRaises(ValueError):
            fm.save_data(self.test_data, "")
    
    # ========== Tests de round-trip (sauvegarde puis rechargement) ==========
    
    def test_json_roundtrip_preserves_all_data(self):
        """Test que toutes les données sont préservées dans un cycle sauvegarde/rechargement JSON."""
        output_path = fm.save_data(self.test_data, "test_roundtrip.json")
        loaded_data = fm.load_data(output_path)
        
        self.assertEqual(len(loaded_data), len(self.test_data))
        self.assertEqual(loaded_data, self.test_data)
    
    def test_csv_roundtrip_preserves_all_data(self):
        """Test que toutes les données sont préservées dans un cycle sauvegarde/rechargement CSV."""
        output_path = fm.save_data(self.test_data, "test_roundtrip.csv")
        loaded_data = fm.load_data(output_path)
        
        self.assertEqual(len(loaded_data), len(self.test_data))
        self.assertEqual(loaded_data, self.test_data)
    
    # ========== Tests de cas spéciaux ==========
    
    def test_csv_save_inconsistent_fields(self):
        """Test de la sauvegarde CSV avec des champs différents entre les lignes."""
        inconsistent_data = [
            {"F1": {"count": 3}, "F2": 12.5, "F5": True},
            {"F3": ["count", 4], "F4": {"count": 1}, "F5": None},
            {"F1": 16.67, "F2": "feur", "F5": True},
            {"F5": False}
        ]
        
        output_path = fm.save_data(inconsistent_data, "test_inconsistent.csv")
        loaded_data = fm.load_data(output_path)
        
        # Vérifier que toutes les lignes sont présentes
        self.assertEqual(len(loaded_data), 4)
        
        # Vérifier que les champs manquants sont None
        self.assertIsNone(loaded_data[0].get('F3'))
        self.assertIsNone(loaded_data[0].get('F4'))
        self.assertIsNone(loaded_data[1].get('F1'))
        self.assertIsNone(loaded_data[1].get('F2'))
        self.assertIsNone(loaded_data[3].get('F1'))
        
        # Vérifier que les valeurs présentes sont correctes
        self.assertEqual(loaded_data[0]['F1'], {"count": 3})
        self.assertEqual(loaded_data[0]['F2'], 12.5)
        self.assertTrue(loaded_data[0]['F5'])
        self.assertFalse(loaded_data[3]['F5'])

if __name__ == '__main__':
    unittest.main()
