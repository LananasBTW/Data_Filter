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
                            data = sort.sort_data(data, field=champ, reverse=reverse)
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
