import copy

class HistoryManager:
    """
    Gestionnaire d'historique pour undo/redo des opérations de filtrage et tri.
    """
    
    def __init__(self, max_history=50):
        """
        Initialise le gestionnaire d'historique.
        
        Args:
            max_history: Nombre maximum d'états à conserver (défaut: 50)
        """
        self.history = []  # Liste des états précédents
        self.current_index = -1  # Index de l'état actuel
        self.max_history = max_history
        self.original_data = None  # Données originales (avant tout traitement)
    
    def save_state(self, data, operation_description=""):
        """
        Sauvegarde un état dans l'historique.
        
        Args:
            data: Données à sauvegarder
            operation_description: Description de l'opération effectuée
        """
        # Faire une copie profonde des données
        data_copy = copy.deepcopy(data)
        
        # Si on est au milieu de l'historique, supprimer les états futurs
        if self.current_index < len(self.history) - 1:
            self.history = self.history[:self.current_index + 1]
        
        # Ajouter le nouvel état
        self.history.append({
            'data': data_copy,
            'description': operation_description,
            'count': len(data_copy)
        })
        
        # Limiter la taille de l'historique
        if len(self.history) > self.max_history:
            self.history.pop(0)
        else:
            self.current_index = len(self.history) - 1
    
    def set_original(self, data):
        """
        Définit les données originales (chargement initial).
        
        Args:
            data: Données originales
        """
        self.original_data = copy.deepcopy(data)
        # Réinitialiser l'historique
        self.history = []
        self.current_index = -1
        # Sauvegarder l'état initial
        self.save_state(data, "Données chargées")
    
    def undo(self):
        """
        Annule la dernière opération (undo).
        
        Returns:
            tuple: (data, description) ou (None, None) si impossible
        """
        if self.current_index > 0:
            self.current_index -= 1
            state = self.history[self.current_index]
            return copy.deepcopy(state['data']), state['description']
        elif self.current_index == 0 and self.original_data is not None:
            # Retourner aux données originales
            self.current_index = -1
            return copy.deepcopy(self.original_data), "Données originales"
        return None, None
    
    def redo(self):
        """
        Refait la dernière opération annulée (redo).
        
        Returns:
            tuple: (data, description) ou (None, None) si impossible
        """
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            state = self.history[self.current_index]
            return copy.deepcopy(state['data']), state['description']
        return None, None
    
    def can_undo(self):
        """
        Vérifie si une opération undo est possible.
        
        Returns:
            bool: True si undo est possible
        """
        return self.current_index > 0 or (self.current_index == 0 and self.original_data is not None)
    
    def can_redo(self):
        """
        Vérifie si une opération redo est possible.
        
        Returns:
            bool: True si redo est possible
        """
        return self.current_index < len(self.history) - 1
    
    def get_history_info(self):
        """
        Retourne des informations sur l'historique.
        
        Returns:
            dict: Informations sur l'historique
        """
        return {
            'current_index': self.current_index,
            'total_states': len(self.history),
            'can_undo': self.can_undo(),
            'can_redo': self.can_redo(),
            'current_description': self.history[self.current_index]['description'] if self.history else None
        }
    
    def reset(self):
        """
        Réinitialise l'historique.
        """
        self.history = []
        self.current_index = -1
        self.original_data = None

