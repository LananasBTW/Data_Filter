import config
from modules import file_manager as fm
from modules import filter
from modules import stats
from modules import sort
from modules import display

def main():
    # Init
    data = []
    current_filepath = None

    while True:

        try:
            display.clear()
            display.welcome()
            choice = display.menu(current_filepath, data)
            if not choice: continue

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
