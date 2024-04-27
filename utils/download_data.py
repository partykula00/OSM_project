import requests
import os


def data_download(link='https://download.geofabrik.de/europe/poland-latest.osm.pbf',
                  folder=os.path.join(os.getcwd(), 'maps')):
    print('Pobieranie z:', link)

    # Wyłuskujemy nazwę pliku bez rozszerzenia .osm
    filename = os.path.splitext(os.path.splitext(os.path.basename(link))[0])[0] + '.pbf'

    path = os.path.join(folder, filename)

    print('Zapisywanie do:', path)

    try:
        response_check = requests.head(link, timeout=5)
    except:
        raise Exception('REQUEST TIMED OUT')

    try:
        response = requests.get(link)
        response.raise_for_status()

        with open(path, 'wb') as f:
            f.write(response.content)

        print(f'Dane zostały pobrane z {link}')
    except requests.RequestException as e:
        print(f'Błąd podczas pobierania danych {e}')

    return path


if __name__ == '__main__':
    data_download()
