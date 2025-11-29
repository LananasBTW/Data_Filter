import config
from modules import file_manager as fm
from modules import filter
from modules import stats
from modules import sort
from modules import display
from modules import history
from modules import field_manager

def main():
    # Init
    data = []
    current_filepath = None
    history_manager = history.HistoryManager()

    while True:

        try:
            display.clear()
            display.welcome()
            
            # Obtenir les informations de l'historique
            history_info = history_manager.get_history_info() if data else None
            choice = display.menu(current_filepath, data, history_info)
            if not choice: continue

            match choice:
            
                # CHARGEMENT
                case "1":
                    path = display.request_file_path("charger")
                    new_data = fm.load_data(path)
                    
                    if new_data:
                        data = new_data
                        current_filepath = path
                        history_manager.set_original(data)
                        print(f"✅ {len(data)} éléments chargés avec succès.\n")
                    else:
                        print("❌ Échec du chargement ou fichier vide.\n")

                # AFFICHAGE
                case "2":
                    if not data:
                        print("⚠️ Aucune donnée chargée. Veuillez charger un fichier d'abord.\n")
                    else:
                        display.show_current_file(current_filepath, data)
                        display.print_data(data, current_filepath)

                # STATISTIQUES
                case "3":
                    if not data:
                        print("⚠️ Aucune donnée chargée. Veuillez charger un fichier d'abord.\n")
                    else:
                        report = stats.analyze_structure(data)
                        display.print_stats(report)

                # FILTRAGE
                case "4":
                    if not data:
                        print("⚠️ Aucune donnée chargée. Veuillez charger un fichier d'abord.\n")
                    else:
                        champ, operator, valeur = display.request_filter_criteria(data)
                        if champ and operator is not None:
                            filtered_data = filter.filter_data(data, champ, operator, valeur)
                            print(f"✅ Filtre appliqué. {len(filtered_data)} résultats conservés (sur {len(data)}).\n")
                            history_manager.save_state(filtered_data, f"Filtre: {champ} {operator} {valeur}")
                            data = filtered_data
                        else:
                            print("❌ Filtrage annulé.\n")

                # TRI
                case "5":
                    if not data:
                        print("⚠️ Aucune donnée chargée. Veuillez charger un fichier d'abord.\n")
                    else:
                        champ, reverse = display.request_sort_field(data)
                        if champ:
                            sorted_data = sort.sort_data(data, field=champ, reverse=reverse)
                            order = "décroissant" if reverse else "croissant"
                            history_manager.save_state(sorted_data, f"Tri: {champ} ({order})")
                            data = sorted_data
                            print("✅ Données triées.")
                        else:
                            print("❌ Tri annulé.\n")

                # SAUVEGARDE
                case "6":
                    if not data:
                        print("⚠️ Rien à sauvegarder.\n")
                    else:
                        path = display.request_file_path("sauvegarder")
                        output_path = fm.save_data(data, path)
                        print(f"✅ Données sauvegardées dans : {output_path}\n")

                # FILTRES COMBINÉS
                case "7":
                    if not data:
                        print("⚠️ Aucune donnée chargée. Veuillez charger un fichier d'abord.\n")
                    else:
                        filters, logic = display.request_combined_filters(data)
                        if filters:
                            filtered_data = filter.filter_combined(data, filters, logic)
                            logic_str = "ET" if logic == "AND" else "OU"
                            filters_desc = ", ".join([f"{f[0]} {f[1]} {f[2]}" for f in filters])
                            print(f"✅ Filtres combinés ({logic_str}) appliqués. {len(filtered_data)} résultats conservés (sur {len(data)}).\n")
                            print(f"   Critères: {filters_desc}\n")
                            history_manager.save_state(filtered_data, f"Filtres combinés ({logic_str}): {filters_desc}")
                            data = filtered_data
                        else:
                            print("❌ Filtrage annulé.\n")

                # GESTION DES CHAMPS
                case "8":
                    if not data:
                        print("⚠️ Aucune donnée chargée. Veuillez charger un fichier d'abord.\n")
                    else:
                        action, field_name, extra = display.request_field_management(data)
                        if action == 'add':
                            data = field_manager.add_field(data, field_name, extra)
                            history_manager.save_state(data, f"Ajout du champ: {field_name}")
                            print(f"✅ Champ '{field_name}' ajouté avec succès.\n")
                        elif action == 'remove':
                            data = field_manager.remove_field(data, field_name)
                            history_manager.save_state(data, f"Suppression du champ: {field_name}")
                            print(f"✅ Champ '{field_name}' supprimé avec succès.\n")
                        elif action == 'rename':
                            old_name, new_name = field_name, extra
                            data = field_manager.rename_field(data, old_name, new_name)
                            history_manager.save_state(data, f"Renommage: {old_name} → {new_name}")
                            print(f"✅ Champ '{old_name}' renommé en '{new_name}' avec succès.\n")
                        else:
                            print("❌ Opération annulée.\n")

                # UNDO
                case "9":
                    if not data:
                        print("⚠️ Aucune donnée chargée.\n")
                    else:
                        undo_data, description = history_manager.undo()
                        if undo_data is not None:
                            data = undo_data
                            print(f"✅ Opération annulée: {description}\n")
                            print(f"📊 {len(data)} éléments restaurés.\n")
                        else:
                            print("⚠️ Aucune opération à annuler.\n")

                # REDO
                case "A":
                    if not data:
                        print("⚠️ Aucune donnée chargée.\n")
                    else:
                        redo_data, description = history_manager.redo()
                        if redo_data is not None:
                            data = redo_data
                            print(f"✅ Opération refaite: {description}\n")
                            print(f"📊 {len(data)} éléments restaurés.\n")
                        else:
                            print("⚠️ Aucune opération à refaire.\n")

                # QUITTER
                case "0":
                    print("👋 Au revoir !\n")
                    break

                case _: print("❌ Choix invalide, veuillez réessayer.\n")
        
        except Exception as e:
            print(f"❌ Une erreur est survenue : {e}\n")

        input("Appuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    main()
