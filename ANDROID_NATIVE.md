# Gacha Impact — version Android native

Cette configuration fabrique un APK à partir du **jeu Pygame Python d'origine** du dépôt, et non de la maquette web dans `mobile/`.

## Ce qui est embarqué

- `main.py`, `settings.py`, `library.py`, `character.py`
- les dossiers `img/`, `font/` et `videos/`
- Pygame via SDL2 et OpenCV pour le lecteur vidéo du jeu
- sauvegarde `save.json` dans le stockage privé de l'application Android

L'écran est verrouillé en paysage pour conserver la mise en page prévue par le jeu. Sur Android, Pygame crée une seule surface SDL plein écran à la résolution de l'appareil ; le code de redimensionnement ne recrée pas la fenêtre. Les pressions tactiles sont converties en événements souris Pygame ; les actions existantes (`MOUSEBUTTONUP`) restent donc utilisées.

## Compilation

Le workflow `.github/workflows/android-pygame.yml` construit l'APK avec Buildozer et python-for-android. L'exécution manuelle est également disponible depuis l'onglet Actions.

Récupérer l'artifact `gacha-impact-original-pygame`, puis installer l'APK contenu dans l'archive.

## Important

La compilation doit encore être validée sur un appareil Android réel. La correction d'initialisation SDL doit notamment être vérifiée sur le Fairphone 6. En particulier, le décodage des vidéos MP4 dépend du backend vidéo disponible dans le build OpenCV/Android. Si celui-ci n'est pas disponible sur l'appareil, les tirages eux-mêmes restent prévus pour continuer sans animation vidéo, conformément au comportement de secours déjà présent dans `play_video()`.

## Pourquoi Buildozer

python-for-android fournit les recettes Pygame et OpenCV qui permettent de compiler leurs dépendances natives pour Android. Le jeu reste en Python/Pygame ; il n'est pas redessiné en HTML.
