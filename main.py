import sys

# On ajoute le dossier courant au path pour être sûr que les imports fonctionnent
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules import file_manager as fm, filter, stats, sort, display


def main():

    # Init
    data = []
    current_filepath = None

    while True:

        try:
            display.clear()
            display.welcome()
            choice = display.menu(current_filepath, data)

            match choice:
            
                # CHARGEMENT
                case "1":
                    path = display.request_file_path("charger")
                    new_data = fm.load_data(path)
                    
                    if new_data:
                        data = new_data
                        current_filepath = path
                        print(f"✅ {len(data)} éléments chargés avec succès.")
                    else:
                        print("❌ Échec du chargement ou fichier vide.")

                # AFFICHAGE
                case "2":
                    if not data:
                        print("⚠️ Aucune donnée chargée. Veuillez charger un fichier d'abord.")
                    else:
                        display.show_current_file(current_filepath, data)
                        display.print_data(data, current_filepath)

                # STATISTIQUES
                case "3":
                    if not data:
                        print("⚠️ Aucune donnée chargée. Veuillez charger un fichier d'abord.")
                    else:
                        report = stats.analyze_structure(data)
                        display.print_stats(report)

                # FILTRAGE
                case "4":
                    if not data:
                        print("⚠️ Aucune donnée chargée. Veuillez charger un fichier d'abord.")
                    else:
                        # Pas sur de faire comme ça mais à voir
                        champ, valeur = display.request_filter_criteria()
                        filtered_data = filter.filter_data(data, champ, valeur)
                        print(f"Filtre appliqué. {len(filtered_data)} résultats conservés (sur {len(data)}).")
                        data = filtered_data

                # TRI
                case "5":
                    if not data:
                        print("⚠️ Aucune donnée chargée. Veuillez charger un fichier d'abord.")
                    else:
                        champ = display.request_sort_field()
                        data = sort.sort_data(data, champ)
                        print("✅ Données triées.")

                # SAUVEGARDE
                case "6":
                    if not data:
                        print("⚠️ Rien à sauvegarder.")
                    else:
                        path = display.request_file_path("sauvegarder")
                        fm.save_data(data, path)

                # QUITTER
                case "0":
                    print("👋 Au revoir !\n")
                    break

                case _: print("❌ Choix invalide, veuillez réessayer.")
        
        except Exception as e:
            print(f"\n❌ Une erreur est survenue : {e}")

        input("\nAppuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    main()

    # data = [
    #     {"name": "Alice", "age": 30, "city": "New York"},
    #     {"name": "Bob", "age": 25, "city": "Los Angeles"},
    #     {"name": "Charlie", "age": 35, "city": "Chicago"}
    # ]

    # # Save data
    # fm.save_data(data, "data/output/output.csv")
    # fm.save_data(data, "data/output/output.json")

    # # Load data
    # data_csv = fm.load_data("data/output/output.csv")
    # data_json = fm.load_data("data/output/output.json")
    # print("\nEqual data loaded from CSV and JSON:", data_csv == data_json)
    # print("\nLoaded CSV Data :", data_csv)
    # print("\nLoaded JSON Data:", data_json, "\n")